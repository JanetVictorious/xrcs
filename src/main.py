from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .screens.main_screen import MainScreen
from .screens.profile_screen import ProfileScreen
from .screens.workout_list_screen import WorkoutListScreen
from .screens.workout_planning_screen import WorkoutPlanningScreen
from .storage.storage import ProfileStorage


class ExerciseApp(App):
    """Exercise app class.

    The class is the main application class. It is responsible for building the
    application UI and running the application.
    """

    def build(self):
        """Build application UI.

        The method creates a screen manager and add all screens to it.
        The screen manager is then returned as the root widget.
        """
        self.storage = ProfileStorage()  # pylint: disable=attribute-defined-outside-init
        sm = ScreenManager()

        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(WorkoutPlanningScreen(name='workout_planning'))
        sm.add_widget(WorkoutListScreen(name='workout_list'))

        sm.current = 'main' if self.storage.profile_exists() else 'profile'

        return sm


if __name__ == '__main__':
    # Run application
    ExerciseApp().run()
