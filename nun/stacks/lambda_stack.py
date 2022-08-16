from aws_cdk import (
    aws_lambda as _lambda,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, sqs_queue_first_url: ssm, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_pull = _lambda.Function(
            self, 'lambda_poll',
            function_name='lambda_poll',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda.handler',
            code=_lambda.Code.from_asset('./lambda/pull'),
            environment={
                'SQS_QUEUE_FIRST_URL': sqs_queue_first_url
            }
        )
