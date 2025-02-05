from pydantic import BaseModel, PositiveFloat, PositiveInt

# from datetime import datetime


class Exercise(BaseModel):
    """Exercise model class."""

    name: str
    sets: PositiveInt
    reps: PositiveInt
    weight: PositiveFloat | None = None
    notes: str | None = None


class Workout(BaseModel):
    """Workout model class."""

    exercises: list[Exercise]
    # date: datetime
    name: str
    notes: str | None = None
