# csv_serializer.py
import re
from typing import Dict, List, Optional
import pandas as pd
from workout import Exercise, MuscleGroup, Workout, Set

# Expected schemas
EXPECTED_EXERCISE_COLS = ["name", "parent_exercise", "muscle_groups", "description", "form_notes", ]
EXPECTED_WORKOUT_COLS = ["date", "exercise", "reps", "weight", "notes", ]

def read_exercises_from_csv(path: str) -> Dict[str, Exercise]:
    """
    Read exercises CSV and return a dict keyed by exercise name.
    Validates expected headers and resolves parent_exercise references.
    """
    df = pd.read_csv(path)

    missing = [c for c in EXPECTED_EXERCISE_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns in exercises CSV: {missing}. Found: {df.columns.tolist()}"
        )

    temp: Dict[str, Dict] = {}
    exercises: Dict[str, Exercise] = {}

    for _, row in df.iterrows():
        name = str(row["name"]).strip()
        parent_name: Optional[str] = (
            str(row["parent_exercise"]).strip()
            if pd.notna(row["parent_exercise"]) and str(row["parent_exercise"]).strip()
            else None
        )

        # Parse muscle groups into MuscleGroup enums
        mg_raw = row["muscle_groups"] if pd.notna(row["muscle_groups"]) else ""
        muscle_groups = []
        for m in re.split(r"[,;]", str(mg_raw)):
            m = m.strip()
            if not m:
                continue
            try:
                muscle_groups.append(MuscleGroup[m.upper()])
            except KeyError:
                # fallback: match against values (e.g. "Legs")
                match = next((g for g in MuscleGroup if g.value.lower() == m.lower()), None)
                if match:
                    muscle_groups.append(match)

        description = row["description"] if pd.notna(row["description"]) else ""
        form_notes = row["form_notes"] if pd.notna(row["form_notes"]) else ""

        exercises[name] = Exercise(
            name=name,
            parent_exercise=None,  # resolve later
            muscle_groups=muscle_groups,
            description=description,
            form_notes=form_notes,
        )
        temp[name] = {"parent_name": parent_name}

    # Second pass → resolve parent references
    for name, meta in temp.items():
        parent_name = meta["parent_name"]
        if parent_name and parent_name in exercises:
            exercises[name].parent_exercise = exercises[parent_name]

    return exercises

def read_workouts_from_csv(file_path: str, exercises: dict) -> list[Workout]:
    df = pd.read_csv(file_path)

    # Validate headers
    missing = [c for c in EXPECTED_WORKOUT_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns in workout CSV: {missing}")

    workouts: list[Workout] = []

    # Group by date to create one Workout per date
    grouped = df.groupby("date")

    for date, group in grouped:
        sets: list[Set] = []
        workout_notes: list[str] = []

        for _, row in group.iterrows():
            ex_name = row["exercise"]
            if ex_name not in exercises:
                raise ValueError(f"Unknown exercise '{ex_name}' in workout log")

            exercise = exercises[ex_name]

            workout_set = Set(
                exercise=exercise,
                reps=int(row["reps"]) if not pd.isna(row["reps"]) else 0,
                weight=str(row["weight"]) if not pd.isna(row["weight"]) else "",
                notes=str(row["notes"]).strip() if not pd.isna(row["notes"]) else "",
            )

            sets.append(workout_set)
            if workout_set.notes:
                workout_notes.append(workout_set.notes)

        workout_notes = " | ".join(workout_notes) if workout_notes else None
        workouts.append(Workout(date=date, exercises=sets, notes=workout_notes))

    return workouts