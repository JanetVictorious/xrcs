from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from ..utils.storage import ProfileStorage


class MainScreen(Screen):
    """Main screen class."""

    def __init__(self, **kwargs):
        """Initialize the main screen."""
        super().__init__(**kwargs)
        self.storage = ProfileStorage()
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = BoxLayout(orientation='vertical', padding=10)
        profile_data = self.storage.load_profile()

        if profile_data:
            welcome_text = f'Welcome {profile_data["name"]}!'
            layout.add_widget(Label(text=welcome_text))

        # Create new workout button
        create_workout_button = Button(text='Create Workout', size_hint_y=None, height=50)
        create_workout_button.bind(on_press=self.create_workout)  # pylint: disable=no-member
        layout.add_widget(create_workout_button)

        # List workouts
        list_workouts_button = Button(text='List Workouts', size_hint_y=None, height=50)
        list_workouts_button.bind(on_press=self.list_workouts)  # pylint: disable=no-member
        layout.add_widget(list_workouts_button)

        self.add_widget(layout)

    def create_workout(self, instance):  # pylint: disable=unused-argument
        """Create a new workout."""
        self.manager.current = 'workout_planning'

    def list_workouts(self, instance):  # pylint: disable=unused-argument
        """List all workouts."""
        self.manager.current = 'workout_list'
