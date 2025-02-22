from pydantic import BaseModel, PositiveFloat, PositiveInt


class Profile(BaseModel):
    """User profile model.

    The model is used to create a user profile.
    """

    name: str
    age: PositiveInt
    weight: PositiveFloat
