import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
  logger.info('Incomming event: {}'.format(event))

  return {
    'statusCode': 200,
    'body': 'successfully consumed sqs message'
  }