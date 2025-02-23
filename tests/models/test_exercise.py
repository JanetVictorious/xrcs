from datetime import date, datetime

import pytest
from pydantic import ValidationError

from src.models.exercise import Exercise, Workout


def test_create_valid_exercise():
    """Test valid Exercise."""
    exercise = Exercise(name='Squat', sets=3, reps=10, weight=100.0)
    assert exercise.name == 'Squat'
    assert exercise.sets == 3
    assert exercise.reps == 10
    assert exercise.weight == 100.0


def test_create_exercise_without_weight():
    """Test valid Exercise without weight."""
    exercise = Exercise(name='Push-up', sets=3, reps=10)
    assert exercise.weight is None


def test_invalid_exercise_negative_values():
    """Test invalid Exercise with negative values."""
    with pytest.raises(ValidationError):
        Exercise(name='Squat', sets=-1, reps=10, weight=100.0)
    with pytest.raises(ValidationError):
        Exercise(name='Squat', sets=3, reps=-1, weight=100.0)
    with pytest.raises(ValidationError):
        Exercise(name='Squat', sets=3, reps=10, weight=-100.0)


def test_create_valid_workout():
    """Test valid Workout."""
    exercises = [Exercise(name='Squat', sets=3, reps=10, weight=100.0), Exercise(name='Push-up', sets=3, reps=10)]
    workout = Workout(exercises=exercises, name='Leg Day')
    assert workout.name == 'Leg Day'
    assert len(workout.exercises) == 2
    assert workout.date == date.today().isoformat()
    assert workout.datetime is not None


def test_workout_with_all_fields():
    """Test Workout with all fields."""
    exercises = [Exercise(name='Squat', sets=3, reps=10, weight=100.0)]
    workout = Workout(exercises=exercises, name='Full Workout', notes='Great session')
    assert workout.name == 'Full Workout'
    assert workout.notes == 'Great session'
    assert workout.date == date.today().isoformat()
    assert workout.datetime is not None


def test_invalid_workout_empty_exercises():
    """Test invalid Workout with empty exercises."""
    with pytest.raises(ValidationError):
        Workout(exercises=[], name='Empty Workout')


def test_workout_dates_auto_population():
    """Test auto population of date and datetime fields."""
    exercises = [Exercise(name='Squat', sets=3, reps=10)]
    workout = Workout(exercises=exercises, name='Test Workout')

    assert workout.date == date.today().isoformat()
    assert isinstance(datetime.fromisoformat(workout.datetime), datetime)
