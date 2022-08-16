from aws_cdk import (
    aws_sqs as sqs,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct


class SQSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # environment variables are set in 'cdk.json'
        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        """ 
        SQS Queues
        """
        sqs_queue_first = sqs.Queue(
            self, 'first_queue', queue_name='first_queue')  
        
        """ 
        SSM Parameters
        """
        self.sqs_queue_first_url = ssm.StringParameter(
            self, 'sqs_queue_first_url',
            parameter_name='/{}/sqs_queue_first_url'.format(env_name),
            string_value=sqs_queue_first.queue_url
        )