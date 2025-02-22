from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen

from ..storage.storage import ProfileStorage

Builder.load_file('screens/screens.kv')


class MainScreen(Screen):
    """Main screen class."""

    def __init__(self, **kwargs):
        """Initialize main screen."""
        super().__init__(**kwargs)
        Logger.info('Starting main screen')
        self.storage = ProfileStorage()

        # Load profile data
        profile_data = self.storage.load_profile()
        if profile_data:
            self.ids.welcome_label.text = f'Welcome {profile_data["name"]}!'
