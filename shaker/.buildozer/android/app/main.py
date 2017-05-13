from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import random
import os
import time


from plyer import accelerometer
path = "/home/shipra/Awwnindya/images"


class AccelerometerTest(BoxLayout):
    def __init__(self):
        super(AccelerometerTest, self).__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            time.sleep(1000)
            print(random.choice([
                x for x in os.listdir(path)
                if os.path.isfile(os.path.join(path, x))]))
        time.sleep(10)


class AccelerometerTestApp(App):
    def build(self):
        return AccelerometerTest()

    def on_pause(self):
        return True

if __name__ == '__main__':
    AccelerometerTestApp().run()
