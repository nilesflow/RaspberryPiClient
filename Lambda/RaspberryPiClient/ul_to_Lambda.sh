#!/bin/sh

rm -f Lambda-RaspberryPiClient.zip
git archive HEAD --output=Lambda-RaspberryPiClient.zip --worktree-attributes

# 証明書があるか確認
if [ -e certs ]; then
    :
else
    echo "certs/ 配下にSSL証明書を指定してください。"
    exit
fi
zip -r Lambda-RaspberryPiClient.zip certs

aws lambda update-function-code --function-name RaspberryPiClient --zip-file fileb://Lambda-RaspberryPiClient.zip --publish
