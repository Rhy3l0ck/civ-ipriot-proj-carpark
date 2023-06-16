import tkinter as tk
from mqtt_device import MqttDevice


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
        self.mqtt_detector = MqttDevice(config['broker'])
        self.root.mainloop()

    def incoming_car(self):
        self.mqtt_detector.client.publish("Car goes in")

    def outgoing_car(self):
        self.mqtt_detector.client.publish("Car goes out")


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    CarDetector(config)
