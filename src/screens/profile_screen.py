from kivy.lang.builder import Builder
from kivy.logger import Logger
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
        profile = Profile(
            name=self.ids.name_input.text,
            age=int(self.ids.age_input.text),
            weight=float(self.ids.weight_input.text),
        )

        Logger.info('Instatiated profile : %s', profile.model_dump())

        # Save new profile
        self.storage.save_profile(profile)

        # Move to main screen
        self.manager.current = 'main'
