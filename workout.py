from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class MuscleGroup(Enum):
    LEGS = "Legs", "Exercises targeting the lower extremities."
    CHEST = "Chest", "Exercises targeting the chest."
    BACK = "Back", "Exercises targeting the upper and lower back."
    ARMS = "Arms", "Exercises targeting the arms."
    SHOULDERS = "Shoulders", "Exercises targeting specifically the shoulders."
    CORE = "Core", "Exercises targeting all areas of the abs and core."

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, description: str = None):
        self._description_ = description

    def __str__(self):
        return self.value

    # Makes description read-only
    @property
    def description(self):
        return self._description_

@dataclass
class Exercise:
    name: str
    parent_exercise: Optional["Exercise"]
    muscle_groups: List[MuscleGroup]
    description: str
    form_notes: str
    
@dataclass
class Set:
    exercise: Exercise
    reps: int
    weight: str
    notes: str

@dataclass
class Workout:
    date: str
    exercises: List[Set]
    notes: Optional[str] = None
