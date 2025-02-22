import json
import os

from ..models.exercise import Workout
from ..models.profile import Profile


class ProfileStorage:
    """Storage class for saving and loading profile data."""

    def __init__(self, filename: str = 'profile.json'):
        """Initialize the storage class."""
        self.filename = filename

    def save_profile(self, profile: Profile) -> None:
        """Save the profile data to the file."""
        with open(self.filename, 'w', encoding='utf-8') as file_:
            json.dump(profile.model_dump(), file_)

    def load_profile(self) -> Profile | None:
        """Load the profile data from the file."""
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, encoding='utf-8') as file_:
            return json.load(file_)

    def profile_exists(self) -> bool:
        """Check if the profile file exists."""
        return os.path.exists(self.filename)


class ExerciseStorage:
    """Storage class for saving and loading exercise data."""

    def __init__(self, filename: str = 'exercises.json'):
        """Initialize the storage class."""
        self.filename = filename

    def save_exercise(self, exercise_name: str) -> None:
        """Save exercise data."""
        exercises = self.load_exercises() or []
        if exercise_name.lower() not in exercises:
            exercises.append(exercise_name.lower())
            with open(self.filename, 'w', encoding='utf-8') as file_:
                json.dump(exercises, file_)

    def load_exercises(self) -> list | None:
        """Load exercise data."""
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, encoding='utf-8') as file_:
            data = json.load(file_)
        return list(data)


class WorkoutStorage:
    """Storage class for saving and loading workout data."""

    def __init__(self, filename: str = 'workouts.json'):
        """Initialize the storage class."""
        self.filename = filename

    def save_workout(self, workout: Workout) -> None:
        """Save workout data."""
        workouts = self.load_workouts() or []
        workouts.append(workout.model_dump())
        with open(self.filename, 'w', encoding='utf-8') as file_:
            json.dump(workouts, file_)

    def load_workouts(self) -> list[dict] | None:
        """Load workout data."""
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, encoding='utf-8') as file_:
            data = json.load(file_)
        return data
