#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
see https://github.com/pradeesi/AWS-IoT-with-Python-Paho
"""

# standard modules
import paho.mqtt.client as mqtt
import ssl
import json

class PahoAwsIot:

	def __init__(self, **args):
		self.logger = args['logging'].getLogger(__name__)

		self.topic_sub = args['topic_sub']

		# Initiate MQTT Client
		mqttc = mqtt.Client()

		# Assign event callbacks
		mqttc.on_message = self._on_message
		mqttc.on_connect = self._on_connect
		mqttc.on_subscribe = self._on_subscribe

		# Configure TLS Set
		mqttc.tls_set(
			args['ca'],
			certfile = args['cert'],
			keyfile = args['key'],
			cert_reqs = ssl.CERT_REQUIRED,
			tls_version = ssl.PROTOCOL_TLSv1_2,
			ciphers = None
		)

		# Connect with MQTT Broker
		mqttc.connect(
			args['host'],
			int(args['port']),
			int(args['keepalive'])
		)

		self.mqttc = mqttc

	def _on_connect(self, client, userdata, flags, rc):
		"""
		Define on connect event function
		We shall subscribe to our Topic in this function
		"""
		self.logger.error(self.topic_sub)
		self.mqttc.subscribe(self.topic_sub, 0)

	def _on_message(self, mosq, obj, msg):
		"""
		Define on_message event function. 
		This function will be invoked every time,
		a new message arrives for the subscribed topic 
		"""
		pass

	def _on_subscribe(self, mosq, obj, mid, granted_qos):
		self.logger.info("Subscribed to Topic with QoS: " + str(granted_qos))

	def loop_start(self):
		return self.mqttc.loop_start()

	def loop_stop(self, force=False):
		return self.mqttc.loop_stop(force)

	def loop_forever(self, timeout):
		# Continue monitoring the incoming messages for subscribed topic
		return self.mqttc.loop_forever(timeout)

	def disconnect(self):
		return self.mqttc.disconnect()