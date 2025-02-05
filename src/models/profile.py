from pydantic import BaseModel, PositiveFloat, PositiveInt


class Profile(BaseModel):
    """User profile model."""

    name: str
    age: PositiveInt
    weight: PositiveFloat
