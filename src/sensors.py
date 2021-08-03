from gpiozero import Button
import time


sensorPin1 = 25
sensorPin2 = 20
sensorPin3 = 21
sensorPin4 = 5
sensorPin5 = 6
sensorPin6 = 13
sensorPin7 = 19
sensorPin8 = 26


class Switch():
    def __init__(self, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8):
        self.sensor1 = Button(sensor1)
        self.sensor2 = Button(sensor2)
        self.sensor3 = Button(sensor3)
        self.sensor4 = Button(sensor4)
        self.sensor5 = Button(sensor5)
        self.sensor6 = Button(sensor6)
        self.sensor7 = Button(sensor7)
        self.sensor8 = Button(sensor8)

    def read_value(self):
        return {"sensor1": self.sensor1.value, "sensor2": self.sensor2.value, "sensor3": self.sensor3.value, "sensor4": self.sensor4.value, "sensor5": self.sensor5.value, "sensor6": self.sensor6.value, "sensor7": self.sensor7.value, "sensor8": self.sensor8.value}


if __name__ == '__main__':
    sensorBlock = Switch(sensorPin1, sensorPin2, sensorPin3,
                         sensorPin4, sensorPin5, sensorPin6, sensorPin7, sensorPin8)
    while True:
        print(sensorBlock.read_value())
        time.sleep(1)
