#!/bin/sh

git archive HEAD --output=Lambda-RaspberryPiClient.zip
aws lambda update-function-code --function-name RaspberryPiClient --zip-file fileb://Lambda-RaspberryPiClient.zip --publish
