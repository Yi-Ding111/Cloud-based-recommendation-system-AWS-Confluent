#put the prediction attribute into record
import json
import re
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dynamo-yiding')


def lambda_handler(event, context):
    # TODO implement
    #print(event)
    
    #read sns event to get info
    message=json.loads(event["Records"][0]["Sns"]["Message"])
    
    user_id=str(message['user_id'])
    product_id=str(message['product_id'])
    feature=str(message['feature'])
    prediction=Decimal(float(message['prediction']))
    
    
    #update record in dynamo db
    table.put_item(Item={'user_id': user_id,'product_id': product_id,'feature':feature,'prediction': prediction})