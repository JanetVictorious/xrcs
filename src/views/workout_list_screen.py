import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from ..utils.storage import WorkoutStorage


class WorkoutListScreen(Screen):
    """Workout list screen class."""

    def __init__(self, **kwargs):
        """Initialize the workout list screen."""
        super().__init__(**kwargs)
        logging.info('Initializing workout list screen')
        self.storage = WorkoutStorage()
        self._init_ui()
        self.refresh_workouts()

    def _init_ui(self):
        """Initialize UI components."""
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = Label(text='Workouts', size_hint_y=None, height=50, bold=True)
        self.layout.add_widget(header)

        # Scrollable container for workouts
        scroll = ScrollView()
        self.workout_grid = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=10,
        )
        self.workout_grid.bind(minimum_height=self.workout_grid.setter('height'))  # pylint: disable=no-member
        scroll.add_widget(self.workout_grid)
        self.layout.add_widget(scroll)

        # Back button
        back_button = Button(text='Back', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)  # pylint: disable=no-member
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def create_workout_item(self, workout):
        """Create a widget for a single workout."""
        item = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=5)

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
        logging.info('Refreshing workout list')
        self.workout_grid.clear_widgets()
        workouts = self.storage.load_workouts()

        if not workouts:
            self.workout_grid.add_widget(Label(text='No workouts found', italic=True))
            return

        # Sort workouts by date, newest first
        workouts.sort(key=lambda x: x['date'], reverse=True)

        for workout in workouts:
            self.workout_grid.add_widget(self.create_workout_item(workout))

    def go_back(self, instance):  # pylint: disable=unused-argument
        """Go back to the main screen."""
        self.manager.current = 'main'
