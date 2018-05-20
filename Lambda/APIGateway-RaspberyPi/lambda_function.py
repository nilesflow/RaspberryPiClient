#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
import sys
import logging

# 実行ディレクトリ＆モジュールパス設定
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
sys.path.append(dir + '/site-packages')
sys.path.append(dir + '/user-packages')

# user modules 
from pyfw.error.error import Error
from pyfw.error.httperror import HttpParamError, HttpInternalError
from pyfw import util
from lambdautil import apigateway

from raspberrypi import RaspberryPi

def lambda_handler(event, context):
    """
    Lambda Handler
    
    :param str event['action']: (required) RaspberryPiに指示するコマンド
    :param str event['user']: (optional) 指示ユーザ
    
     action:
      speak --
       :param str event['text'] : (required) 再生するメッセージ
    """

    try:
        logger = logging.getLogger(__file__)
        logger.setLevel(logging.DEBUG)

        logger.info(event)
    
        # パラメータを取得
        if 'action' not in event:
            raise HttpParamError("actionが指定されていません。")
        action = event['action']

        user = None
        if 'user' in event:
            user = event['user']

        # actionに従った処理
        if action == 'speak': 
            # パラメータ準備
            if 'text' not in event:
                raise HttpParamError("textが指定されていません。")
            text = event['text']

            # 音声出力処理
            cwd = os.getcwd()
            pi = RaspberryPi(
                host = os.environ['SUBSCRIBE_HOST'] if 'SUBSCRIBE_HOST' in os.environ else None,
                ca = cwd + '/' + os.environ['SUBSCRIBE_CAROOTFILE'] if 'SUBSCRIBE_CAROOTFILE' in os.environ else None,
                cert = cwd + '/' + os.environ['SUBSCRIBE_CERTFILE'] if 'SUBSCRIBE_CERTFILE' in os.environ else None,
                key = cwd + '/' + os.environ['SUBSCRIBE_KEYFILE'] if 'SUBSCRIBE_KEYFILE' in os.environ else None,
                logging = logging
            )
            result = pi.speak(text)
            logger.info(result)

        else:
            raise HttpParamError("定義されていないactionです。")

        # 正常終了
        return apigateway.success(result + "invoked %s" % (user))

    except Error as e:
        logger.error(e)
        return apigateway.error(e.statusCode, e.error, e.description)

    except Exception as exp:
        logger.critical(exp)
        logger.critical(util.trace())
        e = HttpInternalError("内部エラーが発生しました。")
        return apigateway.error(e.statusCode, e.error, e.description)

