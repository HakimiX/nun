import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
  # TODO: should pull data from s3
  logger.info('incoming event: {}'.format(event))



  return {
    'statusCode': 200,
    'body': 'success'
  }
