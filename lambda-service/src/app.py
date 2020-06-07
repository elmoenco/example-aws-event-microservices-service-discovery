import json


def lambda_handler(event, context):
    """
    Example Lambda service
    """

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world, I'm an Example Lambda service",
            "received_event": event,
        }),
    }
