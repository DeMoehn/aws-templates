# Read Application Loadbalancer Logs with Lambda

### Install Modules needed by Lambda Function

### Package the Lambda Stack

- As the Lambda Stack uses the Serverless Application Model (SAM) `Transform: AWS::Serverless-2016-10-31`, it needs to be packaged separately

```bash
aws cloudformation package --template-file infrastructure.yaml --s3-bucket demoehn-sam --output-template-file packaged-infrastructure.yaml
````

- That´s it, you should get something like *"Successfully packaged artifacts and wrote output template to file packaged-infrastructure.yaml."*

### Package the complete Stack

- Now you need to package the complete, nested Stack
- The Stack consists of a network Stack, a security Stack, an infrastructure Stack and finally the Lambda Stack.

```bash
aws cloudformation package --template-file root-stack.yaml --s3-bucket demoehn-sam --output-template-file packaged-root-stack.yaml
```

```bash
aws cloudformation deploy --stack-name nandstwo --template-file packaged-root-stack.yaml  --parameter-overrides EnvironmentName=nands SNSSubMail=sebastian.moehn@gmail.com --capabilities CAPABILITY_NAMED_IAM
```