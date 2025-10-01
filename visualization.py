import os
import pygal
from datetime import datetime
from collections import defaultdict
from workout import Workout
import statistics

from utilities import safe_filename

def plot_lifting_volume(workouts: list[Workout], exercise_name: str):
    volume_by_date = defaultdict(int)
    for w in workouts:
        for s in w.exercises:
            if s.exercise.name == exercise_name and s.weight and s.reps:
                try:
                    weight = float(s.weight)
                    volume_by_date[w.date] += s.reps * weight
                except ValueError:
                    print(f"Skipping invalid weight '{s.weight}' in workout on {w.date}")
    if not volume_by_date:
        print(f"No weighted data for {exercise_name}. Skipping volume plot.")
        return

    sorted_dates = sorted(volume_by_date.keys(), key=lambda d: datetime.fromisoformat(d))
    sorted_volumes = [volume_by_date[d] for d in sorted_dates]

    chart = pygal.Line()
    chart.title = f"Lifting Volume Over Time: {exercise_name}"
    chart.x_labels = sorted_dates
    chart.add(exercise_name, sorted_volumes)

    output_dir = os.path.join("output", "volume")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{safe_filename(exercise_name)}.svg")
    chart.render_to_file(output_file)
    print(f"Saved lifting volume chart to {output_file}")


def plot_total_reps(workouts: list[Workout], exercise_name: str):
    reps_by_date = defaultdict(int)
    for w in workouts:
        for s in w.exercises:
            if s.exercise.name == exercise_name and s.reps:
                reps_by_date[w.date] += s.reps
    if not reps_by_date:
        print(f"No rep-only data for {exercise_name}. Skipping reps plot.")
        return

    sorted_dates = sorted(reps_by_date.keys(), key=lambda d: datetime.fromisoformat(d))
    sorted_reps = [reps_by_date[d] for d in sorted_dates]

    chart = pygal.Line()
    chart.title = f"Total Reps Over Time: {exercise_name}"
    chart.x_labels = sorted_dates
    chart.add(exercise_name, sorted_reps)

    output_dir = os.path.join("output", "reps")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{safe_filename(exercise_name)}.svg")
    chart.render_to_file(output_file)
    print(f"Saved total reps chart to {output_file}")


def plot_weight_stats(workouts: list[Workout], exercise_name: str):
    weights_by_date = defaultdict(list)
    for w in workouts:
        for s in w.exercises:
            if s.exercise.name == exercise_name and s.weight:
                try:
                    weight = float(s.weight)
                    weights_by_date[w.date].append(weight)
                except ValueError:
                    print(f"Skipping invalid weight '{s.weight}' in workout on {w.date}")
    if not weights_by_date:
        print(f"No weighted data for {exercise_name}. Skipping weight stats plot.")
        return

    print(f"\n--- DEBUG: Weights by Date for {exercise_name} ---")
    for date, weights in weights_by_date.items():
        print(f"  {date}: {len(weights)} set(s) -> {weights}")
    print("--------------------------------------------------\n")

    sorted_dates = sorted(weights_by_date.keys(), key=lambda d: datetime.fromisoformat(d))
    min_weights = [min(weights_by_date[d]) for d in sorted_dates]
    max_weights = [max(weights_by_date[d]) for d in sorted_dates]
    avg_weights = [statistics.mean(weights_by_date[d]) for d in sorted_dates]

    chart = pygal.Line()
    chart.title = f"Weight Stats Over Time: {exercise_name}"
    chart.x_labels = sorted_dates
    chart.add("Min Weight", min_weights)
    chart.add("Max Weight", max_weights)
    chart.add("Avg Weight", avg_weights)

    output_dir = os.path.join("output", "weight_stats")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{safe_filename(exercise_name)}.svg")
    chart.render_to_file(output_file)
    print(f"Saved weight stats chart to {output_file}")
