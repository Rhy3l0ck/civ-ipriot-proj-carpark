from datetime import datetime

import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config['broker'])
        carpark_name = config['broker']['location']
        self.total_spaces = config[carpark_name]['total-spaces']
        self.total_cars = config.get(f"{carpark_name}.total-cars", 0)
        self._temperature = None
        print(f"Carpark at {carpark_name} is ready")
        self.mqtt_carpark = paho.Client()
        self.mqtt_carpark.connect(config['broker']['broker'], config['broker']['port'])
        self.mqtt_carpark.subscribe(config['broker']['topic-final'])
        self.mqtt_carpark.on_message = self.on_message
        self.mqtt_carpark.loop_forever()

    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                    f"TIME: {readable_time}, "
                    + f"SPACES: {self.available_spaces}, "
                    + "TEMPC: 42"
            )
        )
        message = (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces}, "
                + "TEMPC: 42"
        )
        self.mqtt_carpark.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        print(msg)
        payload = msg.payload.decode()
        # TODO: Extract temperature from payload
        # self.temperature = ... # Extracted  value
        if 'exited' in payload:
            self.on_car_exit()
        elif 'entered' in payload:
            self.on_car_entry()


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    car_park = CarPark(config)
    print("Carpark initialized")
