# AWS Templates

This repository shows a couple of my personal AWS Samples, Tools, etc.
Feel free to use them.

## Overview

Currently the collection is seperated into:

- Service Samples: Samples / Demos / Tutorials
- Simple Tools: Tools that may help to work with AWS

## Service Samples

This section includes some samples / demos / tutorials for different AWS services.
May be helpful to get to know the services or to find a simple sample.

### CloudFormation

- cloudformation-ec2: Deploys a simple EC2 Instance with a HTTP/SSH Security Group
- cloudformation-vpc-subnets-and-autoscaling: Deploys a VPC with 4 Subnets (2 Public, 2 Private), 2 NATs, 1 IGW as well as 1 Bastion host (public subnet) and an ALB redirecting traffic to min. 2 autoscaled Webserver Instances in the private Subnets

### IAM

- limit-ec2-region.json: IAM policy that only allows to launch an EC2 actions in a certain region
- limit-ec2-type.json: IAM policy that only allows to launch an EC2 instance with a certain type

## Lambda

- lambda-alb-read-logs: Lambda Function that reacts to Application Loadbalancer (ALB) Log Files
- lambda-api-gateway: Simple Demo of API Gateway used with AWS Lambda
- lambda-s3-image-upload: Lambda reacts to an uploaded image to S3, does resizing and creates a watermark
- lambda-tag-ec2: Lambda reacts to newly created EC2 instances and adds some tags (owner & launched)

## Simple Tools

This section includes some CLI, Python or Node tools that do some stuff in AWS.

### S3

Python Command Line Tools to:

- Clean up S3 Buckets, including all objects and versions (be careful!)
- Create a S3 Bucket with sample objects and versions