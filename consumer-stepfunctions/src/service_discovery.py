import json
from boto3 import client


def lookup_resource_arn(service_name,namespace_name,aws_region):
    """
    Takes a Cloud Map servicename and namespace name. Looks up a single registered instance for the service and returns the Arn.
    Assumes there is only 1 instance registered to the service, will cause Exception if not.  
    """

    servicediscovery_client = client('servicediscovery', region_name=aws_region)

    # discover
    resp_discover_instances = servicediscovery_client.discover_instances(
        NamespaceName=namespace_name,
        ServiceName=service_name,
        HealthStatus='ALL',
    )

    if len(resp_discover_instances['Instances']) > 1:
        raise IndexError('Found more than 1 instances for service: ' + service_name)
    elif len(resp_discover_instances['Instances']) == 0:
        raise IndexError('Found 0 instances for service: ' + service_name)

    try:
        service_arn = resp_discover_instances['Instances'][0]['Attributes']['Arn']
    except KeyError:
        raise KeyError("Could not find Arn attribute!")
    else:
        return service_arn