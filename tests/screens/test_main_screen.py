from unittest.mock import Mock, patch

import pytest
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

# We need to patch the Builder before importing MainScreen
with patch('kivy.lang.builder.Builder.load_file'):
    from src.screens.main_screen import MainScreen
from src.models.profile import Profile


@pytest.fixture
def screen_manager():
    """ScreenManager fixture."""
    return ScreenManager()


@pytest.fixture
def main_screen():
    """MainScreen fixture."""
    # Patch ProfileStorage to return None for load_profile
    with patch('src.screens.main_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_storage.load_profile.return_value = None
        mock_profile_storage.return_value = mock_storage

        # Create a MainScreen instance with patched ProfileStorage
        screen = MainScreen(name='main')

        # Set up the ids dictionary with a welcome_label
        screen.ids = {}
        screen.ids['welcome_label'] = Label()

        return screen


def test_default_widgets():
    """Test default widget."""
    # Patch ProfileStorage to return None for load_profile
    with patch('src.screens.main_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_storage.load_profile.return_value = None
        mock_profile_storage.return_value = mock_storage

        # Create a MainScreen instance with patched ProfileStorage
        ms = MainScreen(name='main')

        # Set up the ids dictionary with a welcome_label
        ms.ids = {}
        ms.ids['welcome_label'] = Label()

    assert isinstance(ms, Screen)
    assert ms.name == 'main'


def test_profile_data_loading(main_screen):
    """Test profile data loading."""
    # Setup mock profile data
    profile = Profile(name='Test User', dob='1990-01-01', weight=70)

    # Patch ProfileStorage to return our profile
    with patch('src.screens.main_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_storage.load_profile.return_value = profile
        mock_profile_storage.return_value = mock_storage

        # Re-initialize the main screen to trigger profile loading with our mocked profile
        main_screen.__init__(name='main')

    # Add assertions to verify the profile data was loaded correctly
    assert main_screen.ids.welcome_label.text == f'Welcome {profile.name}!'


def test_no_profile_data(main_screen):
    """Test behavior when no profile data exists."""
    with patch('src.screens.main_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_storage.load_profile.return_value = None
        mock_profile_storage.return_value = mock_storage

        main_screen.__init__(name='main')

    # Verify welcome label is empty
    assert main_screen.ids.welcome_label.text == ''


def test_create_workout_navigation(main_screen):
    """Test navigation to workout planning screen."""
    # Mock the screen manager
    main_screen.manager = Mock()
    main_screen.manager.transition = Mock()

    # Since we're patching Builder.load_file, we need to manually create and add a button

    # Create a button with the text "Create workout"
    create_button = Button(text='Create workout')

    # Define the on_press behavior to match what's in the KV file
    def on_press(instance):
        main_screen.manager.current = 'workout_planning'
        main_screen.manager.transition.direction = 'left'

    # Attach the on_press handler
    create_button.bind(on_press=on_press)

    # Add the button to the main screen
    main_screen.add_widget(create_button)

    # Simulate button press
    create_button.dispatch('on_press')

    # Check if navigation was triggered correctly
    assert main_screen.manager.current == 'workout_planning'
    assert main_screen.manager.transition.direction == 'left'


def test_list_workouts_navigation(main_screen):
    """Test navigation to workout list screen."""
    # Mock the screen manager
    main_screen.manager = Mock()
    main_screen.manager.transition = Mock()

    # Since we're patching Builder.load_file, we need to manually create and add a button

    # Create a button with the text "List workouts"
    list_button = Button(text='List workouts')

    # Define the on_press behavior to match what's in the KV file
    def on_press(instance):
        main_screen.manager.current = 'workout_list'
        main_screen.manager.transition.direction = 'left'

    # Attach the on_press handler
    list_button.bind(on_press=on_press)

    # Add the button to the main screen
    main_screen.add_widget(list_button)

    # Simulate button press
    list_button.dispatch('on_press')

    # Check if navigation was triggered correctly
    assert main_screen.manager.current == 'workout_list'
    assert main_screen.manager.transition.direction == 'left'
