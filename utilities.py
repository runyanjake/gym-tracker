# utilities.py
import re
from collections import defaultdict
from typing import Dict, List
from workout import Workout, MuscleGroup

def safe_filename(name: str) -> str:
    """Convert exercise name to a uniform safe filename."""
    return re.sub(r"[^\w\d]+", "_", name.strip().lower())

def group_by_muscle(workouts: List[Workout]) -> Dict[MuscleGroup, int]:
    """
    Aggregate total number of sets per muscle group across all workouts.
    """
    muscle_counts: Dict[MuscleGroup, int] = defaultdict(int)

    for workout in workouts:
        for s in workout.exercises:
            for mg in s.exercise.muscle_groups:
                muscle_counts[mg] += 1

    return dict(muscle_counts)


def summarize_progress(workouts: List[Workout]):
    """
    Simple console printout of progress across time.
    Could be expanded into more advanced analysis.
    """
    print("Progress summary:")
    for w in workouts:
        print(f"Date: {w.date}, Sets: {len(w.exercises)}, Notes: {w.notes or '-'}")
