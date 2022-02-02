import json 
import boto3 
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    database = event['database']
    query_output = event['query_output']
    # TODO implement
    query1 = """
    DROP TABLE IF EXISTS user_features_2
    """
    
    query2 = """
    CREATE TABLE user_features_2 WITH (external_location = 's3://***/features/user_features_2/', format = 'parquet')
    as (SELECT user_id,Count(*) AS user_total_products, Count(DISTINCT product_id) AS user_distinct_products,Sum(CASE WHEN reordered = 1 THEN 1 ELSE 0 END) / Cast(Sum(CASE WHEN order_number > 1 THEN 1 ELSE 0 END) AS DOUBLE) AS user_reorder_ratio
        FROM order_products_prior 
        GROUP BY user_id)
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
