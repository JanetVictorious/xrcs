from datetime import date, datetime

from pydantic import BaseModel, PositiveFloat, PositiveInt, field_validator, model_validator


class Profile(BaseModel):
    """User profile model.

    The model is used to create a user profile.
    """

    name: str
    dob: str
    weight: PositiveFloat | PositiveInt
    age: PositiveInt | None = None

    @field_validator('dob')
    @classmethod
    def validate_dob(cls, value):
        """Validate date of birth."""
        try:
            # Check if the date is valid
            datetime.strptime(value, '%Y-%m-%d').date()
            return value
        except Exception as err:
            raise ValueError('Date must be in format YYYY-MM-DD') from err

    @model_validator(mode='after')
    def calculate_age(self) -> 'Profile':
        """Calculate age from date of birth."""
        today = date.today()
        dob = datetime.strptime(self.dob, '%Y-%m-%d').date()
        # Calculate age
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.age = age
        return self

    @model_validator(mode='after')
    def weight_to_float(self) -> 'Profile':
        """Convert weight to float."""
        if isinstance(self.weight, int):
            self.weight = float(self.weight)
        return self
