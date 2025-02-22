from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from ..storage.storage import WorkoutStorage

Builder.load_file('screens/screens.kv')


class WorkoutListScreen(Screen):
    """Workout list screen class."""

    def __init__(self, **kwargs):
        """Initialize workout list screen."""
        super().__init__(**kwargs)
        Logger.info('Starting workout list screen')
        self.storage = WorkoutStorage()
        self.refresh_workouts()

    def create_workout_item(self, workout: dict):
        """Create widget for a single workout.

        Args:
            workout: Dict with workout data.
        """
        item = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=100,
            spacing=5,
        )

        # Workout header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        name = Label(text=workout['name'], bold=True, size_hint_x=0.7)
        date = Label(text=workout['date'], size_hint_x=0.3)
        header.add_widget(name)
        header.add_widget(date)

        # Exercise summary
        exercises = '\n'.join(
            [f'{ex["name"]}: {ex["sets"]}x{ex["reps"]} ({ex.get("weight", None)} kg)' for ex in workout['exercises']]
        )
        details = Label(text=exercises, size_hint_y=None, height=70, halign='left')
        details.bind(size=details.setter('text_size'))  # pylint: disable=no-member

        item.add_widget(header)
        item.add_widget(details)

        # Add separator
        item.add_widget(Label(size_hint_y=None, height=1, color=(0.5, 0.5, 0.5, 1)))

        return item

    def refresh_workouts(self):
        """Refresh the workout list."""
        Logger.info('Refreshing workout list')
        self.ids.workout_grid.clear_widgets()
        workouts = self.storage.load_workouts()

        if not workouts:
            self.ids.workout_grid.add_widget(Label(text='No workouts found', italic=True))
            return

        workouts.sort(key=lambda x: x['date'], reverse=True)
        for workout in workouts:
            Logger.info('Workout')
            self.ids.workout_grid.add_widget(self.create_workout_item(workout))
