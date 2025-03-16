from unittest.mock import mock_open, patch

import pytest

from src.models.exercise import Exercise, Workout
from src.models.profile import Profile
from src.storage.storage import ExerciseStorage, ProfileStorage, WorkoutStorage


@pytest.fixture
def profile_storage(tmp_path):
    """ProfileStorage fixture.

    Args:
        tmp_path: A pytest tmp_path fixture.
    """
    storage = ProfileStorage(filename=str(tmp_path / 'test_profile.json'))
    yield storage


@pytest.fixture
def exercise_storage(tmp_path):
    """ExerciseStorage fixture.

    Args:
        tmp_path: A pytest tmp_path fixture.
    """
    storage = ExerciseStorage(filename=str(tmp_path / 'test_exercises.json'))
    yield storage


@pytest.fixture
def workout_storage(tmp_path):
    """WorkoutStorage fixture.

    Args:
        tmp_path: A pytest tmp_path fixture.
    """
    storage = WorkoutStorage(filename=str(tmp_path / 'test_workouts.json'))
    yield storage


def test_profile_storage_save(tmp_path, profile_storage):
    """Test ProfileStorage save method."""
    test_profile = Profile(name='Test User', dob='1990-01-01', weight=70)
    with patch('builtins.open', mock_open()) as mock_file:
        profile_storage.save_profile(profile=test_profile)
        mock_file.assert_called_once_with(str(tmp_path / 'test_profile.json'), 'w', encoding='utf-8')


def test_profile_storage_load_nonexistent(profile_storage):
    """Test ProfileStorage load method with nonexistent file."""
    assert profile_storage.load_profile() is None


def test_profile_storage_load(profile_storage):
    """Test ProfileStorage load method when file exists."""
    test_profile = Profile(name='Test User', dob='1990-01-01', weight=70)
    profile_storage.save_profile(profile=test_profile)
    loaded_profile = profile_storage.load_profile()
    assert loaded_profile.name == test_profile.name
    assert loaded_profile.dob == test_profile.dob
    assert loaded_profile.weight == test_profile.weight


def test_profile_storage_exists(profile_storage):
    """Test ProfileStorage profile_exists method."""
    test_profile = Profile(name='Test User', dob='1990-01-01', weight=70)
    profile_storage.save_profile(profile=test_profile)
    assert profile_storage.profile_exists()


def test_profile_storage_does_not_exists(profile_storage):
    """Test ProfileStorage load method with nonexistent file."""
    assert not profile_storage.profile_exists()


def test_exercise_storage_save(tmp_path, exercise_storage):
    """Test ExerciseStorage save method."""
    with patch('builtins.open', mock_open()) as mock_file:
        exercise_storage.save_exercise('pushup')
        mock_file.assert_called_once_with(str(tmp_path / 'test_exercises.json'), 'w', encoding='utf-8')


def test_exercise_storage_load_nonexistent(exercise_storage):
    """Test ExerciseStorage load method with nonexistent file."""
    assert exercise_storage.load_exercises() is None


def test_exercise_storage_load(exercise_storage):
    """Test ExerciseStorage load method with existing file."""
    # Add exercise
    exercise_storage.save_exercise('pushup')
    loaded_exercises = exercise_storage.load_exercises()
    assert loaded_exercises == ['pushup']

    # Add another exercise
    exercise_storage.save_exercise('snatch')
    loaded_exercises = exercise_storage.load_exercises()
    assert len(loaded_exercises) == 2
    assert 'pushup' in loaded_exercises
    assert 'snatch' in loaded_exercises

    # Add first exercise again
    # Duplicate should not be added
    exercise_storage.save_exercise('pushup')
    loaded_exercises = exercise_storage.load_exercises()
    assert len(loaded_exercises) == 2
    assert 'pushup' in loaded_exercises
    assert 'snatch' in loaded_exercises


def test_workout_storage_save(tmp_path, workout_storage):
    """Test WorkoutStorage save method."""
    test_exercise = Exercise(name='snatch', sets=3, reps=10, weight=70.0)
    test_workout = Workout(exercises=[test_exercise], name='snatch day')
    with patch('builtins.open', mock_open()) as mock_file:
        workout_storage.save_workout(test_workout)
        mock_file.assert_called_once_with(str(tmp_path / 'test_workouts.json'), 'w', encoding='utf-8')


def test_workout_storage_load_nonexistent(workout_storage):
    """Test WorkoutStorage load method with nonexistent file."""
    assert workout_storage.load_workouts() is None


def test_workout_storage_load(workout_storage):
    """Test WorkoutStorage load method with existing file."""
    # Add first workout
    test_exercise = Exercise(name='snatch', sets=3, reps=10, weight=70.0)
    test_workout = Workout(exercises=[test_exercise], name='snatch day')
    workout_storage.save_workout(test_workout)
    loaded_workouts = workout_storage.load_workouts()
    assert len(loaded_workouts) == 1
    assert loaded_workouts[0]['name'] == test_workout.name
    assert loaded_workouts[0]['exercises'][0]['name'] == test_exercise.name
    assert loaded_workouts[0]['exercises'][0]['sets'] == test_exercise.sets
    assert loaded_workouts[0]['exercises'][0]['reps'] == test_exercise.reps
    assert loaded_workouts[0]['exercises'][0]['weight'] == test_exercise.weight
    assert loaded_workouts[0]['date'] == test_workout.date
    assert loaded_workouts[0]['datetime'] == test_workout.datetime

    # Add second workout
    test_exercise = Exercise(name='cleans', sets=3, reps=10, weight=70.0)
    test_workout = Workout(exercises=[test_exercise], name='clean day')
    workout_storage.save_workout(test_workout)
    loaded_workouts = workout_storage.load_workouts()
    assert len(loaded_workouts) == 2
    assert loaded_workouts[1]['name'] == test_workout.name
    assert loaded_workouts[1]['exercises'][0]['name'] == test_exercise.name
    assert loaded_workouts[1]['exercises'][0]['sets'] == test_exercise.sets
    assert loaded_workouts[1]['exercises'][0]['reps'] == test_exercise.reps
    assert loaded_workouts[1]['exercises'][0]['weight'] == test_exercise.weight
    assert loaded_workouts[1]['date'] == test_workout.date
    assert loaded_workouts[1]['datetime'] == test_workout.datetime
