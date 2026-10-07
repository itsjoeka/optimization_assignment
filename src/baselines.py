"""Benchmark policies to compare the optimum against.

CORRECTION B5 and C9. The original repository compared the optimum against a
SINGLE random draw that was itself infeasible (one crew worked 11.667 h against
an 8 h shift). That is not a benchmark.

Three things are fixed here:

  1. FEASIBILITY IS MEASURED, NOT ASSUMED. Every policy is checked against the
     shift and capacity constraints, and the feasibility RATE is reported.
     On this instance it is the headline result, because an ad-hoc plan that
     does not fit the shift is not a plan.

  2. STRONG BARS, NOT STRAW MEN. Greedy and local search are included, so the
     optimum has to beat something that a competent dispatcher might actually
     do. If the optimum only beats local search by a few percent, that is worth
     knowing before a referee discovers it.

  3. BEST-OF-N AS AN ORDER STATISTIC. Comparing against the MEAN of feasible
     random draws flatters the optimum. Best-of-N is the fairer bar and is
     reported alongside.

Every policy returns a schedule {crew: [fault indices in service order]}, scored
by the same evaluate() the model is scored by, so the comparison is like-for-like.
"""
from __future__ import annotations

import random
from itertools import permutations


def evaluate(schedule, travel, job_time, zones, floors, weights, params):
    """Score a schedule on the model's own objective. Returns None if infeasible.

    Infeasible means it violates the shift limit or crew capacity -- the two
    constraints the model enforces and an ad-hoc plan can breach.
    """
    response, loads = {}, {}
    for crew, seq in schedule.items():
        if len(seq) > params.capacity:
            return None
        cum = 0.0
        for j in seq:
            response[j] = cum + travel[j]
            cum += job_time[j]
        if cum > params.shift_hours + 1e-9:
            return None
        loads[crew] = cum
    if len(schedule) > params.n_crews:
        return None

    zone_excess = {}
    for z in {zones[j] for j in response}:
        members = [j for j in response if zones[j] == z]
        zone_excess[z] = sum(response[j] for j in members) / len(members) - floors[z]
    gap = abs(zone_excess.get("Far", 0.0) - zone_excess.get("Near", 0.0))
    W = sum(weights)
    mean_resp = sum(weights[j] * response[j] for j in response) / W
    return {
        "weighted_mean_response": mean_resp,
        "equity_gap": gap,
        "makespan": max(loads.values()),
        "max_response": max(response.values()),
        "zone_excess": zone_excess,
        "objective": params.alpha * mean_resp + params.beta * gap,
    }


def _best_order(seq, travel, job_time, weights):
    """Exact best service order for one crew's fault set.

    With Q <= 3 there are at most 6 permutations, so this is exhaustive rather
    than heuristic. Minimises that crew's contribution to weighted response.
    """
    best, best_cost = None, float("inf")
    for perm in permutations(seq):
        cum, cost = 0.0, 0.0
        for j in perm:
            cost += weights[j] * (cum + travel[j])
            cum += job_time[j]
        if cost < best_cost:
            best, best_cost = list(perm), cost
    return best


# --- policies ---------------------------------------------------------------

def random_round_robin(n, params, seed):
    """The original repository's baseline: shuffle, deal round-robin.

    Reproduced exactly so the paper can report what the naive approach gives.
    """
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return {k: idx[k::params.n_crews] for k in range(params.n_crews)}


def random_ordered(n, params, seed, travel, job_time, weights):
    """Random assignment, but each crew then works its faults in the best order.

    Separates two effects: a bad ASSIGNMENT versus a bad ORDER. Without this,
    the optimum's advantage over random conflates the two.
    """
    sched = random_round_robin(n, params, seed)
    return {k: _best_order(v, travel, job_time, weights) for k, v in sched.items() if v}


