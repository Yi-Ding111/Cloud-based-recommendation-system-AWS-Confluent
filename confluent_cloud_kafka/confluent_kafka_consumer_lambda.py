#polling kafka streaming data and store into dynamo db
import json
import re
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dynamo-yiding')

def lambda_handler(event, context):
    #print(event)
    #print(event[0]['payload']['value'])
    
    #reduce the number of write requests
    with table.batch_writer() as batch:
        for values in event:
            value = values['payload']['value']
            #regular expression to find fixed value
            user_id = re.search(r"user_id=(.*), product_id", value).group(1)
            product_id = re.search(r"product_id=(.*)\}", value).group(1)
            feature = re.search(r"feature=(.*)\,\ user_id",value ).group(1)
            #print(user_id,product_id,feature)
            
            #put records into dynamodb table
            batch.put_item(
                Item={
                    'user_id': user_id,
                    'product_id': product_id,
                    'feature': feature
                }
            )
            break

    return {
        'statusCode': 200
    }
