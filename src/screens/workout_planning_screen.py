from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from ..models.exercise import Exercise, Workout
from ..storage.storage import ExerciseStorage, WorkoutStorage

Builder.load_file('screens/screens.kv')


class ExerciseInput(TextInput):
    """Custom exercise input with dropdown suggestions."""

    def __init__(self, exercise_storage: ExerciseStorage, **kwargs):
        """Initialize exercise input."""
        super().__init__(
            multiline=False,
            hint_text='Exercise Name',
            size_hint_x=0.35,
            write_tab=False,
            **kwargs,
        )
        self.exercise_storage = exercise_storage
        self.dropdown = None
        # Only bind to text changes, not focus
        self.bind(text=self._on_text)  # pylint: disable=no-member

    def _create_dropdown(self):
        """Create new dropdown instance."""
        from kivy.uix.dropdown import DropDown

        if self.dropdown:
            self.dropdown.dismiss()
        self.dropdown = DropDown()

    def _update_dropdown(self, text: str = ''):
        """Update dropdown suggestions."""
        # Don't create dropdown for empty text
        if not text:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            return

        self._create_dropdown()
        exercises = self.exercise_storage.load_exercises() or []

        # If no exercises, don't show dropdown
        if not exercises:
            return

        filtered = [ex for ex in exercises if text.lower() in ex.lower()]

        # If no matches, don't show dropdown
        if not filtered:
            return

        # Create button for each filtered exercise
        for exercise in filtered[:5]:  # Limit to 5 suggestions
            btn = Button(
                text=exercise,
                size_hint_y=None,
                height=30,
            )
            # Fix the lambda to capture the current value
            btn.bind(on_release=lambda btn, ex=exercise: self._select_exercise(ex))  # pylint: disable=no-member
            self.dropdown.add_widget(btn)  # type: ignore

    def _on_text(self, instance, value):  # pylint: disable=unused-argument
        """Handle text change event."""
        # Only update dropdown when we have text
        if value and self.focus:
            self._update_dropdown(value)
            if self.dropdown and self.dropdown.children:
                self.dropdown.open(self)
        elif self.dropdown:
            self.dropdown.dismiss()

    def _select_exercise(self, exercise):
        """Select exercise from dropdown."""
        self.text = exercise
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None


class WorkoutPlanningScreen(Screen):
    """Workout planning screen.

    This class is responsible for the workout planning screen.
    The screen allows the user to create a new workout by adding exercises.
    """

    def __init__(self, **kwargs):
        """Initialize workout planning screen.

        During initialization, the screen creates an instance of the exercise and workout storage
        and initializes the list of exercise rows.
        """
        super().__init__(**kwargs)
        Logger.info('Starting workout planning screen')
        self.exercise_storage = ExerciseStorage()
        self.workout_storage = WorkoutStorage()
        self.exercise_rows = []

        self.add_exercise_input(None)

    def add_exercise_input(self, instance):  # pylint: disable=unused-argument
        """Add exercise input fields.

        Create a new row with input fields for exercise name, sets, reps, and weight.
        """
        Logger.info('Adding exercise')
        exercise_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        inputs = {
            'name': ExerciseInput(exercise_storage=self.exercise_storage),
            'sets': TextInput(
                multiline=False,
                hint_text='Sets',
                size_hint_x=0.15,
                input_filter='int',
                write_tab=False,
            ),
            'reps': TextInput(
                multiline=False,
                hint_text='Reps',
                size_hint_x=0.15,
                input_filter='int',
                write_tab=False,
            ),
            'weight': TextInput(
                multiline=False,
                hint_text='Weight (kg)',
                size_hint_x=0.15,
                input_filter='float',
                write_tab=False,
            ),
        }

        for _, input_field in inputs.items():
            exercise_box.add_widget(input_field)

        # Remove button
        remove_btn = Button(
            text='X',
            size_hint_x=0.1,
            background_color=(1, 0, 0, 1),
        )
        remove_btn.bind(on_press=lambda x: self.remove_row(exercise_box))  # pylint: disable=no-member
        exercise_box.add_widget(remove_btn)

        self.ids.exercise_layout.add_widget(exercise_box)
        self.exercise_rows.append(exercise_box)
        Logger.info(self.exercise_rows)

    def remove_row(self, row: BoxLayout):
        """Remove exercise row.

        Remove the given exercise row from the screen.

        Args:
            row: Exercise row to remove.
        """
        if len(self.exercise_rows) > 1:
            Logger.info('Removing exercise row')
            self.exercise_rows.remove(row)
            self.ids.exercise_layout.remove_widget(row)
            Logger.info(self.exercise_rows)
        else:
            Logger.warning('Cannot remove last remaining exercise row')

    def save_workout(self, instance):  # pylint: disable=unused-argument
        """Save workout.

        Saves the workout with the given name and exercises to the database.
        """
        Logger.info('Saving workout...')

        # Validate workout name
        if not self.ids.workout_name.text:
            self._show_error_popup('Workout name is required')
            return

        # Validate exercises
        exercises = []
        invalid_rows = []

        for idx, row in enumerate(self.exercise_rows):
            try:
                inp_row = {
                    'name': row.children[4].text,
                    'sets': int(row.children[3].text),
                    'reps': int(row.children[2].text),
                    'weight': float(row.children[1].text) if row.children[1].text else None,
                }

                # Skip rows with empty name
                if not inp_row['name']:
                    continue

                Logger.info('Exercise %d: %s', idx, inp_row)

                # Create exercise with validated input
                exercise = Exercise(**inp_row)
                exercises.append(exercise)
                Logger.debug('Successfully processed row %s', idx + 1)

                # Add exercise to database
                self.exercise_storage.save_exercise(exercise_name=exercise.name)

            except (ValueError, IndexError) as e:
                Logger.error('Invalid input for row %s: %s', idx + 1, e)
                invalid_rows.append(idx + 1)

        if invalid_rows:
            self._show_error_popup(f'Invalid input in rows: {", ".join(map(str, invalid_rows))}')
            return

        if not exercises:
            self._show_error_popup('No valid exercises added')
            return

        # Create workout model
        workout = Workout(
            name=self.ids.workout_name.text,
            exercises=exercises,
        )

        # Save workout
        self.workout_storage.save_workout(workout)

        # Clear inputs
        self.clear_inputs()

        # Return to main screen
        self.manager.current = 'main'

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
            size=(400, 400),
        )

        # Bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)  # pylint: disable=no-member

        # Open the popup
        popup.open()

    def clear_inputs(self):
        """Clear all inputs after saving."""
        Logger.debug('Clearing all inputs')
        self.ids.workout_name.text = ''
        self.ids.exercise_layout.clear_widgets()
        self.exercise_rows.clear()
