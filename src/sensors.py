from gpiozero import Button
import time


sensorPin1 = 25
sensorPin2 = 20
sensorPin3 = 21


class Switch():
    def __init__(self, sensor1, sensor2, sensor3):
        self.sensor1 = Button(sensor1)
        self.sensor2 = Button(sensor2)
        self.sensor3 = Button(sensor3)

    def read_value(self):
        return {"sensor1": self.sensor1.value, "sensor2": self.sensor2.value, "sensor3": self.sensor3.value}


if __name__ == '__main__':
    sensorBlock = Switch(sensorPin1, sensorPin2, sensorPin3)
    while True:
        print(sensorBlock.read_value())
        time.sleep(1)
