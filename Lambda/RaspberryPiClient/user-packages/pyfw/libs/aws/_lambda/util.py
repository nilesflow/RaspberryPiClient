#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
import logging

def basicConfig():
    """
    Lambda呼び出し側で設定されているハンドラを削除
    logging設定を行うため
    """
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    level = eval("logging." + os.environ['LOGGING_LEVEL']) if 'LOGGING_LEVEL' in os.environ else logging.INFO
    logging.basicConfig(
        level = level
    )