import logging

# user modules 
from exception import Error, ParamError
from util import success, error
from raspberrypi import RaspberryPi

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
        logger.info(event)
    
        # パラメータを取得
        if 'action' not in event:
            raise ParamError("actionが指定されていません。")
        action = event['action']

        user = None
        if 'user' in event:
            user = event['user']

        # actionに従った処理
        if action == 'speak': 
            # パラメータ準備
            if 'text' not in event:
                raise ParamError("textが指定されていません。")
            text = event['text']

            # 音声出力処理
            RaspberryPi(logger).speak(text)

        else:
            raise ParamError("定義されていないactionです。")

        # 正常終了
        return success("RaspberryPiへリクエストを送信しました。invoked %s" % (user))

    except Error as e:
        logger.error(e)
        return error(e.statusCode, e.error, e.description)

    except Exception as e:
        logger.error(e)
        return error(500, "server_error", "内部エラーが発生しました。")

