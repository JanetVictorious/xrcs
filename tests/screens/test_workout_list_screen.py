from unittest.mock import Mock, patch

import pytest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

# We need to patch the Builder before importing WorkoutListScreen
with patch('kivy.lang.builder.Builder.load_file'):
    from src.screens.workout_list_screen import WorkoutListScreen


@pytest.fixture
def screen_manager():
    """ScreenManager fixture."""
    return ScreenManager()


@pytest.fixture
def workout_list_screen():
    """WorkoutListScreen fixture."""
    # Patch WorkoutStorage
    with patch('src.screens.workout_list_screen.WorkoutStorage') as mock_workout_storage:
        mock_storage = Mock()
        # Return None instead of empty list to match the actual implementation
        mock_storage.load_workouts.return_value = None
        mock_workout_storage.return_value = mock_storage

        # Patch refresh_workouts to prevent it from being called during initialization
        with patch('src.screens.workout_list_screen.WorkoutListScreen.refresh_workouts'):
            # Create a WorkoutListScreen instance with patched WorkoutStorage
            screen = WorkoutListScreen(name='workout_list')

            # Set up the ids dictionary with required widgets
            screen.ids = {}
            screen.ids['workout_grid'] = Mock()

            return screen


def test_default_widgets():
    """Test default widget initialization."""
    # Patch WorkoutStorage
    with patch('src.screens.workout_list_screen.WorkoutStorage') as mock_workout_storage:
        mock_storage = Mock()
        # Return None instead of empty list to match the actual implementation
        mock_storage.load_workouts.return_value = None
        mock_workout_storage.return_value = mock_storage

        # Patch refresh_workouts to prevent it from being called during initialization
        with patch('src.screens.workout_list_screen.WorkoutListScreen.refresh_workouts'):
            # Create a WorkoutListScreen instance with patched WorkoutStorage
            wls = WorkoutListScreen(name='workout_list')

            # Set up the ids dictionary with required widgets
            wls.ids = {}
            wls.ids['workout_grid'] = Mock()

    assert isinstance(wls, Screen)
    assert wls.name == 'workout_list'


def test_create_workout_item(workout_list_screen):
    """Test creation of a workout item widget."""
    # Sample workout data matching the expected format in the implementation
    workout = {
        'name': 'Test Workout',
        'date': '2023-01-01',
        'exercises': [
            {'name': 'Squat', 'sets': 3, 'reps': 10, 'weight': 100},
            {'name': 'Bench Press', 'sets': 3, 'reps': 8, 'weight': 80},
        ],
    }

    # Create workout item
    item = workout_list_screen.create_workout_item(workout)

    # Verify the item structure
    assert isinstance(item, BoxLayout)
    assert item.orientation == 'vertical'
    assert item.height == 100

    # Check that the item has 3 children (header, details, separator)
    assert len(item.children) == 3

    # The children are in reverse order due to Kivy's layout system
    # So the header is the last child, details is the middle, and separator is the first
    header = item.children[2]
    assert isinstance(header, BoxLayout)
    assert len(header.children) == 2  # name and date labels

    # Check that the exercise details are included
    details = item.children[1]
    assert isinstance(details, Label)
    assert 'Squat: 3x10 (100 kg)' in details.text
    assert 'Bench Press: 3x8 (80 kg)' in details.text


def test_refresh_workouts_with_data(workout_list_screen):
    """Test refreshing workout list with workout data."""
    # Sample workout data
    workouts = [
        {
            'name': 'Workout 1',
            'date': '2023-01-02',
            'exercises': [{'name': 'Exercise 1', 'sets': 3, 'reps': 10, 'weight': 100}],
        },
        {
            'name': 'Workout 2',
            'date': '2023-01-01',
            'exercises': [{'name': 'Exercise 2', 'sets': 4, 'reps': 8, 'weight': 80}],
        },
    ]

    # Mock the storage to return our sample workouts
    workout_list_screen.storage.load_workouts.return_value = workouts

    # Mock the create_workout_item method to return a simple widget
    workout_list_screen.create_workout_item = Mock(return_value=BoxLayout())

    # Call refresh_workouts
    workout_list_screen.refresh_workouts()

    # Verify the workout grid was cleared
    workout_list_screen.ids.workout_grid.clear_widgets.assert_called_once()

    # Verify create_workout_item was called for each workout
    assert workout_list_screen.create_workout_item.call_count == 2

    # Verify workouts were sorted by date (most recent first)
    # First call should be with Workout 1 (2023-01-02)
    assert workout_list_screen.create_workout_item.call_args_list[0][0][0] == workouts[0]
    # Second call should be with Workout 2 (2023-01-01)
    assert workout_list_screen.create_workout_item.call_args_list[1][0][0] == workouts[1]

    # Verify the workout items were added to the grid
    assert workout_list_screen.ids.workout_grid.add_widget.call_count == 2


def test_refresh_workouts_no_data(workout_list_screen):
    """Test refreshing workout list with no workout data."""
    # Mock the storage to return None (which is what the actual implementation returns)
    workout_list_screen.storage.load_workouts.return_value = None

    # Call refresh_workouts
    workout_list_screen.refresh_workouts()

    # Verify the workout grid was cleared
    workout_list_screen.ids.workout_grid.clear_widgets.assert_called_once()

    # Verify a "No workouts found" label was added
    workout_list_screen.ids.workout_grid.add_widget.assert_called_once()
    added_widget = workout_list_screen.ids.workout_grid.add_widget.call_args[0][0]
    assert isinstance(added_widget, Label)
    assert added_widget.text == 'No workouts found'


def test_on_enter(workout_list_screen):
    """Test on_enter method refreshes workouts."""
    # Mock the refresh_workouts method
    workout_list_screen.refresh_workouts = Mock()

    # Call on_enter
    workout_list_screen.on_enter()

    # Verify refresh_workouts was called
    workout_list_screen.refresh_workouts.assert_called_once()


def test_workout_with_missing_weight(workout_list_screen):
    """Test creation of a workout item with missing weight."""
    # Sample workout data with missing weight
    workout = {
        'name': 'Test Workout',
        'date': '2023-01-01',
        'exercises': [
            {'name': 'Bodyweight Exercise', 'sets': 3, 'reps': 10}  # No weight specified
        ],
    }

    # Create workout item
    item = workout_list_screen.create_workout_item(workout)

    # Check that the exercise details handle missing weight
    details = item.children[1]  # Details is the middle child
    assert isinstance(details, Label)
    assert 'Bodyweight Exercise: 3x10 (None kg)' in details.text
