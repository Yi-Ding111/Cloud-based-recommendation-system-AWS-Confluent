import json
import boto3

client=boto3.client('stepfunctions')

def lambda_handler(event, context):
    # TODO implement

    #get the event info from API gateway
    #record=str(json.dumps(event['body']))
    record=event['body']
    #print(record)

    response = client.start_execution(
    stateMachineArn='arn:aws:states:ap-southeast-2:724193151683:stateMachine:API_prediction_SF',
    name='API_prediction_record',
    input="{\"record\" :\"" + record + "\"}"
    ) 