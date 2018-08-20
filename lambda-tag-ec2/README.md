# Tag new EC2 Intance

This Lambda function uses CloudWatch Events to tag a new created EC2 Instance with an "Owner" and a "Launched" Tag.

## How to use

- Package the template (uploads the Skript to S3 and creates a valid CloudFormation template)
- Replace \<S3-BUCKET> with an S3 Bucket where the Script can be stored. You can use `aws s3 mb s3://<S3_BUCKET>` to create a new one

``` bash
aws cloudformation package --template-file template.yaml \
--s3-bucket <S3-BUCKET> \
--output-template-file packaged-template.yaml
```

- Replace: \<STACK_NAME> with your desired Stack name
- Deploy the CloudFormation Template

``` bash
aws cloudformation deploy --stack-name <STACK_NAME> \
--template-file packaged-template.yaml  \
--capabilities CAPABILITY_NAMED_IAM
```