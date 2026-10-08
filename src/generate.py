"""Synthetic fault-instance generator.

The 23 towns and their travel times are REAL field data. The faults are
SYNTHETIC. This module makes that generation explicit, seeded and reusable, so
the multi-instance study rests on a documented process rather than on a figure
produced once in a notebook.

CORRECTION B6: the paper must disclose in the ABSTRACT that fault instances are
simulated, and must state that the two distributions below are assumptions
without a published source. Obtaining ECG's historical fault log would replace
them with measured frequencies and materially strengthen the paper.
"""
from __future__ import annotations

import random

import pandas as pd

from .data import classify_zone, load_towns

# Repair time by fault type, in hours. Supplied by the project team from ECG
# practice; no published source. CONFIRM WITH ECG.
FAULT_TYPES = {
    "Transformer installation": 4.0,
    "Transformer maintenance": 0.75,
    "Cable joining and termination": 0.33,
    "Network line extension": 2.0,
    "Pole replacement": 1.0,
    "Vegetation control": 4.0,
}

# ASSUMED fault-type mix. No source. State as an assumption in Methods.
TYPE_WEIGHTS = [0.15, 0.25, 0.20, 0.15, 0.10, 0.15]

# ASSUMED priority split. No source. State as an assumption in Methods.
PRIORITY_LEVELS = ["High", "Normal"]
PRIORITY_WEIGHTS = [0.30, 0.70]

PUBLISHED_SEED = 60   # reproduces dataset/ecg_faults_dataset.csv


def generate_faults(n_faults=15, seed=PUBLISHED_SEED, threshold_km=None):
    """Draw a synthetic fault instance against the real town network.

    seed=60, n_faults=15 reproduces the committed dataset exactly, which is the
    check that this module and the original notebook agree.
    """
    rng = random.Random(seed)
    towns = load_towns() if threshold_km is None else load_towns(threshold_km)

    chosen = rng.choices(towns["service_town"].tolist(), k=n_faults)
    types = rng.choices(list(FAULT_TYPES), weights=TYPE_WEIGHTS, k=n_faults)
    priorities = rng.choices(PRIORITY_LEVELS, weights=PRIORITY_WEIGHTS, k=n_faults)

    by_town = towns.set_index("service_town")
    rows = []
    for i, (town, ftype, prio) in enumerate(zip(chosen, types, priorities), start=1):
        t = by_town.loc[town]
        rows.append({
            "Fault_ID": f"F{i}",
            "Town": town,
            "Zone": (classify_zone(float(t["distance_in_km"]), threshold_km)
                     if threshold_km is not None else t["zone"]),
            "Distance_km": float(t["distance_in_km"]),
            "Travel_time_hours": round(float(t["travel_time_in_hours"]), 3),
            "Fault_type": ftype,
            "Repair_time_hours": FAULT_TYPES[ftype],
            "Priority": prio,
        })
    return pd.DataFrame(rows)


def reproduces_published(published_csv) -> bool:
    """True iff generate_faults(15, 60) matches the committed dataset.

    Guards against this module and the original notebook silently diverging.
    """
    want = pd.read_csv(published_csv)
    got = generate_faults(15, PUBLISHED_SEED)
    cols = ["Fault_ID", "Town", "Distance_km", "Travel_time_hours",
            "Fault_type", "Repair_time_hours", "Priority"]
    return want[cols].equals(got[cols])
