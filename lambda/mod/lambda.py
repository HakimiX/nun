import os
import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.environ['SQS_QUEUE_SECOND_URL']


def handler(event, context):
    logger.info('Incomming event: {}'.format(event))

    sqs = boto3.client('sqs')

    if event is None:
        message_body = 'I know peaut butter is good'
    else:
        message_body = event

    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
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
        'body': 'Success'
    }
