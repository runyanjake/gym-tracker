# main.py
import os
from csv_serializer import read_exercises_from_csv, read_workouts_from_csv
from utilities import group_by_muscle, summarize_progress
from visualization import plot_lifting_volume, plot_total_reps, plot_weight_stats

def main():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    exercises = read_exercises_from_csv("input/exercises.csv")
    workouts = read_workouts_from_csv("input/data.csv", exercises)

    plot_charts(exercises, workouts)
    summarize_progress(workouts)

def plot_charts(exercises, workouts):
    all_exercises = set(
        s.exercise.name
        for w in workouts
        for s in w.exercises
    )

    weighted_exercises = set(
        s.exercise.name
        for w in workouts
        for s in w.exercises
        if s.weight
    )

    non_weighted_exercises = set(
        s.exercise.name
        for w in workouts
        for s in w.exercises
        if not s.weight
    )

    #  Charts for lifting volume (only weighted exercises)
    for exercise_name in weighted_exercises:
        plot_lifting_volume(workouts, exercise_name)

    # Charts for weight tracking over time. (only weighted exercises)
    for exercise_name in weighted_exercises:
        plot_weight_stats(workouts, exercise_name)

    # Charts for rep based exercises (all exercises)
    for exercise_name in all_exercises:
        plot_total_reps(workouts, exercise_name)

    print("Done saving charts!\n")

if __name__ == "__main__":
    main()
