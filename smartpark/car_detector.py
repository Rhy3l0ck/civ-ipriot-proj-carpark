import tkinter as tk
from mqtt_device import MqttDevice
import paho.mqtt.client as paho


class CarDetector(MqttDevice):
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, config):
        super().__init__(config['broker'])
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘', font=('Arial', 50), cursor='bottom_left_corner',
            command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)
        self.topic = config['broker']['topic-final']
        self.broker = config['broker']['broker']
        self.port = config['broker']['port']
        self.mqtt_detector = paho.Client()
        self.mqtt_detector.connect(self.broker, self.port)
        self.root.mainloop()

    def incoming_car(self):
        self.mqtt_detector.publish(self.topic, "Car goes in")
        print("Car has entered")

    def outgoing_car(self):
        self.mqtt_detector.publish(self.topic, "Car goes out")
        print("Car has exited")


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    CarDetector(config)
