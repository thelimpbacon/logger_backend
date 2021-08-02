#!/usr/bin/env python
from flask import Flask, request
from flask_socketio import SocketIO
import eventlet
from threading import Lock
from sensors import Switch

sensorPin1 = 25
sensorPin2 = 20
sensorPin3 = 21


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

            self.socketio.emit("sensors", {
                               "sensor1": sensor_data["sensor1"], "sensor2": sensor_data["sensor2"], "sensor3": sensor_data["sensor3"], "tick": tick})
            tick += 1

            if tick == 500:
                tick = 0

    def connect(self):
        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socketio.start_background_task(
                    self.background_thread)
        print("Connected", request.sid)

    def disconnect(self):
        print("Disconnected", request.sid)

    def run(self):
        print(f"server running in {self.host}:{self.port}")
        self.socketio.run(self.app, self.host, self.port)


if __name__ == '__main__':
    server = SocketServer(sensorBlock=Switch(
        sensorPin1, sensorPin2, sensorPin3))
    server.run()
