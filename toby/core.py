
import os, urlparse, time
import paho.mqtt.client as mqtt
from .errors import ConnectionError
from .errors import CallbackError


class Bot:

    def __init__(self, botId, botSk):
        self.botId = botId
        self.botSk = botSk
        self.client = False
        self.on_message = False
        self.on_connect = False

    def set_on_connect (self, callback):
        self.on_connect = callback

    def set_on_message(self, callback):
        self.on_message = callback

    # TODO
    def follow(self, hashtag_string):
        if (not self.client):
            raise ConnectionError('Bot#follow requires active connection')
        #self.client.publish("server/" + self.botId + "/follow", hashtag_string)

    # TODO
    def send(self, message):
        if (not self.client):
            raise ConnectionError('Bot#send requires active connection')

        self.client.publish("server/" + self.botId, message)


    def start(self):
        if (not self.on_connect or not self.on_message):
            raise CallbackError('set on_connect and on_message callbacks before starting')
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            self.client.subscribe("client/" + self.botId + "/#")
            self.on_connect()

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            self.on_message(str(msg.payload))

        self.client = mqtt.Client(client_id=self.botId)
        self.client.username_pw_set(self.botId, password=self.botSk)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect("toby.cloud", 444, 60)

        # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
        self.client.loop_forever()
