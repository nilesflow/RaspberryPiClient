#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import boto3
import json
import uuid
from time import sleep

# user modules
from pyfw import util
from pyfw.error.error import Error, ParamError
from pyfw.error.httperror import HttpInternalError

from pahoraspberrypi import PahoRaspberryPi

class RaspberryPi:
    """
    RaspberryPi操作クラス
    """

    def __init__(self, **args):
        self.logger = args['logging'].getLogger(__name__)

        # publishのみ
        self.iot = boto3.client('iot-data')

        # subscribe：RaspberryPiからのレスポンス待ち準備
        # パラメータが定義されていた場合
        if 'host' in args and args['host']:
            self.topic_sub = 'raspberrypi/response'
            self.paho = PahoRaspberryPi(
                topic_sub = self.topic_sub,
                ca = args['ca'],
                cert = args['cert'],
                key = args['key'],
                host = args['host'],
                port = 8883,
                keepalive = 3,
                logging = args['logging'],
                on_message = self.on_response
            )
    
            # subscribe受信管理用
            self.isReceived = False
            self.response = None

            # publish前にsubscribeしておく
            result = self.paho.loop_start()
            self.logger.info(result)

    def _terminate(self):
        """
        subscribe停止
        """
        result = self.paho.loop_stop()
        self.logger.info(result)

        result = self.paho.disconnect()
        self.logger.info(result)

    def _request(self, action, payload):
        """
        AWS IoTでRaspberryPiへリクエスト
        """
        self.request_id = str(uuid.uuid4())
        payload['request_id'] = self.request_id

        result = self.iot.publish(
            topic = 'raspberrypi/request/' + action,
            qos = 0,
            payload = json.dumps(payload, ensure_ascii=False)
        )
        self.logger.info(result)

    def _wait_response(self):
        """
        RaspberryPiからの受信待ち
        """
        
        #最大X秒待つ
        for wait in range(30):
            # 有効なレスポンスを受信
            if self.isReceived:
                break;
            sleep(0.1)
        else:
            raise HttpUnavailableError("タイムアウトが発生しました。")

        # callback状況の確認
        if not self.response:
            raise HttpUnavailableError("応答の受信に失敗しました。")
        self.logger.info(self.response)
        response = self.response

        # RaspberryPi側のエラーチェック
        if 'error' in response:
            e = response.error
            if e.error == 'internal_error':
                raise HttpInternalError(e.description)
            else:
                raise HttpUnavailableError(e.description)

        # 正常終了
        if 'result' in response:
            return response['result']

        return 'RaspberryPiの処理が成功しました。'

    def speak(self, text):
        """
        RaspberryPiへ音声出力要求
        """
        self.logger.info(text)

        # AWS IoTでRaspberryPiへ音声出力要求
        payload = {
            'text': text,
            # see https://docs.aws.amazon.com/ja_jp/polly/latest/dg/voicelist.html
            'voice' : "Takumi"
        }
        self._request('speak', payload)

        # subscribeモードでなければ、ここで応答を返す
        if not hasattr(self, 'paho'):
            return 'RaspberryPiへリクエストを送信しました。'

        # レスポンスを待つ
        ret = self._wait_response()
        
        # 終了処理
        self._terminate()

        return ret

    def on_response(self, msg):
        """
        応答の受信

        :param dict msg: dictionary converted from json
         str  topic : raspberrypi/response
         int  qos :
         json payload : {"param1": "...", "param2": "..."}

          payload : {"action": "...", "request_id": "..."}
        	:str action: requestで指定したaction
        	:str request_id: requestで指定したrequest_id
        """
        try:
            self.logger.info("Topic: " + str(msg.topic))
            self.logger.info("QoS: " + str(msg.qos))
            self.logger.info("Payload: " + str(msg.payload))

            # topic 確認
            # Level1:既定文字列のチェック
            levels_pub = msg.topic.split('/', 2)
            levels_sub = self.topic_sub.split('/')
            if levels_pub[0] != levels_sub[0]:
            	raise ParamError("invalid topic.")
            
            # Level2：typeのチェック
            if levels_pub[1] != levels_sub[1]:
            	raise ParamError("invalid type.")
            
            # responseをjsonデコード
            response = json.loads(msg.payload)
            
            # リクエストIDのチェック
            if not response['request_id']:
            	raise ParamError("can't find request_id.")
            if response['request_id'] != self.request_id:
                raise ParamError("invalid request_id.")
            
            # 処理終了
            self.response = response
            self.isReceived = True
            self.logger.info('received valid response.')

        except Error as e:
        	self.logger.error(e.description)
        	# 正しい応答を待つ
        
        except Exception as e:
        	self.logger.critical(e)
        	self.logger.critical(util.trace())
	        # 正しい応答を待つ
