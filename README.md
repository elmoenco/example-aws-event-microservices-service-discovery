# Example for AWS event-driven microservices Service Discovery

## Context
In AWS event-driven microservice architecture services are not perse exposed by a REST API, but by an ARN resource endpoint. 
This entrypoint needs to be discoverable, and we can do that through Service Discovery. 
This example uses [*AWS Cloud Map Service Discovery*](https://aws.amazon.com/cloud-map/).

With endpoint service discovery we do not need to enforce order of service deployment or tighly coupled endpoint lookup's during deployment (for instance Outputs from terraform state or Cloudformation). 

## Service Discovery design

### Overall approach
1. Create a namespace in Cloud Map
2. Define a service. Make sure there is some kind of naming convention for microservices in the architecture. 
3. Register a service instance to the service with the instance ARN resource endpoint. This can be done during deployment.
4. Whenever a consuming resource or services wants to invoke the registered service, first do a service discovery lookup and retreive the instance ARN resource endpoint.

### Cloud Map API namespace 
Since were event-driven based, we must use an Cloud Map 'API' discovery namespace, not a DNS discovery namespace.

### Single Instance per Service
There is no need for multiple instances per service in this design.

### Instance attributes
Every instance should have a instance attribute 'Arn' that contains the resource ARN as a string. 

## Example code
This example exists of 3 [SAM applications](https://aws.amazon.com/serverless/sam/) :

### Lambda service
When invoked, it returns a simple hello world message.
The SAM template creates the Service, deploys the Lambda function, and registers the Lambda function as an Instance.

### Consumer Lambda
This Consumer Lambda wants to invoke the Lambda service by doing a service discovery lookup, retreive the instance ARN resource endpoint and invoke the Lambda service.

### Consumer Step Functions State Machine
The State machine has a state task that wants to invoke the Lambda service. Since a state machine cannot do Cloud Map lookup before invoking a Lambda in a state task, we use a small plumbing 'connector' lambda that does the discovery lookup and invokes the Lambda with the given event from the state machine. 
