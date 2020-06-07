import json
import os
from boto3 import client
from service_discovery import lookup_resource_arn

region = 'eu-west-1'


def lambda_handler(event, context):
    """
    - discover service / instance
    - invoke lambda
    """
    
    lambda_client = client('lambda', region_name=region)

    service_name = os.environ['ENV_SERVICE_NAME']
    namespace_name = os.environ['ENV_NAMESPACE_NAME']
    service_arn = lookup_resource_arn(service_name, namespace_name, region)

    # Lets invoke service lambda
    service_response = lambda_client.invoke(
        FunctionName=service_arn,
        InvocationType='RequestResponse',
        LogType='None',
        Payload='{}',
    )


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world, im a consumer lambda",
            "service_response": json.load(service_response['Payload'])
        }),
    }
