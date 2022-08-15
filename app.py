#!/usr/bin/env python3
import os

import aws_cdk as cdk

from nun.nun_stack import NunStack

app = cdk.App()

# Everything in one stack 
nun_stack = NunStack(app, 'nun-stack')

# TODO: implement separated stacks with references in ssm. 

app.synth()
