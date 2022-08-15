import queue
from aws_cdk import (
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_ssm as ssm,
    aws_lambda_event_sources as lambda_events,
    Stack
)
from constructs import Construct


class NunStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # environment variables are set in 'cdk.json'
        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        """ 
        SQS Queues
        """
        # sqs-queue (first)
        sqs_queue_first = sqs.Queue(
            self, 'first_queue', queue_name='first_queue')

        sqs_queue_second = sqs.Queue(
            self, 'second_queue', queue_name='second_queue'
        )

        """ 
        SSM Parameters
        """
        sqs_queue_second_url = ssm.StringParameter(
            self, 'sqs_queue_second_url',
            parameter_name='/{}/sqs_queue_second_url'.format(env_name),
            string_value=sqs_queue_second.queue_url
        )

        sqs_queue_first_url = ssm.StringParameter(
            self, 'sqs_queue_first_url',
            parameter_name='/{}/sqs_queue_first_url'.format(env_name),
            string_value=sqs_queue_first.queue_url
        )

        """ 
        Lambda functions
        """
        # Lambda (pull)
        lambda_pull = _lambda.Function(
            self, 'lambda_pull',
            function_name='lambda_pull',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda.handler",
            code=_lambda.Code.from_asset('./lambda/pull'),
            environment={
                'SQS_QUEUE_FIRST_URL': sqs_queue_first_url.string_value
            }
        )

        # Lambda (mod)
        lambda_mod = _lambda.Function(
            self, 'lambda_mod',
            function_name='lambda_mod',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda.handler',
            code=_lambda.Code.from_asset('./lambda/mod'),
            environment={
                'SQS_QUEUE_SECOND_URL': sqs_queue_second_url.string_value
            }
        )

        """ 
        Permissions
        """
        # grant permission to enqueue
        sqs_queue_first.grant_send_messages(grantee=lambda_pull)
        sqs_queue_second.grant_send_messages(grantee=lambda_mod)

        # grant lambda_mod permission to dequeue
        sqs_queue_first.grant_consume_messages(grantee=lambda_mod)

        # SQS event -> trigger lambda function
        sqs_consume_event = lambda_events.SqsEventSource(sqs_queue_first)
        lambda_mod.add_event_source(sqs_consume_event)

        