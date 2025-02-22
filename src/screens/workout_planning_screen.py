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
        # self.dropdown = None
        # self.bind(focus=self._on_focus)
        # self.bind(text=self._on_text)

    # def _create_dropdown(self):
    #     """Create new dropdown instance."""
    #     if self.dropdown:
    #         self.dropdown.dismiss()
    #     else:
    #         self.dropdown = DropDown()

    # def _update_dropdown(self, text: str = ''):
    #     """Update dropdown suggestions."""
    #     self._create_dropdown()
    #     exercises = self.exercise_storage.load_exercises() or []
    #     filtered = [ex for ex in exercises if text.lower() in ex.lower()]

    #     # Create button for each filtered exercise
    #     for exercise in filtered:
    #         btn = Button(
    #             text=exercise,
    #             size_hint_y=None,
    #             height=30,
    #         )

    #         btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
    #         self.dropdown.add_widget(btn)

    # def _on_focus(self, instance, value):
    #     """Handle focus event."""
    #     if value:
    #         self._update_dropdown(self.text)
    #         if self.dropdown:
    #             self.dropdown.open(self)
    #     else:
    #         if self.dropdown:
    #             self.dropdown.dismiss()

    # def _on_text(self, instance, value):
    #     """Handle text change event."""
    #     self._update_dropdown(value)
    #     if self.focus and self.dropdown and self.dropdown.children:
    #         self.dropdown.open(self)

    # def _select_exercise(self, exercise):
    #     """Select exercise from dropdown."""
    #     self.text = exercise
    #     if self.dropdown:
    #         self.dropdown.dismiss()

    # def keyboard_on_key_down(self, window, keycode, text, modifiers):
    #     """Handle keyboard input."""
    #     if keycode[1] == 'enter':
    #         self.dropdown.dismiss()
    #         return True
    #     return super().keyboard_on_key_down(window, keycode, text, modifiers)


class WorkoutPlanningScreen(Screen):
    """Workout planning screen."""

    def __init__(self, **kwargs):
        """Initialize workout planning screen."""
        super().__init__(**kwargs)
        Logger.info('Starting workout planning screen')
        self.exercise_storage = ExerciseStorage()
        self.workout_storage = WorkoutStorage()
        self.exercise_rows = []

        self.add_exercise_input(None)

    def add_exercise_input(self, instance):  # pylint: disable=unused-argument
        """Add exercise input fields."""
        Logger.info('Adding exercise')
        exercise_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        inputs = {
            # 'name': TextInput(
            #     multiline=False,
            #     hint_text='Exercise Name',
            #     size_hint_x=0.35,
            #     write_tab=False,
            # ),
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

    def remove_row(self, row):
        """Remove row."""
        if len(self.exercise_rows) > 1:
            Logger.info('Removing exercise row')
            self.exercise_rows.remove(row)
            self.ids.exercise_layout.remove_widget(row)
            Logger.info(self.exercise_rows)
        else:
            Logger.warning('Cannot remove last remaining exercise row')

    def save_workout(self, instance):  # pylint: disable=unused-argument
        """Save workout."""
        Logger.info('Saving workout...')

        if not self.ids.workout_name.text:
            Logger.error('Missing workout name')

            # Create content and add to the popup
            content = Button(
                text='Close',
                size_hint_y=0.1,
            )
            popup = Popup(
                title='Workout name is required',
                content=content,
                auto_dismiss=False,
                size_hint=(None, None),
                size=(400, 400),
            )

            # Bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)  # pylint: disable=no-member

            # Open the popup
            popup.open()

            return

        exercises = []
        for idx, row in enumerate(self.exercise_rows):
            try:
                inp_row = {
                    'name': row.children[4].text,
                    'sets': int(row.children[3].text),
                    'reps': int(row.children[2].text),
                    'weight': float(row.children[1].text),
                }
                Logger.info('Exercise %d: %s', idx, inp_row)

                # Create exercise with validated input
                exercise = Exercise(**inp_row)
                exercises.append(exercise)
                Logger.debug('Successfully processed row %s', idx + 1)

                # Add exercise to database
                self.exercise_storage.save_exercise(exercise_name=exercise.name)

            except (ValueError, IndexError) as e:
                Logger.error('Invalid input for row %s: %s', idx + 1, e)

        if not exercises:
            Logger.warning('No exercises added')
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

    def clear_inputs(self):
        """Clear all inputs after saving."""
        Logger.debug('Clearing all inputs')
        self.ids.workout_name.text = ''
        self.ids.exercise_layout.clear_widgets()
        self.exercise_rows.clear()
