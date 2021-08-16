#!/usr/bin/env python
from flask import Flask, request
from flask_socketio import SocketIO
from threading import Lock
from sensors import Switch
import csv
import time

sensorPin1 = 25
sensorPin2 = 20
sensorPin3 = 21
sensorPin4 = 5
sensorPin5 = 6
sensorPin6 = 13
sensorPin7 = 19
sensorPin8 = 26


class SocketServer:
    def __init__(self, sensorBlock, host="192.168.178.51", port=8080):

        self.host = host
        self.port = port
        self.sensorBlock = sensorBlock

        async_mode = "eventlet"

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode=async_mode,
                                 cors_allowed_origins="*")

        self.socketio.on_event("connect", self.connect)
        self.socketio.on_event("disconnect", self.disconnect)

        self.thread = None
        self.thread_lock = Lock()

    def background_thread(self):
        tick = 0
        while True:
            self.socketio.sleep(0.1)

            sensor_data = self.sensorBlock.read_value()

            # specific data
            sensor1 = sensor_data["sensor1"]
            sensor2 = sensor_data["sensor2"]
            sensor3 = sensor_data["sensor3"]
            sensor4 = sensor_data["sensor4"]
            sensor5 = sensor_data["sensor5"]
            sensor6 = sensor_data["sensor6"]
            sensor7 = sensor_data["sensor7"]
            sensor8 = sensor_data["sensor8"]

            # log sensor data to disk
            self.writer.writerow([sensor1, sensor2, sensor3, sensor4,
                                  sensor5, sensor6, sensor7, sensor8, tick, time.time()])

            self.socketio.emit("sensors", {
                "sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4,
                "sensor5": sensor5, "sensor6": sensor6,  "sensor7": sensor7, "sensor8": sensor8, "tick": tick})
            tick += 1

            if tick == 500:
                tick = 0

    def connect(self):
        # open csv and creat css writer
        log_path = "./logs/" + request.sid + ".csv"
        self.file = open(log_path, "w")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["sensor1", "sensor2", "sensor3", "sensor4",
                             "sensor5", "sensor6", "sensor7", "sensor8", "tick", "actual_time"])

        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socketio.start_background_task(
                    self.background_thread)

        print("Connected", request.sid)

    def disconnect(self):
        # close csv
        self.file.close()
        print("Disconnected", request.sid)

    def run(self):
        print(f"server running in {self.host}:{self.port}")
        self.socketio.run(self.app, self.host, self.port)


if __name__ == '__main__':
    server = SocketServer(host="10.3.141.1", sensorBlock=Switch(
        sensorPin1, sensorPin2, sensorPin3, sensorPin4, sensorPin5, sensorPin6, sensorPin7, sensorPin8))
    server.run()
