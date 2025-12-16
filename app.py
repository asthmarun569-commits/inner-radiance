from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class InnerRadianceApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        layout.add_widget(Label(
            text="🌟 Inner Radiance 🌟",
            font_size=24
        ))

        layout.add_widget(Label(
            text="Your journey has begun.",
            font_size=16
        ))

        layout.add_widget(Button(
            text="Start",
            size_hint=(1, 0.3)
        ))

        return layout

if __name__ == "__main__":
    InnerRadianceApp().run()
