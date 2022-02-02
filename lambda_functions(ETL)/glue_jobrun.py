import json
import boto3

client = boto3.client('glue')

def lambda_handler(event, context):
    # TODO implement
    response = client.start_job_run(
    JobName='imba-glue'
    )
    
    return{
    'JobRunId': '200'
    }
    