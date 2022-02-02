import json
import boto3

client = boto3.client('glue')
def lambda_handler(event, context):
    # TODO implement
    response = client.create_job(
    Name='imba_glue_test',
    Description='add glue job through lambda',
    Role='arn:aws:iam::724193151683:role/imba-glue-role',
    ExecutionProperty={
        'MaxConcurrentRuns': 10
    },
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://imba-yiding/scripts/glue_job.py',
        'PythonVersion': '3'
    },
    MaxRetries=0,
    Timeout=2,
    MaxCapacity=10,
    GlueVersion='Glue 2.0',
    NumberOfWorkers=10,
    WorkerType='G.1X'
)
    
    
    return {
        'statusCode': 200
    }