from cProfile import run
from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda
)


class LambdaConstruct(Construct):
    def __init__(self, scope: Construct, id: str, *, url: str, tps: int):
        super().__init__(scope, id)

        lambda_pull = _lambda.Function(
            self, 'lambda_pull',
            function_name='lambda_pull',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda.handler',
            code=_lambda.Code.from_asset('./lambda/pull')
        )
        