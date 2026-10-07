"""Exact solution method: set partitioning over enumerated crew workloads.

Same model as src/model.py -- same feasible set, same optimum -- but a far
better encoding.

WHY THIS IS STILL AN ASSIGNMENT MODEL, NOT ROUTING
--------------------------------------------------
A "column" here is one crew's workload for the shift: a set of faults plus the
order it works them. Every job is an independent out-and-back trip from the
Hohoe base. There is no inter-site travel, no travel matrix, no subtour
elimination. The order matters only because a customer later in a crew's shift
waits longer -- that is scheduling, not routing.

WHY IT BEATS THE BIG-M ENCODING
-------------------------------
Because Q = 3, the complete set of ordered workloads is
    15 + 15*14 + 15*14*13 = 2,955
which is small enough to enumerate exhaustively. Each one is priced EXACTLY in
closed form at enumeration time, in plain Python.

That has three consequences that matter:

  1. The column set is COMPLETE, so the set-partitioning optimum is the exact
     optimum -- not a heuristic, not a relaxation.
  2. There is no big-M anywhere, so no weak LP relaxation and no slow solve.
  3. Response times are COMPUTED, never chosen by the solver. The defect found
     in adversarial review -- a model reporting an equity gap of 0.000 while
     its schedule had a gap of 0.588 h -- is structurally impossible here.

Point 3 is the important one and belongs in the paper.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass
from itertools import permutations

import pulp

from .model import Solution


@dataclass(frozen=True)
class Column:
    faults: tuple          # fault indices, in service order
    arrivals: tuple        # response time of each, same order
    duration: float        # crew shift occupancy
    cost: float            # sum of w_j * arrival_j
    zone_sum: dict         # zone -> sum of arrivals in that zone
    max_arrival: float


def enumerate_columns(travel, job_time, zones, weights, capacity, shift_hours,
                      sla_hours=None, sla_faults=None):
    """Every feasible crew workload, priced exactly.

    A workload is admitted iff its total duration fits the shift, and iff it
    satisfies any hard SLA. The SLA is applied here as a column filter: an
    operating rule that would need extra binaries and a big-M in a compact
    model is just a shorter column list here.
    """
    sla_faults = set(sla_faults or ())
    cols, n = [], len(travel)
    for size in range(1, capacity + 1):
        for seq in permutations(range(n), size):
            cum, arrivals, ok = 0.0, [], True
            for j in seq:
                a = cum + travel[j]       # arrival: when the customer is reached
                if sla_hours is not None and j in sla_faults and a > sla_hours + 1e-9:
                    ok = False
                    break
                arrivals.append(a)
                cum += job_time[j]        # out + repair + return to base
            if not ok or cum > shift_hours + 1e-9:
                continue
            zs = {}
            for j, a in zip(seq, arrivals):
                zs[zones[j]] = zs.get(zones[j], 0.0) + a
            cols.append(Column(
                faults=seq, arrivals=tuple(arrivals), duration=cum,
                cost=sum(weights[j] * a for j, a in zip(seq, arrivals)),
                zone_sum=zs, max_arrival=max(arrivals),
            ))
    return cols


def solve(travel, repair, zones, floors, weights, params, *,
          sense="min", epsilon_budget=None, sla_faults=None, msg=False,
          time_limit=300, columns=None):
    """Solve by set partitioning. Signature mirrors model.build_and_solve."""
    n = len(travel)
    s = [2.0 * travel[j] + repair[j] if params.round_trip else travel[j] + repair[j]
         for j in range(n)]
    t0 = time.time()
    if columns is None:
        columns = enumerate_columns(
            travel, s, zones, weights, params.capacity, params.shift_hours,
            params.sla_hours, sla_faults,
        )
    enum_seconds = time.time() - t0
    meta = {"n_columns": len(columns), "enumerate_seconds": enum_seconds}
    if not columns:
        return Solution("Infeasible", {}, {}, None, enum_seconds, 0, 0, meta)

    near = [j for j in range(n) if zones[j] == "Near"]
    far = [j for j in range(n) if zones[j] == "Far"]
    W = sum(weights)

    direction = pulp.LpMaximize if sense == "max" else pulp.LpMinimize
    prob = pulp.LpProblem("ECG_set_partitioning", direction)
    lam = pulp.LpVariable.dicts("lam", range(len(columns)), cat="Binary")
    G = pulp.LpVariable("G", lowBound=0)

    # Coverage: every fault in exactly one crew's workload.
    member = {j: [] for j in range(n)}
    for idx, c in enumerate(columns):
        for j in c.faults:
            member[j].append(idx)
    for j in range(n):
        prob += pulp.lpSum(lam[i] for i in member[j]) == 1, f"cover_{j}"

    # At most m crews are available.
    prob += pulp.lpSum(lam.values()) <= params.n_crews, "crews"

    efficiency = pulp.lpSum(columns[i].cost * lam[i] for i in lam) / W

    if near and far:
        E = {}
        for z, members in (("Near", near), ("Far", far)):
            E[z] = (pulp.lpSum(columns[i].zone_sum.get(z, 0.0) * lam[i] for i in lam)
                    / len(members) - floors[z])
        # Two-sided gap. One-sided would let the solver inflate Near-zone
        # response to manufacture parity.
        prob += G >= E["Far"] - E["Near"], "gap_fn"
        prob += G >= E["Near"] - E["Far"], "gap_nf"
        if params.theta is not None:
            prob += E["Far"] <= params.theta * E["Near"], "cap_far"
            prob += E["Near"] <= params.theta * E["Far"], "cap_near"

    if epsilon_budget is not None:
        prob += efficiency <= epsilon_budget, "eps_budget"
        prob += G                                 # minimise inequity alone
    else:
        prob += params.alpha * efficiency + params.beta * G

    # Capture CBC's own log so the exit condition and gap can be read rather
    # than inferred. PuLP's status alone cannot distinguish a proven optimum
    # from an incumbent returned at the time limit.
    import tempfile, os
    logfd, logpath = tempfile.mkstemp(suffix=".cbclog")
    os.close(logfd)
    try:
        prob.solve(pulp.PULP_CBC_CMD(msg=msg, timeLimit=time_limit,
                                     logPath=logpath))
        cbc_log = open(logpath, errors="replace").read()
    finally:
        try:
            os.unlink(logpath)
        except OSError:
            pass
    elapsed = time.time() - t0
    status = pulp.LpStatus[prob.status]

    # PuLP reports 'Optimal' whenever CBC returns a feasible solution, INCLUDING
    # when CBC stopped on its time limit without completing the search.
    # Reporting that as a proven optimum in a paper would be wrong.
    stopped_on_time = "Stopped on time limit" in cbc_log
    search_completed = "Search completed" in cbc_log
    gap_match = re.search(r"^Gap:\s+([0-9.eE+-]+)", cbc_log, re.M)
    final_gap = float(gap_match.group(1)) if gap_match else None

    # PuLP reports 'Optimal' whenever CBC returns a feasible solution, INCLUDING
    # when CBC stopped on its time limit without proving optimality. Reporting
    # that as a proven optimum in a paper would be wrong, so a solve that ran to
    # the limit is relabelled. It is a genuine incumbent, just not a proven one.
    solve_only = elapsed - enum_seconds
    hit_limit = stopped_on_time or (
        not search_completed and time_limit is not None
        and solve_only >= 0.98 * time_limit)
    if hit_limit and status == "Optimal":
        status = "Feasible (time limit)"
    meta["hit_time_limit"] = bool(hit_limit)
    meta["search_completed"] = bool(search_completed)
    meta["final_gap"] = final_gap        # CBC's reported gap at exit, if any
    meta["solve_seconds"] = solve_only

    schedule, reported = {}, {}
    if status in ("Optimal", "Feasible (time limit)"):
        chosen = [i for i in lam if lam[i].varValue and lam[i].varValue > 0.5]
        for crew, i in enumerate(chosen):
            schedule[crew] = list(columns[i].faults)
        # Every reported figure is recomputed from the chosen columns in plain
        # Python; nothing is read back off a solver variable. verify.check_solution
        # then re-derives all of it independently from the schedule alone.
        resp = {j: a for i in chosen
                for j, a in zip(columns[i].faults, columns[i].arrivals)}
        zone_mean = {z: sum(resp[j] for j in mem) / len(mem)
                     for z, mem in (("Near", near), ("Far", far)) if mem}
        zone_excess = {z: v - floors[z] for z, v in zone_mean.items()}
        reported = {
            "response": resp,
            "makespan": max(columns[i].duration for i in chosen),
            "max_response": max(resp.values()),
            "weighted_mean_response": sum(weights[j] * resp[j] for j in resp) / W,
            "zone_excess": zone_excess,
            "equity_gap": abs(zone_excess.get("Far", 0.0) - zone_excess.get("Near", 0.0)),
        }

    return Solution(
        status=status, schedule=schedule, reported=reported,
        objective=(pulp.value(prob.objective)
                   if status in ("Optimal", "Feasible (time limit)") else None),
        solve_seconds=elapsed, n_variables=len(prob.variables()),
        n_constraints=len(prob.constraints), columns=meta,
    )
