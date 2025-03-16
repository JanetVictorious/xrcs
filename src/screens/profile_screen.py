from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from ..models.profile import Profile
from ..storage.storage import ProfileStorage

Builder.load_file('screens/screens.kv')


class ProfileScreen(Screen):
    """Profile screen.

    The class is responsible for the main screen of the application.
    The screen is only shown when the user is starting the application for the
    first time and creates a new profile.
    """

    def __init__(self, **kwargs):
        """Instantiate profile screen."""
        super().__init__(**kwargs)
        Logger.info('Starting profile screen')
        self.storage = ProfileStorage()

    def save_profile(self, instance):  # pylint: disable=unused-argument
        """Save new profile.

        The method is called when the user clicks the save button on the profile screen.
        Once the profile is saved, the user is moved to the main screen.
        """
        try:
            # Validate inputs
            if not self.ids.name_input.text:
                self._show_error_popup('Name is required')
                return

            if not self.ids.dob_input.text:
                self._show_error_popup('Date of birth is required')
                return

            if not self.ids.weight_input.text:
                self._show_error_popup('Weight is required')
                return

            # Create profile
            profile = Profile(
                name=self.ids.name_input.text,
                dob=self.ids.dob_input.text,
                weight=float(self.ids.weight_input.text),
            )

            Logger.info('Instantiated profile: %s', profile.model_dump())

            # Save new profile
            self.storage.save_profile(profile)

            # Move to main screen
            self.manager.current = 'main'

        except ValueError as e:
            self._show_error_popup(f'Invalid input: {str(e)}')

    def _show_error_popup(self, message):
        """Show error popup with the given message."""
        # Create content and add to the popup
        content = Button(
            text='Close',
            size_hint_y=0.1,
        )
        popup = Popup(
            title=message,
            content=content,
            auto_dismiss=False,
            size_hint=(None, None),
            size=(400, 200),
        )

        # Bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)  # pylint: disable=no-member

        # Open the popup
        popup.open()
