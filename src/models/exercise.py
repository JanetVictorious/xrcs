from datetime import date, datetime

from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator


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
