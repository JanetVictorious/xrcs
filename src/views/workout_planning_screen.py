import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from ..models.exercise import Exercise, Workout
from ..utils.storage import WorkoutStorage


class WorkoutPlanningScreen(Screen):
    """Workout planning screen class."""

    def __init__(self, **kwargs):
        """Initialize the workout screen."""
        super().__init__(**kwargs)
        logging.info('Initializing workout screen')
        self.storage = WorkoutStorage()
        self.exercise_rows = []
        self._init_ui()

        # Add initial exercise row
        self.add_exercise_input(None)
        logging.debug('Initial exercise rows count: %s', self.exercise_rows)

    def _init_ui(self):
        """Initialize UI components."""
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Workout name section
        name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        name_layout.add_widget(Label(text='Workout Name:', size_hint_x=0.3))
        self.workout_name = TextInput(multiline=False, hint_text='Enter workout name', size_hint_x=0.7)
        name_layout.add_widget(self.workout_name)

        # Exercise section header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        header.add_widget(Label(text='Name:', size_hint_x=0.35))
        header.add_widget(Label(text='Sets:', size_hint_x=0.15))
        header.add_widget(Label(text='Reps:', size_hint_x=0.15))
        header.add_widget(Label(text='Weight:', size_hint_x=0.15))
        header.add_widget(Label(text='', size_hint_x=0.1))  # Empty space for remove button

        # Exercise container
        self.exercise_layout = BoxLayout(orientation='vertical', spacing=5)

        # Control buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        add_button = Button(text='Add Exercise')
        add_button.bind(on_press=self.add_exercise_input)  # pylint: disable=no-member

        # remove_button = Button(text='Remove Exercise')
        # remove_button.bind(on_press=self.remove_exercise_input)

        save_button = Button(text='Save Workout')
        save_button.bind(on_press=self.save_workout)  # pylint: disable=no-member

        button_layout.add_widget(add_button)
        # button_layout.add_widget(remove_button)
        button_layout.add_widget(save_button)

        # Add components to main layout
        self.main_layout.add_widget(name_layout)
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(self.exercise_layout)
        self.main_layout.add_widget(button_layout)

        self.add_widget(self.main_layout)

    def add_exercise_input(self, instance):  # pylint: disable=unused-argument
        """Add exercise input fields."""
        logging.debug('Adding exercise row. Current count: %s', len(self.exercise_rows))
        exercise_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)

        # Create input fields without focus binding
        logging.debug('Creating exercise input fields')
        inputs = {
            'name': TextInput(
                multiline=False,
                hint_text='Exercise Name',
                size_hint_x=0.35,
                write_tab=False,
            ),
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

        # Add all widgets to exercise box
        for field_name, input_field in inputs.items():
            logging.debug('Adding %s input to exercise row', field_name)
            exercise_box.add_widget(input_field)

        # Remove button
        remove_btn = Button(
            text='X',
            size_hint_x=0.1,
            background_color=(1, 0, 0, 1),
        )
        remove_btn.bind(on_press=lambda x: self.remove_specific_row(exercise_box))  # pylint: disable=no-member
        exercise_box.add_widget(remove_btn)

        self.exercise_layout.add_widget(exercise_box)
        self.exercise_rows.append(exercise_box)
        logging.info('Added new exercise row. Total rows: %s', len(self.exercise_rows))

    def remove_specific_row(self, row):
        """Remove specific exercise row."""
        logging.debug('Attempting to remove row. Current count: %s', len(self.exercise_rows))
        if len(self.exercise_rows) > 1:
            self.exercise_rows.remove(row)
            self.exercise_layout.remove_widget(row)
            logging.info('Removed exercise row. Remaining rows: %s', len(self.exercise_rows))
        else:
            logging.warning('Cannot remove last remainin exercise row')

    # def remove_exercise_input(self, instance):
    #     """Remove exercise input fields."""
    #     if len(self.exercise_rows) > 1:
    #         row = self.exercise_rows.pop()
    #         self.exercise_layout.remove_widget(row)

    def save_workout(self, instance):  # pylint: disable=unused-argument
        """Save workout data."""
        logging.info('Attempting to save workout')
        try:
            if not self.workout_name.text:
                logging.error('Missing workout name')
                raise ValueError('Workout name is required')

            exercises = []
            logging.debug('Processing %s exercise rows', len(self.exercise_rows))

            for idx, row in enumerate(self.exercise_rows):
                # Get all TextInput widgets from row (excluding remove button)
                inputs = [w for w in row.children if isinstance(w, TextInput)]
                logging.debug('Row %s input count: %s', idx + 1, len(inputs))

                try:
                    # Get input fields from the row
                    name = inputs[3].text
                    sets_text = inputs[2].text
                    reps_text = inputs[1].text
                    weight_text = inputs[0].text

                    logging.debug(
                        'Row %s values: name=%s, sets=%s, reps=%s, weight=%s',
                        idx + 1,
                        name,
                        sets_text,
                        reps_text,
                        weight_text,
                    )

                    # Validate required fields
                    if not all([name, sets_text, reps_text]):
                        raise ValueError(
                            f'Incomplete data in row {idx + 1}. Exercise name, sets, and reps are required'
                        )

                    # Create exercise with validated data
                    exercise = Exercise(
                        name=name,
                        sets=int(sets_text),
                        reps=int(reps_text),
                        weight=float(weight_text) if weight_text else None,
                    )
                    exercises.append(exercise)
                    logging.debug('Successfully processed row %s', idx + 1)

                except (ValueError, IndexError) as e:
                    logging.error('Error processing row %s: %s', idx + 1, str(e))
                    raise

            if not exercises:
                raise ValueError('At least one exercise is required in order to save workout')

            workout = Workout(
                name=self.workout_name.text,
                exercises=exercises,
            )

            self.storage.save_workout(workout)
            logging.info('Successfully saved workout %s', workout.name)
            self.clear_inputs()
            self.manager.current = 'main'

        except ValueError as e:
            logging.error('Failed to save workout: %s', str(e))

    def clear_inputs(self):
        """Clear all inputs after saving."""
        logging.debug('Clearing all inputs')
        self.workout_name.text = ''
        self.exercise_layout.clear_widgets()
        self.exercise_rows.clear()
        logging.debug('Adding initial empty row')
        self.add_exercise_input(None)
