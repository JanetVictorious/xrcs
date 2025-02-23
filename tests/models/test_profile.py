import pytest
from pydantic import ValidationError

from src.models.profile import Profile


def test_valid_profile():
    """Test valid Profile."""
    name = 'John Doe'
    age = 25
    weight = 75.5

    profile = Profile(name=name, age=age, weight=weight)

    assert profile.name == name
    assert profile.age == age
    assert profile.weight == weight


def test_invalid_profile():
    """Test invalid Profile."""
    with pytest.raises(ValidationError) as e:
        Profile(name=1, age=25, weight=75.5)

    assert 'name' in str(e.value)

    with pytest.raises(ValidationError) as e:
        Profile(name='John Doe', age=-25, weight=75.5)

    assert 'age' in str(e.value)

    with pytest.raises(ValidationError) as e:
        Profile(name='John Doe', age=25, weight=-75)

    assert 'weight' in str(e.value)


def test_weight_to_float():
    """Test weight_to_float_method."""
    profile = Profile(name='John Doe', age=25, weight=75)

    assert isinstance(profile.weight, float)
    assert profile.weight == 75.0
