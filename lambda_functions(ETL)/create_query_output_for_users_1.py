import json 
import boto3 
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    database = 'prd'
    query_output = 's3://**********/query_results/'
    # TODO implement
    query1 = """
    DROP TABLE IF EXISTS user_features_1
    """
    
    query2 = """
    CREATE TABLE user_features_1 WITH (external_location = 's3://***/features/user_features_1/', format = 'parquet')
    as (SELECT user_id,
               Max(order_number) AS user_orders,
               Sum(days_since_prior_order) AS user_period,
               Avg(days_since_prior_order) AS user_mean_days_since_prior
       FROM orders 
       GROUP BY user_id )
    """
    
    response1 = athena_client.start_query_execution(
        QueryString=query1, 
        QueryExecutionContext={
            'Database': database 
        },
        ResultConfiguration={ 
            'OutputLocation': query_output
        } 
    )
    
    # sleep 10 seconds to make sure the table is successfully dropped 
    time.sleep(10)
    
    response2 = athena_client.start_query_execution( 
        QueryString=query2,
        QueryExecutionContext={
            'Database': database 
        },
    ResultConfiguration={ 
        'OutputLocation': query_output
        } 
    )
    
    # get the query execution id
    execution_id = response2['QueryExecutionId']
    
    while True:
        stats = athena_client.get_query_execution(QueryExecutionId=execution_id) 
        status = stats['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(0.2) # 200ms
        
    return {
        'statusCode': status
    }
