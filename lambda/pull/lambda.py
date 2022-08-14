import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
  # TODO: should pull data from s3
  logger.info('incoming event: {}'.format(event))

  sqs = boto3.client('sqs')

  # TODO: queue_url is hardcoded, store it in parameter store
  queue_url = 'https://sqs.eu-west-1.amazonaws.com/933021064415/sqs-stack-firstqueueCCA81F5D-Z4fY2lRXzi8X'  

  message_body = ""
  if event is None:
    message_body = 'peanutbutter is good'
  else:
    message_body = event

  response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=5,
    MessageAttributes={
        'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        },
        'Author': {
            'DataType': 'String',
            'StringValue': 'John Grisham'
        },
        'WeeksOn': {
            'DataType': 'Number',
            'StringValue': '6'
        }
    },
    MessageBody=(
      json.dumps(message_body)
    )
  )

  logger.info('Sent message with id: {}'.format(response['MessageId']))

  return {
    'statusCode': 200,
    'body': 'success'
  }
