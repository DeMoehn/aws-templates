import boto3
import datetime
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

  userName = event['detail']['userIdentity']['arn'].split('/')[1]
  instanceId = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
  date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print("Adding Owner tag " + userName + " to instance " + instanceId + ".")
  print("Adding Launched tag " + date + " to instance " + instanceId + ".")
  ec2.create_tags(Resources=[instanceId,],Tags=[{'Key': 'Owner', 'Value': userName},{'Key': 'Launched', 'Value': date}])
  return