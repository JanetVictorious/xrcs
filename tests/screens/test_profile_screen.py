from unittest.mock import Mock, patch

import pytest
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

# We need to patch the Builder before importing ProfileScreen
with patch('kivy.lang.builder.Builder.load_file'):
    from src.screens.profile_screen import ProfileScreen
from src.models.profile import Profile


@pytest.fixture
def screen_manager():
    """ScreenManager fixture."""
    return ScreenManager()


@pytest.fixture
def profile_screen():
    """ProfileScreen fixture."""
    # Patch ProfileStorage
    with patch('src.screens.profile_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create a ProfileScreen instance with patched ProfileStorage
        screen = ProfileScreen(name='profile')

        # Set up the ids dictionary with required inputs
        screen.ids = {}
        screen.ids['name_input'] = TextInput()
        screen.ids['dob_input'] = TextInput()
        screen.ids['weight_input'] = TextInput()

        return screen


def test_default_widgets():
    """Test default widget initialization."""
    # Patch ProfileStorage
    with patch('src.screens.profile_screen.ProfileStorage') as mock_profile_storage:
        mock_storage = Mock()
        mock_profile_storage.return_value = mock_storage

        # Create a ProfileScreen instance with patched ProfileStorage
        ps = ProfileScreen(name='profile')

        # Set up the ids dictionary with required inputs
        ps.ids = {}
        ps.ids['name_input'] = TextInput()
        ps.ids['dob_input'] = TextInput()
        ps.ids['weight_input'] = TextInput()

    assert isinstance(ps, Screen)
    assert ps.name == 'profile'


def test_save_profile_success(profile_screen):
    """Test successful profile saving."""
    # Set up test data
    profile_screen.ids['name_input'].text = 'Test User'
    profile_screen.ids['dob_input'].text = '1990-01-01'
    profile_screen.ids['weight_input'].text = '70'

    # Mock the screen manager
    profile_screen.manager = Mock()

    # Call the save_profile method
    profile_screen.save_profile(None)

    # Verify profile was saved
    profile_screen.storage.save_profile.assert_called_once()

    # Verify the saved profile data
    saved_profile = profile_screen.storage.save_profile.call_args[0][0]
    assert isinstance(saved_profile, Profile)
    assert saved_profile.name == 'Test User'
    assert saved_profile.dob == '1990-01-01'
    assert saved_profile.weight == 70.0

    # Verify navigation to main screen
    assert profile_screen.manager.current == 'main'


def test_save_profile_missing_name(profile_screen):
    """Test profile saving with missing name."""
    # Set up test data with missing name
    profile_screen.ids['name_input'].text = ''
    profile_screen.ids['dob_input'].text = '1990-01-01'
    profile_screen.ids['weight_input'].text = '70'

    # Mock the _show_error_popup method
    profile_screen._show_error_popup = Mock()

    # Call the save_profile method
    profile_screen.save_profile(None)

    # Verify error popup was shown with correct message
    profile_screen._show_error_popup.assert_called_once_with('Name is required')

    # Verify profile was not saved
    profile_screen.storage.save_profile.assert_not_called()


def test_save_profile_missing_dob(profile_screen):
    """Test profile saving with missing date of birth."""
    # Set up test data with missing dob
    profile_screen.ids['name_input'].text = 'Test User'
    profile_screen.ids['dob_input'].text = ''
    profile_screen.ids['weight_input'].text = '70'

    # Mock the _show_error_popup method
    profile_screen._show_error_popup = Mock()

    # Call the save_profile method
    profile_screen.save_profile(None)

    # Verify error popup was shown with correct message
    profile_screen._show_error_popup.assert_called_once_with('Date of birth is required')

    # Verify profile was not saved
    profile_screen.storage.save_profile.assert_not_called()


def test_save_profile_missing_weight(profile_screen):
    """Test profile saving with missing weight."""
    # Set up test data with missing weight
    profile_screen.ids['name_input'].text = 'Test User'
    profile_screen.ids['dob_input'].text = '1990-01-01'
    profile_screen.ids['weight_input'].text = ''

    # Mock the _show_error_popup method
    profile_screen._show_error_popup = Mock()

    # Call the save_profile method
    profile_screen.save_profile(None)

    # Verify error popup was shown with correct message
    profile_screen._show_error_popup.assert_called_once_with('Weight is required')

    # Verify profile was not saved
    profile_screen.storage.save_profile.assert_not_called()


def test_save_profile_invalid_weight(profile_screen):
    """Test profile saving with invalid weight format."""
    # Set up test data with invalid weight
    profile_screen.ids['name_input'].text = 'Test User'
    profile_screen.ids['dob_input'].text = '1990-01-01'
    profile_screen.ids['weight_input'].text = 'not-a-number'

    # Mock the _show_error_popup method
    profile_screen._show_error_popup = Mock()

    # Call the save_profile method
    profile_screen.save_profile(None)

    # Verify error popup was shown with correct message containing "Invalid input"
    profile_screen._show_error_popup.assert_called_once()
    assert 'Invalid input' in profile_screen._show_error_popup.call_args[0][0]

    # Verify profile was not saved
    profile_screen.storage.save_profile.assert_not_called()


def test_show_error_popup(profile_screen, monkeypatch):
    """Test the error popup creation and display."""
    # Mock Popup class
    mock_popup = Mock(spec=Popup)
    mock_popup_instance = Mock()
    mock_popup.return_value = mock_popup_instance

    # Mock Button class
    mock_button = Mock(spec=Button)
    mock_button_instance = Mock()
    mock_button.return_value = mock_button_instance

    # Apply monkeypatches
    monkeypatch.setattr('src.screens.profile_screen.Popup', mock_popup)
    monkeypatch.setattr('src.screens.profile_screen.Button', mock_button)

    # Call the method
    profile_screen._show_error_popup('Test error message')

    # Verify popup was created with correct parameters
    mock_popup.assert_called_once()
    assert mock_popup.call_args[1]['title'] == 'Test error message'
    assert mock_popup.call_args[1]['auto_dismiss'] is False

    # Verify button was created
    mock_button.assert_called_once()
    assert mock_button.call_args[1]['text'] == 'Close'

    # Verify popup was opened
    mock_popup_instance.open.assert_called_once()

    # Verify button was bound to dismiss the popup
    mock_button_instance.bind.assert_called_once()
    # Check that bind was called with on_press keyword argument
    assert 'on_press' in mock_button_instance.bind.call_args[1]
    # Check that the value passed to on_press is the popup's dismiss method
    assert mock_button_instance.bind.call_args[1]['on_press'] == mock_popup_instance.dismiss
