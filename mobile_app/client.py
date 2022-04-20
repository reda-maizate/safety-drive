from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """
<VideoStream>:
    orientation: 'vertical'
    Label:
        text: 'Client'
        font_size: '30sp'
        size_hint_y: '0.1'
    Camera:
        id: camera
        resolution: (1920, 1080)
        play: False
    ToggleButton:
        text: 'Start camera'
        on_press: root.play()
        size_hint_y: None
        height: '48dp'
"""
)


class VideoStream(BoxLayout):
    def play(self):
        """
        Function to start/stop the camera
        """
        camera = self.ids["camera"]
        camera.play = not camera.play
        print("Started")


class TestCamera(App):
    def build(self):
        return VideoStream()


TestCamera().run()
