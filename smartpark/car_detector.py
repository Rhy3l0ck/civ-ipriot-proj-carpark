import tkinter as tk
from mqtt_device import MqttDevice
import paho.mqtt.client as paho
from random import uniform

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
        carpark_name = config['broker']['location']
        self.total_cars = config.get(f"{carpark_name}.total-cars", 0)
        self.mqtt_detector = paho.Client()
        self.mqtt_detector.connect(self.broker, self.port)
        self.root.mainloop()

    def incoming_car(self):
        if self.total_cars < 192:
            temp = uniform(19, 28)
            self.mqtt_detector.publish(self.topic, "Car has entered")
            self.mqtt_detector.publish(self.topic, f"Temp in Carpark is {temp}")
            self.total_cars += 1
            print("Car has entered")
        else:
            print("Carpark is full")

    def outgoing_car(self):
        if self.total_cars > 0:
            temp = uniform(19, 28)
            self.mqtt_detector.publish(self.topic, "Car has exited")
            self.mqtt_detector.publish(self.topic, f"Temp in Carpark is {temp}")
            self.total_cars -= 1
            print("Car has exited")
        else:
            print("Carpark is empty")


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    CarDetector(config)
