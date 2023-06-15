import random
import threading
import time
import tkinter as tk
from typing import Iterable
import paho.mqtt.client as paho
from windowed_display import WindowedDisplay

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def on_message_callback(self, client, userdata, message):
        msg = message
        msg_data = str(msg.payload.decode("UTF-8"))
        print(msg_data)
        return msg_data

    def __init__(self):
        self.window = WindowedDisplay(
            'Joondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription
        available_bays = 192
        while True:
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{available_bays}',
                f'{random.randint(0, 45):02d}℃',
                time.strftime("%H:%M:%S")]))
            # Pretending to wait on updates from MQTT
            time.sleep(random.randint(1, 10))
            # When you get an update, refresh the display.
            self.window.update(field_values)
            client.loop_forever()


if __name__ == '__main__':
    CarParkDisplay()