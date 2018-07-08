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
from pyfw.error.error import Error, ParamError
from pyfw.error.httperror import HttpParamError, HttpInternalError
from pyfw.libs import util
from pyfw.libs.aws import _lambda
from pyfw.libs.aws._lambda import apigateway
from pyfw.slack.incomingwebhooks import IncomingWebHooks

# local modules
from raspberrypi import RaspberryPi

def lambda_handler(event, context):
    """
    Lambda Handler
    
    :param str event['sender']: (required) 'slack' or 'raspberrypi'
    :param str event['action']: (required) RaspberryPiに指示するコマンド
    :param str event['user']: (optional) 指示ユーザ
    
     sender:
      slack --
       action:
        speak --
         :param str event['text'] : (required) 再生するメッセージ

      raspberrypi --
       action:
        listend --
         :param str event['result'] : (required) 音声聞き取りの結果
    """

    try:
        # ルートハンドラ除去＆ロギング設定
        _lambda.util.basicConfig()
        logger = logging.getLogger(__file__)
        logger.info(event)

        # API Gateway(Slack) or Aws IoT(RaspberryPi)
        if 'sender' not in event:
            raise ParamError("senderが指定されていません。")
        else:
            sender = event['sender']

    except Exception as exp:
        logger.critical(exp)
        logger.critical(util.trace())
        raise exp

    try:
        # 呼び出し元によって分岐
        if sender == 'raspberrypi':
            # パラメータを取得
            if 'action' not in event:
                raise ParamError("actionが指定されていません。")
            action = event['action']

            # actionに従った処理
            if action == 'listened': 
                # パラメータ準備
                if 'result' not in event:
                    raise ParamError("resultが指定されていません。")
                text = event['result']

                # Lambda設定の確認    
                if 'SLACK_WEBHOOK_URL' not in os.environ:
                    raise InternalError("SLACK_WEBHOOK_URLが設定されていません。")

                # Slackへ通知
                slack = IncomingWebHooks(
                    url = os.environ['SLACK_WEBHOOK_URL'],
                    logging = logging
                )
                slack.webhook(text)
    
            else:
                raise ParamError("定義されていないactionです。")
            
            return 'success'
            
        else:
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

    except Error as err:
        logger.error(err)
        e = err

    except Exception as exp:
        logger.critical(exp)
        logger.critical(util.trace())
        e = HttpInternalError("内部エラーが発生しました。")

    # 共通エラー処理（呼び元に従う）
    if sender == 'raspberrypi':
        # 通常のエラー to AWS IoT / InvocationType : Event
        raise e
    else:
        # 200としてエラー to API Gateway /InvocationType : RequestResponse
        return apigateway.error(e.statusCode, e.error, e.description)
