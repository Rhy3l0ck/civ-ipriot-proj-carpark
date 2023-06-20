from datetime import datetime

import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
from random import uniform


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config['broker'])
        carpark_name = config['broker']['location']
        self.total_spaces = config[carpark_name]['total-spaces']
        self.total_cars = config.get(f"{carpark_name}.total-cars", 0)
        self.temperature = None
        if self.temperature is None:
            self.temperature = round(uniform(19, 28))
        print(f"Carpark at {carpark_name} is ready")
        self.mqtt_carpark = paho.Client()
        self.mqtt_carpark.connect(config['broker']['broker'], config['broker']['port'])
        self.mqtt_carpark.subscribe(config['broker']['topic-final'])
        self.mqtt_carpark.on_message = self.on_message
        self.mqtt_carpark.loop_forever()

    def available_spaces(self):
        self.available = self.total_spaces - self.total_cars
        if self.available in range(0, 193):
            return self.available

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                    f"TIME: {readable_time}, "
                    + f"SPACES: {self.available_spaces()}, "
                    + f"TEMPC: {self.temperature}"
            )
        )
        message = (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces()}, "
                + f"TEMPC: {self.temperature}"
        )
        self.mqtt_carpark.publish(config['broker']['topic-final'], message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        if "Temp" in payload:
            payload_split = payload.split('is')
            temp = payload_split[1].strip()
            temp = float(temp)
            self.temperature = round(temp)
        # self.temperature = ... # Extracted  value
        if 'exited' in payload:
            self.on_car_exit()
        elif 'entered' in payload:
            self.on_car_entry()


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    car_park = CarPark(config)
