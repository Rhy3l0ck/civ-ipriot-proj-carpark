import threading
from windowed_display import WindowedDisplay
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']
    dictonary_values = [0, 0, 0]

    def __init__(self, config):
        self.window = WindowedDisplay(
            'Joondalup', CarParkDisplay.fields)
        self.topic = config['broker']['topic-final']
        self.broker = config['broker']['broker']
        self.port = config['broker']['port']
        self.mqtt_sub = paho.Client()
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        while True:
            self.mqtt_sub.connect(self.broker, self.port)
            self.mqtt_sub.subscribe(self.topic)
            self.mqtt_sub.on_message = self.on_message_recieved
            self.mqtt_sub.loop_forever()

    def on_message_recieved(self, client, userdata, msg: MQTTMessage):
        message = msg.payload.decode()
        if 'Car' not in message:
            message = message.replace(',', "")
            payload_split = message.split()
            print(payload_split)
            self.dictonary_values[0] = payload_split[3]
            self.dictonary_values[1] = payload_split[5]
            self.dictonary_values[2] = payload_split[1]
            print("Message recieved")
            print("Updating UI")
            self.updating_visual_interface()

    def updating_visual_interface(self):
        field_values = dict(zip(CarParkDisplay.fields, self.dictonary_values))
        self.window.update(field_values)


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    CarParkDisplay(config)
