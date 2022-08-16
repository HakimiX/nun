import queue
import string
from aws_cdk import (
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_ssm as ssm,
    aws_s3 as _s3,
    aws_s3_notifications as s3_notification,
    aws_lambda_event_sources as lambda_events,
    Stack
)
from constructs import Construct


class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # environment variables are set in 'cdk.json'
        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.s3_bucket = _s3.Bucket(
          self, 's3_bucket',
          removal_policy=RemovalPolicy.DESTROY,
          auto_delete_objects=True
        )

        # store s3 bucket name in ssm 
        self.s3_bucket_name_param = ssm.StringParameter(
          self, 's3_bucket_name',
          parameter_name='/{}/s3_bucket_name'.format(env_name),
          string_value=self.s3_bucket.bucket_name
        )

        # notify lambda about new objects
        #new_object_notification = s3_notification.LambdaDestination(lambda_to_notify)
        #self.s3_bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, new_object_notification)