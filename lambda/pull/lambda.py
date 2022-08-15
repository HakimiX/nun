import logging
import boto3
import json
import os

""" 
Flow 
1. Get S3 notification (OBJECT_CREATED)
2. Get S3 object (parse content)
3. Send SQS message
"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.environ['SQS_QUEUE_FIRST_URL']
S3_BUCKET = os.environ['S3_BUCKET']


def fetch_object(bucket, key):
    logger.info('Fetching object: {}, from bucket: {}'.format(bucket, key))

    s3_client = boto3.client('s3')
    object = s3_client.get_object(Bucket=bucket, Key=key)
    object = json.loads(object['Body'].read())
    
    logger.info('Object content: {}'.format(object))
    return object


def send_message(queue, message):
    logger.info('Sending message: {}, to queue: {}'.format(message, queue))

    sqs_client = boto3.client('sqs')
    return sqs_client.send_message(
        QueueUrl=queue,
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
            json.dumps(message)
        )
    )


def handler(event, context):
    logger.info('incoming event: {}, type: {}'.format(event, type(event)))

    for s3_event in event['Records']:
        if s3_event['eventSource'] == 'aws:s3' and s3_event['eventName'] == 'ObjectCreated:Put':
            logger.info('Got an s3 event: OBJECT_CREATED')
            s3_key = s3_event['s3']['object']['key']

            # 1. fetch object
            message_body = fetch_object(S3_BUCKET, s3_key)

            # 2. send object content in a message
            response = send_message(SQS_QUEUE_URL, message_body)

    logger.info('Sent message with id: {}'.format(response['MessageId']))

    return {
        'statusCode': 200,
        'body': 'success'
    }
