"""Data loading, zone classification and validation.

All loading goes through here so the zone rule is applied in exactly one place.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import SUSPECT_TOWNS, ZONE_THRESHOLD_KM

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def classify_zone(distance_km: float, threshold_km: float = ZONE_THRESHOLD_KM) -> str:
    """Near if within the threshold, Far otherwise.

    CORRECTION M1: the threshold is exogenous, not ceil(max(distance))/2.
    Boundary is inclusive, matching the README's "Near: <= 20 km".
    """
    return "Near" if distance_km <= threshold_km else "Far"


def load_towns(threshold_km: float = ZONE_THRESHOLD_KM) -> pd.DataFrame:
    """The 23 real service towns with field-measured distance and travel time."""
    df = pd.read_csv(DATASET / "ecg_towns_dataset.csv")
    df["zone"] = df["distance_in_km"].apply(classify_zone, threshold_km=threshold_km)
    df["implied_speed_kmh"] = df["distance_in_km"] / df["travel_time_in_hours"]
    df["data_quality_flag"] = df["service_town"].map(
        lambda t: SUSPECT_TOWNS.get(t, "")
    )
    return df


def load_faults(threshold_km: float = ZONE_THRESHOLD_KM) -> pd.DataFrame:
    """The 15 SIMULATED faults.

    The towns and travel times are real field data; the faults are synthetic
    (random.choices, seed 60). This must be disclosed in the abstract --
    CORRECTION B6.

    Zones are recomputed from distance rather than trusted from the CSV, so the
    threshold decision propagates everywhere.
    """
    df = pd.read_csv(DATASET / "ecg_faults_dataset.csv")
    df["Zone"] = df["Distance_km"].apply(classify_zone, threshold_km=threshold_km)
    return df


def job_times(faults: pd.DataFrame, round_trip: bool = True) -> list[float]:
    """Occupancy of fault j in a crew's shift.

    Base-to-site dispatch: the crew drives out, repairs, and returns to the
    Hohoe base before its next job. s_j = 2*t_j + r_j.

    Note this is NOT the response time -- the return leg occupies the crew but
    no customer waits on it, so it never enters the objective.
    """
    multiplier = 2.0 if round_trip else 1.0
    return [
        multiplier * float(t) + float(r)
        for t, r in zip(faults["Travel_time_hours"], faults["Repair_time_hours"])
    ]


def zone_floors(faults: pd.DataFrame) -> dict[str, float]:
    """Mean one-way travel per zone: the geographic floor a crew cannot beat.

    CORRECTION M2: equity is measured as excess wait above this floor, not as
    raw mean response. Far towns are further by construction; equalising raw
    means could only be achieved by delaying Near customers.
    """
    return {
        z: float(g["Travel_time_hours"].mean())
        for z, g in faults.groupby("Zone")
    }


def priority_weights(faults: pd.DataFrame, high_weight: float = 1.0) -> list[float]:
    """Per-fault objective weights.

    CORRECTION M3: default 1.0. Four of the five High-priority faults in the
    published instance are in Far towns, so any high_weight > 1 moves the
    Far/Near ratio with no equity mechanism doing the work. Every equity
    experiment must run at high_weight = 1.0.
    """
    return [high_weight if p == "High" else 1.0 for p in faults["Priority"]]


def describe_instance(faults: pd.DataFrame) -> dict:
    """Facts a results section needs, computed once."""
    near = faults[faults["Zone"] == "Near"]
    far = faults[faults["Zone"] == "Far"]
    return {
        "n_faults": len(faults),
        "n_near": len(near),
        "n_far": len(far),
        "mean_travel_near": float(near["Travel_time_hours"].mean()),
        "mean_travel_far": float(far["Travel_time_hours"].mean()),
        "total_travel_oneway": float(faults["Travel_time_hours"].sum()),
        "total_repair": float(faults["Repair_time_hours"].sum()),
        "n_high_priority": int((faults["Priority"] == "High").sum()),
        "n_high_priority_far": int(
            ((faults["Priority"] == "High") & (faults["Zone"] == "Far")).sum()
        ),
        "distinct_towns": int(faults["Town"].nunique()),
    }
