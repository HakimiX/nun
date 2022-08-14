from aws_cdk import (
    aws_lambda_event_sources as lambda_events,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    Stack
)
from constructs import Construct

class SQSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, lambda_fns: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_pull: _lambda = lambda_fns['lambda_pull']
        lambda_mod: _lambda = lambda_fns['lambda_mod']

        # SQS queue (first)
        sqs_queue_first = sqs.Queue(self, 'first-queue', queue_name='first_queue')

        # allow lambda_pull to send messages
        sqs_queue_first.grant_send_messages(grantee=lambda_pull)

        # allow lambda mod to consume messages    
        sqs_queue_first.grant_consume_messages(grantee=lambda_mod)
        
        # SQS event
        sqs_event = lambda_events.SqsEventSource(sqs_queue_first)
        
        # SQS event trigger lambda (mod)
        lambda_mod.add_event_source(sqs_event)
