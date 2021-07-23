#!/usr/bin/env python
from flask import Flask, request
from flask_socketio import SocketIO
import eventlet
from threading import Lock


class SocketServer:
    def __init__(self, host="localhost", port=8080):

        self.host = host
        self.port = port

        async_mode = "eventlet"

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode=async_mode,
                                 cors_allowed_origins="*")

        self.socketio.on_event("connect", self.connect)
        self.socketio.on_event("disconnect", self.disconnect)

        self.thread = None
        self.thread_lock = Lock()

    def background_thread(self):
        while True:
            self.socketio.sleep(3.1)
            print("hit")

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
    server = SocketServer()
    server.run()
