from datetime import date
from collections import defaultdict
import os

from visualization import plot_time_series
from workout import read_sessions_from_csv

INPUT_DIR = "input"
OUTPUT_DIR = "output"
CSV_FILE = os.path.join(INPUT_DIR, "data.csv")


def compute_lifting_volume(sessions):
    volume_data = defaultdict(list)
    for session in sessions:
        for exercise in session.exercises:
            total_volume = 0
            for s in exercise.sets:
                try:
                    weight = float(s.weight.replace("body+", "").replace("body", "0"))
                    total_volume += weight * s.reps
                except ValueError:
                    continue
            volume_data[exercise.name].append((session.date, total_volume))
    return volume_data


def main():
    # Ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read sessions from CSV
    sessions = read_sessions_from_csv(CSV_FILE)
    print(f"Loaded {len(sessions)} sessions from {CSV_FILE}")

    # Compute volume per exercise
    volume_per_exercise = compute_lifting_volume(sessions)

    # Plot each exercise
    for ex_name, data in volume_per_exercise.items():
        data_sorted = sorted(data, key=lambda x: x[0])
        dates = [date.fromisoformat(d) for d, _ in data_sorted]
        volumes = [v for _, v in data_sorted]

        output_file = os.path.join(
            OUTPUT_DIR, f"{ex_name.replace(' ', '_')}_volume.png"
        )
        plot_time_series(
            x=dates,
            y=volumes,
            output_file=output_file,
            title=f"{ex_name} Lifting Volume Over Time",
            y_label="Total Volume (lbs)",
            line_color="#2ca02c",
        )
        print(f"Saved plot: {output_file}")


if __name__ == "__main__":
    main()

