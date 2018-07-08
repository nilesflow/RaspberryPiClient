#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import urllib.request

# user modules
from pyfw.error.error import Error

class Http:

	def __init__(self, **kargs):
		logging = kargs['logging']
		self.logger = logging.getLogger(__name__)

	def post(self, **kargs):
		try:
			self.logger.debug(kargs)
			url = kargs['url']
			data = kargs['data']
			headers = kargs['headers']
	
			request = urllib.request.Request(
				url = url,
				data = data.encode("utf-8"),
				headers = headers,
				method = "POST"
			)
			with urllib.request.urlopen(request) as response:
				code = response.getcode()
				self.logger.info(code)
	
				body = response.read().decode('utf-8')
				self.logger.info(body)
				return body

		except Exception as e:
			self.logger.error(e)
			raise HTTPError(e)

class HTTPError(Error):
	"""
	このモジュールのエラー
	"""

	def __init__(self, description):
		super(HTTPError, self).__init__("internal_error", description)
