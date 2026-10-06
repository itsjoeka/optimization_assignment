"""The ECG technician-assignment model.

CLASS: identical parallel machine scheduling, P || sum_j w_j C_j, with crew
capacity, a shift-duration limit and a spatial-equity constraint.

Each fault is a job. Each crew is a machine. A crew dispatches from the Hohoe
base, repairs, and returns before its next job, so job j occupies
s_j = 2*t_j + r_j of a crew's shift. This is an ASSIGNMENT problem with a
service order -- there is no inter-site travel, no travel matrix, no subtour
elimination and no routing.

WHY THE OBJECTIVE IS RESPONSE TIME AND NOT TRAVEL TIME (correction B1)
----------------------------------------------------------------------
Travel to fault j costs the same whichever crew goes, so under the coverage
constraint sum_i x_ij = 1 the travel objective factors out to the constant
sum_j t_j = 8.985 h. Every feasible assignment scores identically; the solver
optimises nothing. This holds for one-way and round-trip travel alike.

Response time -- hours from shift start until a crew ARRIVES at fault j --
depends on which crew takes the fault and on how many jobs precede it. It is
not additively separable over faults, so no such collapse exists.

The return leg occupies the crew but no customer waits on it, so it enters
s_j (the shift constraint) and never the objective.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pulp


@dataclass
class Solution:
    status: str
    schedule: dict[int, list[int]]
    reported: dict
    objective: float | None
    solve_seconds: float
    n_variables: int
    n_constraints: int
    columns: dict = field(default_factory=dict)


def build_and_solve(
    travel, repair, zones, floors, weights, params,
    *, sense="min", epsilon_budget=None, sla_faults=None,
    msg=False, time_limit=300,
):
    """Build and solve the assignment-and-schedule model.

    sense="max" maximises the same functional over the same feasible set --
    used only to measure the objective's spread as non-degeneracy evidence.

    sla_faults is the set of fault indices bound by params.sla_hours.

    epsilon_budget caps weighted mean response and minimises the equity gap
    alone (the epsilon-constraint form). The weighted sum recovers only
    supported Pareto points, so the frontier figure must use this.
    """
    import time

    n = len(travel)
    m, Q, H = params.n_crews, params.capacity, params.shift_hours
    J, I, K = range(n), range(m), range(Q)
    s = [2.0 * travel[j] + repair[j] if params.round_trip else travel[j] + repair[j]
         for j in J]
    W = sum(weights)
    # Tight big-M. No arrival can exceed the shift, so H bounds every term.
    M = H

    direction = pulp.LpMaximize if sense == "max" else pulp.LpMinimize
    prob = pulp.LpProblem("ECG_technician_assignment", direction)

    # y[i][j][k] = 1 iff crew i serves fault j at position k of its shift.
    y = pulp.LpVariable.dicts("y", (I, J, K), cat="Binary")
    R = pulp.LpVariable.dicts("R", J, lowBound=0)          # response time
    G = pulp.LpVariable("G", lowBound=0)                   # equity gap
    Cmax = pulp.LpVariable("Cmax", lowBound=0)
    Rmax = pulp.LpVariable("Rmax", lowBound=0)

    load = {i: pulp.lpSum(s[j] * y[i][j][k] for j in J for k in K) for i in I}

    # --- C1 Coverage: every fault served exactly once -----------------------
    for j in J:
        prob += pulp.lpSum(y[i][j][k] for i in I for k in K) == 1, f"coverage_{j}"

    for i in I:
        # --- C2 One fault per position slot --------------------------------
        for k in K:
            prob += pulp.lpSum(y[i][j][k] for j in J) <= 1, f"slot_{i}_{k}"
        # --- C3 No idle gaps: position k+1 used only if k is ---------------
        for k in list(K)[:-1]:
            prob += (pulp.lpSum(y[i][j][k] for j in J)
                     >= pulp.lpSum(y[i][j][k + 1] for j in J)), f"nogap_{i}_{k}"
        # --- C4 Shift-duration limit ---------------------------------------
        prob += load[i] <= H, f"shift_{i}"
        # --- C5 Makespan ----------------------------------------------------
        prob += Cmax >= load[i], f"cmax_{i}"

    # --- C6 Response time, PINNED BY EQUALITY -------------------------------
    # Both inequalities are mandatory. With only the >= side, R is driven to the
    # true arrival time solely by the efficiency term; whenever the objective
    # stops pushing it down (beta=1, or an epsilon-constraint), the solver
    # inflates R and buys equity with fiction. That defect was found in
    # adversarial review reporting a gap of 0.000 against a true 0.588 h.
    for i in I:
        for k in K:
            before = pulp.lpSum(s[jj] * y[i][jj][kk]
                                for jj in J for kk in K if kk < k)
            for j in J:
                slack = M * (1 - y[i][j][k])
                prob += R[j] >= before + travel[j] - slack, f"arr_lo_{i}_{j}_{k}"
                prob += R[j] <= before + travel[j] + slack, f"arr_hi_{i}_{j}_{k}"

    for j in J:
        prob += Rmax >= R[j], f"rmax_{j}"

    # --- C7 Equity on EXCESS WAIT (correction M2) ---------------------------
    # E^z = mean response in zone z minus that zone's mean one-way travel.
    # Far towns are further by construction; measuring raw means would let the
    # model "achieve equity" only by delaying Near customers.
    near = [j for j in J if zones[j] == "Near"]
    far = [j for j in J if zones[j] == "Far"]
    excess = {}
    if near and far:
        E_near = pulp.lpSum(R[j] for j in near) / len(near) - floors["Near"]
        E_far = pulp.lpSum(R[j] for j in far) / len(far) - floors["Far"]
        excess = {"Near": E_near, "Far": E_far}
        # Two-sided gap. One-sided would let the solver inflate Near-zone
        # response to manufacture parity.
        prob += G >= E_far - E_near, "gap_far_minus_near"
        prob += G >= E_near - E_far, "gap_near_minus_far"
        # Two-sided hard cap, valid only for theta >= 1 (enforced in Params).
        if params.theta is not None:
            prob += E_far <= params.theta * E_near, "equity_cap_far"
            prob += E_near <= params.theta * E_far, "equity_cap_near"

    # --- C8 Optional hard SLA on high-priority faults -----------------------
    # Operationally the form an ECG engineer recognises: "every high-priority
    # fault reached within D hours". Sweeping D locates the feasibility
    # threshold, which is the result a utility can actually act on.
    if params.sla_hours is not None and sla_faults:
        for j in sla_faults:
            prob += R[j] <= params.sla_hours, f"sla_{j}"

    # --- Symmetry breaking --------------------------------------------------
    # Crews are identical, so any solution can be permuted to satisfy this.
    # Removes the m! = 120-fold symmetry without cutting off any optimum.
    for i in list(I)[:-1]:
        prob += load[i] >= load[i + 1], f"sym_{i}"

    # --- Objective ----------------------------------------------------------
    efficiency = pulp.lpSum(weights[j] * R[j] for j in J) / W
    if epsilon_budget is not None:
        prob += efficiency <= epsilon_budget, "epsilon_budget"
        prob += G                                  # minimise inequity alone
    else:
        prob += params.alpha * efficiency + params.beta * G

    t0 = time.time()
    prob.solve(pulp.PULP_CBC_CMD(msg=msg, timeLimit=time_limit))
    elapsed = time.time() - t0
    status = pulp.LpStatus[prob.status]

    schedule, reported = {}, {}
    if status == "Optimal":
        for i in I:
            seq = []
            for k in K:
                for j in J:
                    if y[i][j][k].varValue is not None and y[i][j][k].varValue > 0.5:
                        seq.append(j)
            if seq:
                schedule[i] = seq
        reported = {
            "response": {j: R[j].varValue for j in J},
            "equity_gap": G.varValue,
            "makespan": Cmax.varValue,
            "max_response": Rmax.varValue,
            "weighted_mean_response": sum(weights[j] * R[j].varValue for j in J) / W,
        }
        if excess:
            reported["zone_excess"] = {
                z: float(pulp.value(e)) for z, e in excess.items()
            }

    return Solution(
        status=status,
        schedule=schedule,
        reported=reported,
        objective=pulp.value(prob.objective) if status == "Optimal" else None,
        solve_seconds=elapsed,
        n_variables=len(prob.variables()),
        n_constraints=len(prob.constraints),
    )
