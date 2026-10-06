"""Independent recomputation of every quantity a solve reports.

CORRECTION B4 -- and the most important file in this repository.

Both defects that nearly sank this project shared one shape: a quantity that
looked optimised but was decoupled from the decision.

  v1  the objective was a constant, so "optimal" meant nothing.
  v2  (caught in adversarial review) an arc model pinned response time only by
      minimality, so at beta=1 it reported an equity gap of 0.000 while its
      chosen routes had a gap of 0.588 h.

Neither was caught by reading the model. Both are caught instantly by taking
the schedule the solver chose, recomputing every reported number from it in
plain Python, and asserting agreement.

Every experiment script MUST call check_solution(). No exceptions.
"""
from __future__ import annotations

from dataclasses import dataclass

TOL = 1e-6


class VerificationError(AssertionError):
    """A reported quantity disagrees with its recomputation from the schedule."""


@dataclass
class Recomputed:
    response: dict[int, float]      # fault index -> response time (h)
    loads: dict[int, float]         # crew index -> shift occupancy (h)
    makespan: float
    zone_mean: dict[str, float]
    zone_excess: dict[str, float]
    equity_gap: float
    weighted_mean_response: float
    max_response: float


def recompute(schedule, travel, job_time, zones, floors, weights):
    """Recompute everything from the schedule alone, using no solver output.

    schedule: {crew_index: [fault_index, ...]} in service order.
    """
    response, loads = {}, {}
    for crew, seq in schedule.items():
        cum = 0.0
        for j in seq:
            response[j] = cum + travel[j]   # arrival: the customer's wait
            cum += job_time[j]              # out + repair + return
        loads[crew] = cum

    zone_mean, zone_excess = {}, {}
    # Derive zone labels from the SERVED faults. Using set(zones) directly would
    # take dict keys rather than values when `zones` is a mapping -- a bug this
    # module's own self-test caught, and precisely the silent-zero class of
    # defect the file exists to prevent.
    for z in {zones[j] for j in response}:
        members = [j for j in response if zones[j] == z]
        if members:
            zone_mean[z] = sum(response[j] for j in members) / len(members)
            zone_excess[z] = zone_mean[z] - floors[z]

    gap = abs(zone_excess.get("Far", 0.0) - zone_excess.get("Near", 0.0))
    total_w = sum(weights)
    return Recomputed(
        response=response,
        loads=loads,
        makespan=max(loads.values()) if loads else 0.0,
        zone_mean=zone_mean,
        zone_excess=zone_excess,
        equity_gap=gap,
        weighted_mean_response=sum(weights[j] * response[j] for j in response) / total_w,
        max_response=max(response.values()) if response else 0.0,
    )


def check_solution(schedule, reported, travel, job_time, zones, floors, weights,
                   n_faults, status, shift_hours, capacity=None, tol=TOL):
    """Four assertions. Raises VerificationError on any mismatch.

    `reported` holds the solver's own values, keyed as in Recomputed.
    Returns the recomputation so callers can use trustworthy numbers.
    """
    # 1. Solver status -- parsed, never assumed.
    if status != "Optimal":
        raise VerificationError(f"solver status is {status!r}, not 'Optimal'")

    # 2. Coverage: every fault served exactly once.
    served = [j for seq in schedule.values() for j in seq]
    if sorted(served) != list(range(n_faults)):
        missing = set(range(n_faults)) - set(served)
        dupes = {j for j in served if served.count(j) > 1}
        raise VerificationError(
            f"coverage violated: {len(served)} assignments for {n_faults} faults"
            f"{f', missing {sorted(missing)}' if missing else ''}"
            f"{f', duplicated {sorted(dupes)}' if dupes else ''}"
        )

    rc = recompute(schedule, travel, job_time, zones, floors, weights)

    # 3. Hard constraints actually hold in the schedule, not just in the model.
    for crew, load in rc.loads.items():
        if load > shift_hours + tol:
            raise VerificationError(
                f"crew {crew} works {load:.4f} h, exceeding the {shift_hours} h shift"
            )
    if capacity is not None:
        for crew, seq in schedule.items():
            if len(seq) > capacity:
                raise VerificationError(
                    f"crew {crew} has {len(seq)} faults, exceeding capacity {capacity}"
                )

    # 4. THE ONE THAT MATTERS. Every reported quantity must equal its
    #    recomputation from the chosen schedule.
    for name, got in reported.items():
        want = getattr(rc, name, None)
        if want is None:
            continue
        if isinstance(want, dict):
            for key, w in want.items():
                g = got.get(key)
                if g is None or abs(g - w) > tol:
                    raise VerificationError(
                        f"{name}[{key}]: model reported {g}, schedule gives {w:.6f}. "
                        "The reported quantity is DECOUPLED from the decision."
                    )
        elif abs(got - want) > tol:
            raise VerificationError(
                f"{name}: model reported {got:.6f}, schedule gives {want:.6f} "
                f"(difference {abs(got - want):.2e}). "
                "The reported quantity is DECOUPLED from the decision."
            )
    return rc


def objective_varies(values, min_spread_pct=50.0):
    """Non-degeneracy evidence: the objective must SPREAD over the feasible set.

    Pass the objective values obtained by minimising and maximising the same
    functional over the same feasible set.

    Note the node count is NOT evidence here. The original degenerate model
    reported '0 iterations and 0 nodes' because there was nothing to optimise;
    a tight formulation can report 0 nodes because its LP bound is already
    exact. Only the spread discriminates.
    """
    lo, hi = min(values), max(values)
    spread = 100.0 * (hi - lo) / lo if lo > 0 else float("inf")
    return spread >= min_spread_pct, spread