def greedy_shortest_job(n, params, travel, job_time, weights):
    """Shortest-job-first onto the least-loaded crew.

    The strongest simple rule for mean response time: on a single machine,
    shortest-processing-time order minimises mean completion time. This is the
    bar a competent dispatcher could plausibly reach by instinct.
    """
    order = sorted(range(n), key=lambda j: job_time[j])
    sched = {k: [] for k in range(params.n_crews)}
    loads = {k: 0.0 for k in range(params.n_crews)}
    for j in order:
        avail = [k for k in sched
                 if len(sched[k]) < params.capacity
                 and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
        if not avail:
            return None                      # policy failed to place every fault
        k = min(avail, key=lambda k: loads[k])
        sched[k].append(j)
        loads[k] += job_time[j]
    return {k: v for k, v in sched.items() if v}


def greedy_longest_job(n, params, travel, job_time, weights):
    """Longest-job-first onto the least-loaded crew, then best order within each crew.

    This is the FEASIBILITY heuristic. Classic LPT list scheduling: placing the
    big jobs while every crew is still empty is what makes a tight instance
    pack at all. Shortest-job-first is the right rule for mean response but a
    bad rule for packing -- on the published instance (95% crew utilisation) it
    paints itself into a corner and fails to place the last faults.

    Reporting "every heuristic fails" without including LPT would be a straw
    man, so this is the fair bar the optimum must beat.
    """
    order = sorted(range(n), key=lambda j: -job_time[j])
    sched = {k: [] for k in range(params.n_crews)}
    loads = {k: 0.0 for k in range(params.n_crews)}
    for j in order:
        avail = [k for k in sched
                 if len(sched[k]) < params.capacity
                 and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
        if not avail:
            return None
        k = min(avail, key=lambda k: loads[k])
        sched[k].append(j)
        loads[k] += job_time[j]
    # LPT fixes the ASSIGNMENT; the order within each crew is then set exactly.
    return {k: _best_order(v, travel, job_time, weights)
            for k, v in sched.items() if v}


def greedy_nearest(n, params, travel, job_time, weights):
    """Nearest-first onto the least-loaded crew."""
    order = sorted(range(n), key=lambda j: travel[j])
    sched = {k: [] for k in range(params.n_crews)}
    loads = {k: 0.0 for k in range(params.n_crews)}
    for j in order:
        avail = [k for k in sched
                 if len(sched[k]) < params.capacity
                 and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
        if not avail:
            return None
        k = min(avail, key=lambda k: loads[k])
        sched[k].append(j)
        loads[k] += job_time[j]
    return {k: v for k, v in sched.items() if v}


def greedy_priority(n, params, travel, job_time, weights, priorities):
    """High-priority faults placed first, then shortest job.

    Approximates a dispatcher working an urgency list.
    """
    order = sorted(range(n),
                   key=lambda j: (0 if priorities[j] == "High" else 1, job_time[j]))
    sched = {k: [] for k in range(params.n_crews)}
    loads = {k: 0.0 for k in range(params.n_crews)}
    for j in order:
        avail = [k for k in sched
                 if len(sched[k]) < params.capacity
                 and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
        if not avail:
            return None
        k = min(avail, key=lambda k: loads[k])
        sched[k].append(j)
        loads[k] += job_time[j]
    return {k: v for k, v in sched.items() if v}


def zone_clustered(n, params, travel, job_time, weights, zones):
    """Crews specialise by zone -- a natural and common dispatch convention."""
    near = sorted([j for j in range(n) if zones[j] == "Near"], key=lambda j: job_time[j])
    far = sorted([j for j in range(n) if zones[j] == "Far"], key=lambda j: job_time[j])
    n_far_crews = max(1, round(params.n_crews * len(far) / n))
    groups = {"Far": list(range(n_far_crews)),
              "Near": list(range(n_far_crews, params.n_crews))}
    sched = {k: [] for k in range(params.n_crews)}
    loads = {k: 0.0 for k in range(params.n_crews)}
    for pool, crews in ((far, groups["Far"]), (near, groups["Near"])):
        for j in pool:
            avail = [k for k in crews
                     if len(sched[k]) < params.capacity
                     and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
            if not avail:                     # spill over rather than fail outright
                avail = [k for k in sched
                         if len(sched[k]) < params.capacity
                         and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
            if not avail:
                return None
            k = min(avail, key=lambda k: loads[k])
            sched[k].append(j)
            loads[k] += job_time[j]
    return {k: v for k, v in sched.items() if v}


def local_search(schedule, travel, job_time, zones, floors, weights, params,
                 max_passes=200):
    """Steepest-descent relocate + swap, with exact re-ordering inside each crew.

    This is the fairest bar in the suite: what a careful dispatcher reaches by
    trial and error. If the exact optimum barely beats it, the paper should say
    so plainly rather than let a referee find it.
    """
    if schedule is None:
        return None
    cur = {k: _best_order(list(v), travel, job_time, weights)
           for k, v in schedule.items() if v}
    best = evaluate(cur, travel, job_time, zones, floors, weights, params)
    if best is None:
        return None

    # First-improvement with restart. The schedule is REPLACED on every accepted
    # move, so the loop must restart rather than keep iterating over a stale
    # snapshot -- doing otherwise tries to relocate a fault that has already
    # moved and raises ValueError from list.remove.
    for _ in range(max_passes):
        improved = False
        for a in list(cur):
            if improved:
                break
            for j in list(cur.get(a, [])):
                if improved:
                    break
                # relocate j into another crew
                for b in range(params.n_crews):
                    if b == a:
                        continue
                    cand = {k: list(v) for k, v in cur.items()}
                    if j not in cand.get(a, []):
                        continue
                    cand.setdefault(b, [])
                    cand[a].remove(j)
                    cand[b].append(j)
                    cand = {k: _best_order(v, travel, job_time, weights)
                            for k, v in cand.items() if v}
                    sc = evaluate(cand, travel, job_time, zones, floors, weights, params)
                    if sc and sc["objective"] < best["objective"] - 1e-12:
                        cur, best, improved = cand, sc, True
                        break
                if improved:
                    break
                # swap j with a fault in another crew
                for b in list(cur):
                    if b == a:
                        continue
                    for j2 in list(cur.get(b, [])):
                        cand = {k: list(v) for k, v in cur.items()}
                        if j not in cand.get(a, []) or j2 not in cand.get(b, []):
                            continue
                        cand[a].remove(j)
                        cand[b].remove(j2)
                        cand[a].append(j2)
                        cand[b].append(j)
                        cand = {k: _best_order(v, travel, job_time, weights)
                                for k, v in cand.items() if v}
                        sc = evaluate(cand, travel, job_time, zones, floors,
                                      weights, params)
                        if sc and sc["objective"] < best["objective"] - 1e-12:
                            cur, best, improved = cand, sc, True
                            break
                    if improved:
                        break
        if not improved:
            break
    return cur


def run_all(n, params, travel, job_time, zones, floors, weights, priorities,
            n_random=2000):
    """Every policy, scored. Returns {policy_name: result-or-None}.

    Random policies report feasibility rate, the mean over feasible draws, and
    best-of-N as an order statistic.
    """
    out = {}
    common = (travel, job_time, zones, floors, weights, params)

    for label, fn in (
        ("random_round_robin", lambda s: random_round_robin(n, params, s)),
        ("random_best_order",
         lambda s: random_ordered(n, params, s, travel, job_time, weights)),
    ):
        feasible = []
        for seed in range(n_random):
            sc = evaluate(fn(seed), *common)
            if sc:
                feasible.append(sc)
        out[label] = {
            "n_trials": n_random,
            "n_feasible": len(feasible),
            "feasibility_rate": len(feasible) / n_random,
            "mean_of_feasible": (
                sum(x["weighted_mean_response"] for x in feasible) / len(feasible)
                if feasible else None),
            "best_of_n": (min(x["weighted_mean_response"] for x in feasible)
                          if feasible else None),
            "best_objective": (min(x["objective"] for x in feasible)
                               if feasible else None),
            "mean_gap_of_feasible": (
                sum(x["equity_gap"] for x in feasible) / len(feasible)
                if feasible else None),
        }

    deterministic = {
        "greedy_bfd_repair": greedy_bfd_repair(n, params, travel, job_time, weights),
        "greedy_longest_job": greedy_longest_job(n, params, travel, job_time, weights),
        "greedy_shortest_job": greedy_shortest_job(n, params, travel, job_time, weights),
        "greedy_nearest": greedy_nearest(n, params, travel, job_time, weights),
        "greedy_priority": greedy_priority(n, params, travel, job_time, weights,
                                           priorities),
        "zone_clustered": zone_clustered(n, params, travel, job_time, weights, zones),
    }
    for label, sched in deterministic.items():
        out[label] = evaluate(sched, *common) if sched else None

    # Seed local search from the best feasible starting point available: LPT
    # first (it packs), then any other greedy, then a feasible random draw.
    # Seeding only from a policy that failed would understate local search.
    seed_sched = None
    for label in ("greedy_bfd_repair", "greedy_longest_job",
                  "greedy_shortest_job", "greedy_nearest",
                  "greedy_priority", "zone_clustered"):
        if deterministic.get(label) and out.get(label):
            seed_sched = deterministic[label]
            break
    if seed_sched is None:
        for sd in range(n_random):
            cand = random_ordered(n, params, sd, travel, job_time, weights)
            if evaluate(cand, *common):
                seed_sched = cand
                break
    ls = local_search(seed_sched, travel, job_time, zones, floors, weights, params)
    out["local_search"] = evaluate(ls, *common) if ls else None
    out["_schedules"] = dict(deterministic, local_search=ls)
    return out


def greedy_bfd_repair(n, params, travel, job_time, weights, max_restarts=200):
    """Best-fit-decreasing with 1-swap repair -- the strongest feasibility bar.

    The published instance runs at 95% crew utilisation with capacity exactly
    equal to demand, so plain list scheduling gets stuck with two small faults
    and no crew able to take them. A real dispatcher in that position would not
    give up; they would rearrange. This policy does the same:

      * best-fit-decreasing placement (tightest feasible crew, not least-loaded,
        which is the better rule when the packing is tight), then
      * when stuck on fault j, try swapping it in for an already-placed j' and
        relocating j' elsewhere, then
      * failing that, restart from a randomised order.

    Including this is what stops "every heuristic fails" from being a straw man.
    """
    import random as _r

    def attempt(order):
        sched = {k: [] for k in range(params.n_crews)}
        loads = {k: 0.0 for k in range(params.n_crews)}
        for j in order:
            avail = [k for k in sched
                     if len(sched[k]) < params.capacity
                     and loads[k] + job_time[j] <= params.shift_hours + 1e-9]
            if avail:
                # best fit: leave the least slack behind
                k = min(avail, key=lambda k: params.shift_hours - loads[k] - job_time[j])
                sched[k].append(j)
                loads[k] += job_time[j]
                continue
            # 1-swap repair: evict j' to make room for j, rehome j' elsewhere
            placed = False
            for k in sched:
                if placed:
                    break
                for jp in list(sched[k]):
                    if loads[k] - job_time[jp] + job_time[j] > params.shift_hours + 1e-9:
                        continue
                    for k2 in sched:
                        if k2 == k:
                            continue
                        if (len(sched[k2]) < params.capacity
                                and loads[k2] + job_time[jp]
                                <= params.shift_hours + 1e-9):
                            sched[k].remove(jp)
                            loads[k] -= job_time[jp]
                            sched[k].append(j)
                            loads[k] += job_time[j]
                            sched[k2].append(jp)
                            loads[k2] += job_time[jp]
                            placed = True
                            break
                    if placed:
                        break
            if not placed:
                return None
        return {k: _best_order(v, travel, job_time, weights)
                for k, v in sched.items() if v}

    base = sorted(range(n), key=lambda j: -job_time[j])
    got = attempt(base)
    if got:
        return got
    rng = _r.Random(0)
    for _ in range(max_restarts):
        order = base[:]
        rng.shuffle(order)
        got = attempt(order)
        if got:
            return got
    return None
