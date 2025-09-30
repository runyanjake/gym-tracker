import csv
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SetEntry:
    set_number: int
    reps: int
    weight: str  # allow text like "bodyweight" or "body+15"


@dataclass
class ExerciseEntry:
    name: str
    sets: List[SetEntry]


@dataclass
class Session:
    date: str  # ISO format "YYYY-MM-DD"
    exercises: List[ExerciseEntry]
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None


def write_sessions_to_csv(sessions: List[Session], filename: str):
    """Write sessions to a flattened CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["date", "exercise", "set_number", "reps", "weight", "tags", "notes"]
        )

        for session in sessions:
            for ex in session.exercises:
                for s in ex.sets:
                    writer.writerow(
                        [
                            session.date,
                            ex.name,
                            s.set_number,
                            s.reps,
                            s.weight,
                            ",".join(session.tags),
                            session.notes or "",
                        ]
                    )


def read_sessions_from_csv(filename: str) -> List[Session]:
    """Read sessions back from CSV into memory."""
    sessions: dict[str, Session] = {}

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["date"]
            if date not in sessions:
                sessions[date] = Session(
                    date=date,
                    exercises=[],
                    tags=row["tags"].split(",") if row["tags"] else [],
                    notes=row["notes"] or None,
                )
            session = sessions[date]

            # Find or create exercise
            ex_name = row["exercise"]
            exercise = next((e for e in session.exercises if e.name == ex_name), None)
            if not exercise:
                exercise = ExerciseEntry(name=ex_name, sets=[])
                session.exercises.append(exercise)

            # Add set
            set_entry = SetEntry(
                set_number=int(row["set_number"]),
                reps=int(row["reps"]),
                weight=row["weight"],
            )
            exercise.sets.append(set_entry)

    return list(sessions.values())
