# Example Consumer Step Functions State Machine for AWS event-driven microservices Service Discovery

## Context
See [repo README](../README.md)

### Consumer Step Functions State Machine
The State machine has a state task that wants to invoke the Lambda service. Since a state machine cannot do Cloud Map lookup before invoking a Lambda in a state task, we use a small plumbing 'connector' lambda that does the discovery lookup and invokes the Lambda with the given event from the state machine. 
