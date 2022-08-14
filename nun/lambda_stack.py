from aws_cdk import (
    aws_lambda as _lambda,
    Stack
)
from constructs import Construct

class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda (pull)
        self.lambda_pull = _lambda.Function(
          self, 'lambda_pull',
          runtime=_lambda.Runtime.PYTHON_3_8,
          function_name='lambda_pull',
          handler="lambda.handler",
          code=_lambda.Code.from_asset('./lambda/pull')
        )

        # Lambda (mod)
        self.lambda_mod = _lambda.Function(
          self, 'lambda_mod',
          function_name='lambda_mod',
          runtime=_lambda.Runtime.PYTHON_3_8,
          handler="lambda.handler",
          code=_lambda.Code.from_asset('./lambda/mod')
        )