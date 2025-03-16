from unittest.mock import Mock, patch

import pytest
from kivy.uix.screenmanager import Screen, ScreenManager

# We need to patch the Builder before importing ExerciseApp
with patch('kivy.lang.builder.Builder.load_file'):
    from src.main import ExerciseApp


@pytest.fixture
def exercise_app():
    """ExerciseApp fixture."""
    # Patch ProfileStorage
    with patch('src.main.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create an ExerciseApp instance with patched ProfileStorage
        app = ExerciseApp()

        return app


def test_app_initialization():
    """Test app initialization."""
    # Create an ExerciseApp instance
    app = ExerciseApp()

    # Verify app is initialized correctly
    assert isinstance(app, ExerciseApp)


def test_build_creates_screen_manager():
    """Test that build method creates a ScreenManager."""
    # Patch all the imported screen classes
    with (
        patch('src.main.ProfileScreen') as mock_profile_screen,
        patch('src.main.MainScreen') as mock_main_screen,
        patch('src.main.WorkoutPlanningScreen') as mock_workout_planning_screen,
        patch('src.main.WorkoutListScreen') as mock_workout_list_screen,
        patch('src.main.ProfileStorage') as mock_profile_storage,
    ):
        # Create actual Screen instances for our mocks to return
        profile_screen = Screen(name='profile')
        main_screen = Screen(name='main')
        workout_planning_screen = Screen(name='workout_planning')
        workout_list_screen = Screen(name='workout_list')

        # Setup mock screens to return actual Screen instances
        mock_profile_screen.return_value = profile_screen
        mock_main_screen.return_value = main_screen
        mock_workout_planning_screen.return_value = workout_planning_screen
        mock_workout_list_screen.return_value = workout_list_screen

        # Setup mock storage
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create app and call build
        app = ExerciseApp()
        result = app.build()

        # Verify result is a ScreenManager
        assert isinstance(result, ScreenManager)

        # Verify screens were added
        assert mock_profile_screen.called
        assert mock_main_screen.called
        assert mock_workout_planning_screen.called
        assert mock_workout_list_screen.called


def test_build_adds_all_screens():
    """Test that build method adds all screens to the ScreenManager."""
    # Patch all the imported screen classes
    with (
        patch('src.main.ProfileScreen') as mock_profile_screen,
        patch('src.main.MainScreen') as mock_main_screen,
        patch('src.main.WorkoutPlanningScreen') as mock_workout_planning_screen,
        patch('src.main.WorkoutListScreen') as mock_workout_list_screen,
        patch('src.main.ProfileStorage') as mock_profile_storage,
    ):
        # Create actual Screen instances for our mocks to return
        profile_screen = Screen(name='profile')
        main_screen = Screen(name='main')
        workout_planning_screen = Screen(name='workout_planning')
        workout_list_screen = Screen(name='workout_list')

        # Setup mock screens to return actual Screen instances
        mock_profile_screen.return_value = profile_screen
        mock_main_screen.return_value = main_screen
        mock_workout_planning_screen.return_value = workout_planning_screen
        mock_workout_list_screen.return_value = workout_list_screen

        # Setup mock storage
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create app and call build
        app = ExerciseApp()
        sm = app.build()

        # Verify screens were added to the ScreenManager
        assert len(sm.screens) == 4
        assert any(screen.name == 'profile' for screen in sm.screens)
        assert any(screen.name == 'main' for screen in sm.screens)
        assert any(screen.name == 'workout_planning' for screen in sm.screens)
        assert any(screen.name == 'workout_list' for screen in sm.screens)


def test_initial_screen_with_profile():
    """Test that initial screen is 'main' when profile exists."""
    # Patch all the imported screen classes
    with (
        patch('src.main.ProfileScreen') as mock_profile_screen,
        patch('src.main.MainScreen') as mock_main_screen,
        patch('src.main.WorkoutPlanningScreen') as mock_workout_planning_screen,
        patch('src.main.WorkoutListScreen') as mock_workout_list_screen,
        patch('src.main.ProfileStorage') as mock_profile_storage,
    ):
        # Create actual Screen instances for our mocks to return
        profile_screen = Screen(name='profile')
        main_screen = Screen(name='main')
        workout_planning_screen = Screen(name='workout_planning')
        workout_list_screen = Screen(name='workout_list')

        # Setup mock screens to return actual Screen instances
        mock_profile_screen.return_value = profile_screen
        mock_main_screen.return_value = main_screen
        mock_workout_planning_screen.return_value = workout_planning_screen
        mock_workout_list_screen.return_value = workout_list_screen

        # Setup mock storage with profile_exists returning True
        mock_storage = Mock()
        mock_storage.profile_exists.return_value = True
        mock_profile_storage.return_value = mock_storage

        # Create app and call build
        app = ExerciseApp()
        sm = app.build()

        # Verify initial screen is 'main'
        assert sm.current == 'main'


def test_initial_screen_without_profile():
    """Test that initial screen is 'profile' when no profile exists."""
    # Patch all the imported screen classes
    with (
        patch('src.main.ProfileScreen') as mock_profile_screen,
        patch('src.main.MainScreen') as mock_main_screen,
        patch('src.main.WorkoutPlanningScreen') as mock_workout_planning_screen,
        patch('src.main.WorkoutListScreen') as mock_workout_list_screen,
        patch('src.main.ProfileStorage') as mock_profile_storage,
    ):
        # Create actual Screen instances for our mocks to return
        profile_screen = Screen(name='profile')
        main_screen = Screen(name='main')
        workout_planning_screen = Screen(name='workout_planning')
        workout_list_screen = Screen(name='workout_list')

        # Setup mock screens to return actual Screen instances
        mock_profile_screen.return_value = profile_screen
        mock_main_screen.return_value = main_screen
        mock_workout_planning_screen.return_value = workout_planning_screen
        mock_workout_list_screen.return_value = workout_list_screen

        # Setup mock storage with profile_exists returning False
        mock_storage = Mock()
        mock_storage.profile_exists.return_value = False
        mock_profile_storage.return_value = mock_storage

        # Create app and call build
        app = ExerciseApp()
        sm = app.build()

        # Verify initial screen is 'profile'
        assert sm.current == 'profile'


def test_storage_initialization():
    """Test that storage is initialized in build method."""
    # Patch all the imported screen classes and ProfileStorage
    with (
        patch('src.main.ProfileScreen') as mock_profile_screen,
        patch('src.main.MainScreen') as mock_main_screen,
        patch('src.main.WorkoutPlanningScreen') as mock_workout_planning_screen,
        patch('src.main.WorkoutListScreen') as mock_workout_list_screen,
        patch('src.main.ProfileStorage') as mock_profile_storage,
    ):
        # Create actual Screen instances for our mocks to return
        profile_screen = Screen(name='profile')
        main_screen = Screen(name='main')
        workout_planning_screen = Screen(name='workout_planning')
        workout_list_screen = Screen(name='workout_list')

        # Setup mock screens to return actual Screen instances
        mock_profile_screen.return_value = profile_screen
        mock_main_screen.return_value = main_screen
        mock_workout_planning_screen.return_value = workout_planning_screen
        mock_workout_list_screen.return_value = workout_list_screen

        # Setup mock storage
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create app and call build
        app = ExerciseApp()
        app.build()

        # Verify storage was initialized
        assert app.storage is not None
        assert app.storage == mock_storage
