# let lambda as backend integration with API gateway
import boto3
import json

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('dynamo-yiding')
sns=boto3.client('sns')

def lambda_handler(event, context):

    # get event from REST API 
    body=event['body']
    #print(event)
    #print(body)
    #give the input value from web server
    user_id=body.split(',')[0]
    product_id=body.split(',')[1]

    #get the record from dynamo db based on given partitioned key and sorted key
    input_value=table.get_item(Key={'user_id':user_id,'product_id':product_id})
    record=input_value['Item']['feature']
    # invoke the endpoint 
    runtime = boto3.Session().client('sagemaker-runtime')

    #interact with sagemaker endpoint to get prediction
    response = runtime.invoke_endpoint(EndpointName = 'xgboost-2022-01-24-13-33-20-946',
                                       ContentType = 'text/csv',                 
                                       Body = record
                                       )

    # decode output
    result = response['Body'].read().decode('utf-8')

    # Round the result so that our web app only gets '1' or '0' as a response.
    result = float(result)
    #print(result)
    
    
    
    # send output as publisher for SNS to store in dynamoDB
    notification={
        'user_id':user_id,
        'product_id':product_id,
        'feature':record,
        'prediction':result
    }
    
    response=sns.publish(
        TargetArn='arn:aws:sns:ap-southeast-2:724193151683:add_dynamo_attr',
        Message =json.dumps({'default': json.dumps(notification)}),
        MessageStructure='json'
        
        )
    
    
    
    
    
    
    return {
        'statusCode' : 200,
        'body' : str(result)
    }
