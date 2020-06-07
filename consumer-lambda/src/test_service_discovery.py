import boto3
import pytest
from botocore.exceptions import ClientError
import mock
from service_discovery import lookup_resource_arn

region = 'eu-west-1'

@mock.patch("service_discovery.client")
def test_lookup_resource_arn_happy(mock_client):
    """
    This function uses mock.patch as a decorator, and replaces (mocks) client of boto3.
    We're testing both happy and unhappy flow
    """

    print('test happy flow')
    invoke_response = {'Instances': 
        [
            {
                'InstanceId': 'example-serviceInstance',
                'NamespaceName': 'example-namespace',
                'ServiceName': 'example-service',
                'HealthStatus': 'UNKNOWN',
                'Attributes': {
                    'Arn': 'ExampleArn'
                }
            },
        ]
    }
    mock_client.return_value.discover_instances.return_value = invoke_response
    lookup_resource_arn('example-service', 'example-namespace', region)
    mock_client.assert_called_with('servicediscovery', region_name=region)

@mock.patch("service_discovery.client")
def test_lookup_resource_arn_zero_instances(mock_client):
    """
    This function uses mock.patch as a decorator, and replaces (mocks) client of boto3.
    We're testing both happy and unhappy flow
    """

    print('test with zero instances')
    invoke_response = {'Instances': 
        [
        ]
    }
    mock_client.return_value.discover_instances.return_value = invoke_response
    with pytest.raises(IndexError):
        lookup_resource_arn('example-service', 'example-namespace', region)

@mock.patch("service_discovery.client")
def test_lookup_resource_arn_morethanone_instances(mock_client):
    """
    This function uses mock.patch as a decorator, and replaces (mocks) client of boto3.
    We're testing both happy and unhappy flow
    """

    print('test with more than one instances')
    invoke_response = {'Instances': 
        [
            {
                'InstanceId': 'example-serviceInstance',
                'NamespaceName': 'example-namespace',
                'ServiceName': 'example-service',
                'HealthStatus': 'UNKNOWN',
                'Attributes': {
                    'Arn': 'ExampleArn'
                }
            },
            {
                'InstanceId': 'example-serviceInstance',
                'NamespaceName': 'example-namespace',
                'ServiceName': 'example-service',
                'HealthStatus': 'UNKNOWN',
                'Attributes': {
                    'Arn': 'ExampleArn'
                }
            },                        
        ]
    }
    mock_client.return_value.discover_instances.return_value = invoke_response
    with pytest.raises(IndexError):
        lookup_resource_arn('example-service', 'example-namespace', region)

@mock.patch("service_discovery.client")
def test_lookup_resource_arn_instance_without_arn_attribute(mock_client):
    """
    This function uses mock.patch as a decorator, and replaces (mocks) client of boto3.
    We're testing both happy and unhappy flow
    """

    print('test with instance without arn attribute')
    invoke_response = {'Instances': 
        [
            {
                'InstanceId': 'example-serviceInstance',
                'NamespaceName': 'example-namespace',
                'ServiceName': 'example-service',
                'HealthStatus': 'UNKNOWN',
                'Attributes': {
                }
            },                   
        ]
    }
    mock_client.return_value.discover_instances.return_value = invoke_response
    with pytest.raises(KeyError):
        lookup_resource_arn('example-service', 'example-namespace', region)