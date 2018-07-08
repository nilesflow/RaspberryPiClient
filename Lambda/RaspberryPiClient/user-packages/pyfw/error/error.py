#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Error(Exception):
	"""
	例外クラス：基底クラス
	"""

	def __init__(self, error, description):
		self.error = error
		self.description = description

class ParamError(Error):
	"""
	例外クラス：パラメータエラー
	"""

	def __init__(self, description):
		super(ParamError, self).__init__("invalid_request", description)

class InternalError(Error):
	"""
	例外クラス：内部エラー
	"""

	def __init__(self, description):
		super(InternalError, self).__init__("internal_error", description)