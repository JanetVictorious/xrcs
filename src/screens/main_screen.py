from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen

from ..storage.storage import ProfileStorage

Builder.load_file('screens/screens.kv')


class MainScreen(Screen):
    """xcrs main screen.

    The class is responsible for the main screen of the application.
    """

    def __init__(self, **kwargs):
        """Instantiate main screen and load profile data."""
        super().__init__(**kwargs)
        Logger.info('Starting main screen')
        self.storage = ProfileStorage()

        # Load profile data
        profile_data = self.storage.load_profile()
        if profile_data:
            self.ids.welcome_label.text = f'Welcome {profile_data["name"]}!'
