#!/usr/bin/env python3
import os

import aws_cdk as cdk

from nun.lambda_stack import LambdaStack
from nun.sqs_stack import SQSStack

app = cdk.App()

lambda_stack = LambdaStack(app, 'lambda-stack')

sqs_stack = SQSStack(app, 'sqs-stack', lambda_fns={
  'lambda_pull': lambda_stack.lambda_pull,
  'lambda_mod': lambda_stack.lambda_mod
})

app.synth()
