import boto3
import json

class RaspberryPi:
    """
    RaspberryPi操作クラス
    """

    def __init__(self, logger):
        self.logger = logger
        self.iot = boto3.client('iot-data')

    def speak(self, text) :
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
        result = self.iot.publish(
            topic = 'raspberrypi/speak',
            qos = 0,
            payload = json.dumps(payload, ensure_ascii=False)
        )
        self.logger.info(result)
