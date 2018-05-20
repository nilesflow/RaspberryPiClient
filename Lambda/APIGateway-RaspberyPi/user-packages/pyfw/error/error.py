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

class HttpError(Error):
    """
    例外クラス：基底クラス
    """

    def __init__(self, statusCode, error, description):
        super(HttpError, self).__init__(error, description)
        self.statusCode = statusCode

class HttpParamError(HttpError):
    """
    例外クラス：HTTPパラメータエラー
    """

    def __init__(self, description):
        super().__init__(400, "invalid_request", description)

class HttpInternalError(HttpError):
    """
    例外クラス：HTTP内部エラー
    """

    def __init__(self, description):
        super().__init__(500, "server_error", description)

class HttpUnavailableError(HttpError):
    """
    例外クラス：サービス利用不可
    """

    def __init__(self, description):
        super().__init__(503, "service unavailable", description)
