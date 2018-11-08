# CLI Commands

This only includes some useful CLI commands

## EC2

Here are some commands for EC2:

- Get Instance Details: `aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId, State.Name, InstanceType]' --output table`
- Get Amazon Linux AMIs: `aws ec2 describe-images --filters "Name=name,Values=amzn2-ami-hvm-2*-gp2" --query 'Images[*].{Name:Name,ImageId:ImageId}' --output table`
- Get Subnets: `aws ec2 describe-subnets --query 'Subnets[*].[AvailabilityZone, VpcId, SubnetId, Tags[?Key==`Name`].Value[] | [0]]' --output table`
- Get Security Groups: `aws ec2 describe-security-groups --query 'SecurityGroups[*].{Name:GroupName, Desc:Description, Id:GroupId}' --output table`
- Get KeyPairs: `aws ec2 describe-key-pairs --query 'KeyPairs[*].[KeyName]' --output table`

## Just Useful

Here are some random useful commands:

- Get AWS Account ID: `aws sts get-caller-identity`