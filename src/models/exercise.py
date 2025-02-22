from datetime import date, datetime

from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator


class Exercise(BaseModel):
    """Exercise model.

    The model takes an exercise name, sets, reps, and weight as input.
    """

    name: str
    sets: PositiveInt
    reps: PositiveInt
    weight: PositiveFloat | None = None


class Workout(BaseModel):
    """Workout model.

    The model takes a list of exercises, a name, and optional date, datetime, and notes as input.
    """

    exercises: list[Exercise]
    name: str
    date: str | None = None
    datetime: str | None = None
    notes: str | None = None

    @model_validator(mode='after')
    def set_dates(self) -> 'Workout':
        """Set date and datetime fields."""
        self.date = date.today().isoformat()
        self.datetime = datetime.now().isoformat()
        return self
