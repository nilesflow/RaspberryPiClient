#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import json

# user modules
from pyfw.http import Http

class IncomingWebHooks:

	def __init__(self, **kargs):
		self.url = kargs['url']

		self.logger = kargs['logging'].getLogger(__name__)

		self.http = Http(
			logging = kargs['logging']
		)

	def webhook(self, text):
		dict = {
			'text': text
		}
		headers = {
			'Content-Type' : 'application/json'
		}
		data = json.dumps(dict, ensure_ascii=False)
		body = self.http.post(
			url = self.url,
			data = data,
			headers = headers
		)