import random
import threading
import time
from windowed_display import WindowedDisplay
import paho.mqtt.client as paho


class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']
    fields_dictonary = {}

    def payload_split(self, client, userdata, message):
        msg = message
        payload = str(msg.payload.decode("UTF-8"))
        if "Car" not in payload:
            payload_split = payload.split()
            self.fields_dictonary[self.fields[0]] = payload_split[3]
            self.fields_dictonary[self.fields[1]] = payload_split[5]
            self.fields_dictonary[self.fields[2]] = payload_split[1]

    def __init__(self):
        self.window = WindowedDisplay(
            'Joondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()
        self.payload_split = None

    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription
        from config_parser import parse_config
        config = parse_config("config.toml")
        topic = config['broker']['topic-final']
        broker = config['broker']['broker']
        port = config['broker']['port']
        mqtt_sub = paho.Client()
        mqtt_sub.connect(broker, port)
        mqtt_sub.subscribe(topic)
        while True:
            mqtt_sub.on_message = self.payload_split
            print(CarParkDisplay.fields[1])
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{CarParkDisplay.fields_dictonary.get(CarParkDisplay.fields[0])}',
                f'{CarParkDisplay.fields_dictonary.get(CarParkDisplay.fields[1])}℃',
                f'{CarParkDisplay.fields_dictonary.get(CarParkDisplay.fields[2])}']))
            # Pretending to wait on updates from MQTT
            time.sleep(random.randint(1, 10))
            # When you get an update, refresh the display.
            self.window.update(field_values)
            mqtt_sub.loop_forever()


if __name__ == '__main__':
    CarParkDisplay()
