def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        "body": "Hello from Lambda",
        "isBase64Encoded": "false"
    }
    return response