from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator


class Profile(BaseModel):
    """User profile model.

    The model is used to create a user profile.
    """

    name: str
    age: PositiveInt
    weight: PositiveFloat | PositiveInt

    @model_validator(mode='after')
    def weight_to_float(self) -> 'Profile':
        """Convert weight to float."""
        if isinstance(self.weight, int):
            self.weight = float(self.weight)
        return self
