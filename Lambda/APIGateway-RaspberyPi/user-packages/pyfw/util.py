#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import sys
import os

def trace():
	"""
	エラー発生個所
	"""
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

	return [exc_type, fname, exc_tb.tb_lineno]
