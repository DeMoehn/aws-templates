# Cloudformation: EC2 with SecurityGroup
Deploys a simple EC2 Instance with a HTTP/SSH Security Group

## How to use

- Replace <STACK_NAME>, <ENVIRONMENT_NAME>, <KEY-PAIR_NAME>, <SUBNET_ID>, <VPC_ID> and <SECURITY-GROUP_ID>

``` bash
aws cloudformation create-stack --stack-name <STACK_NAME> \
--template-body file://EC2_and_SG.yaml \
--parameters ParameterKey=EnvironmentName,ParameterValue=<ENVIRONMENT_NAME> ParameterKey=KeyName,ParameterValue=<KEY-PAIR_NAME> ParameterKey=CreateSecurityGroup,ParameterValue=true ParameterKey=SubnetConfig,ParameterValue=<SUBNET_ID> ParameterKey=VPCConfig,ParameterValue=<VPC_ID> ParameterKey=SecurityGroupConfig,ParameterValue=<SECURITY-GROUP_ID>
```