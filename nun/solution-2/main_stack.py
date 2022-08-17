from ast import Lambda
from aws_cdk import (
    Stack
)
from constructs import Construct

from lambda_construct import LambdaConstruct

class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        LambdaConstruct(self, 'lambda-construct')