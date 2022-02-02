import json
import boto3
def lambda_handler(event, context):
    # TODO implement
    bucket = 'imba-yiding'
    prefix = 'features/'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    
    for key in bucket.objects.filter(Prefix=prefix):
        key.delete() 
    
    return {
        'statusCode': 200 
    }
