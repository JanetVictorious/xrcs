# pylint: disable=attribute-defined-outside-init

import argparse
import logging

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .utils.storage import ProfileStorage
from .views.main_screen import MainScreen
from .views.profile_screen import ProfileScreen
from .views.workout_list_screen import WorkoutListScreen
from .views.workout_planning_screen import WorkoutPlanningScreen


class ExerciseApp(App):
    """Exercise app class."""

    def build(self):
        """Build application UI."""
        self.storage = ProfileStorage()
        self.sm = ScreenManager()

        # Add screens
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(WorkoutPlanningScreen(name='workout_planning'))
        self.sm.add_widget(WorkoutListScreen(name='workout_list'))

        # Set initial screen based on profile existence
        self.sm.current = 'main' if self.storage.profile_exists() else 'profile'

        return self.sm


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Exercise app')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )

    # Run application
    ExerciseApp().run()
