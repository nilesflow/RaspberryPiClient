# Slack2RaspberryPi
using AWS API Gateway &amp; AWS Lambda via AWS IoT 
## Slack to RaspberryPi  
```
  Slack Outgoing Webhooks -> API Gateway -> Lambda -> AWS IoT -> RaspberryPi (ex. speaker  
                          <-                Lambda <- AWS IoT <- 
```
### Slack Outgoing Webhooks  
API Gateway のエンドポイントを指定する  
`https://{your domain}/(your path)/speak?token=xxxxxx`

### AWS IoT 
`raspberrypi/request/speak` の形式で MQTT publish  
`raspberrypi/response` の形式で MQTT subscribe  

次の形式のJSONを受け取る
```
{"action": "speak", "request_id": "..."}
```

### Lambda
AWS IoT のSSL証明書を配置  

## RaspberryPi to Slack
```
   Slack Incoming Webhooks <-                Lambda <- AWS IoT <- RaspberryPi (ex. mic  
```
### AWS IoT 
ルールクエリステートメントに `SELECT * FROM 'raspberrypi/notify'`  
アクションで、 Lambda関数`RaspberryPiClient`を呼び出す

次の形式のJSONを受け取る
```
 {"action": "listened", "sender": "raspberrypi", "result": "xxxxx"}
```
### Slack Incoming Webhooks  
エンドポイントを Lambda に設定する
