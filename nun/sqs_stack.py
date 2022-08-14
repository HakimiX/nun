from aws_cdk import (
    aws_sqs as sqs,
    aws_lambda as _lambda,
    Stack
)
from constructs import Construct

class SQSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, lambda_fn: _lambda.Function, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SQS queue (first)
        sqs_queue_first = sqs.Queue(self, 'first-queue')

        # allow lambda_pull to send messages
        sqs_queue_first.grant_send_messages(grantee=lambda_fn)