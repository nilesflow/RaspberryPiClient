# see https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Help function to generate an IAM policy
def generate_policy(principalId, effect, resource):
  return {
    'principalId': principalId,
    'policyDocument': {
      'Version': '2012-10-17',
      'Statement': [{
        'Action': 'execute-api:Invoke',
        'Effect': effect,
        'Resource': resource
      }]
    }
  }

def generate_allow(principalId, resource):
    return generate_policy(principalId, 'Allow', resource)

def generate_deny(principalId, resource):
    return generate_policy(principalId, 'Deny', resource)


def lambda_handler(event, context):
    logger.info(event)

    queryStringParameters = event['queryStringParameters']

    if queryStringParameters['token'] == os.environ['AUTHORIZATION_TOKEN']:
        return generate_allow('me', event['methodArn'])
    else:
        raise Exception("認証エラーが発生しました。")
