from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from ..models.profile import Profile
from ..utils.storage import ProfileStorage


class ProfileScreen(Screen):
    """Profile screen class."""

    def __init__(self, **kwargs):
        """Initialize the profile screen."""
        super().__init__(**kwargs)
        self.storage = ProfileStorage()
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text='Create your profile'))

        self.name_input = TextInput(multiline=False, hint_text='Enter your name')
        self.age_input = TextInput(multiline=False, hint_text='Enter your age')
        self.weight_input = TextInput(multiline=False, hint_text='Enter your weight (kg)')

        layout.add_widget(self.name_input)
        layout.add_widget(self.age_input)
        layout.add_widget(self.weight_input)

        save_button = Button(text='Save Profile')
        save_button.bind(on_press=self.save_profile)  # pylint: disable=no-member
        layout.add_widget(save_button)

        self.add_widget(layout)

    def save_profile(self, instance):  # pylint: disable=unused-argument
        """Save profile data."""
        profile = Profile(
            name=self.name_input.text,
            age=int(self.age_input.text),
            weight=float(self.weight_input.text),
        )
        self.storage.save_profile(profile)
        self.manager.current = 'main'
