import json 
import boto3 
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    database = 'prd'
    query_output = 's3://*****/query_results/'
    # TODO implement
    query1 = """
    DROP TABLE IF EXISTS up_features
    """
    
    query2 = """
    CREATE TABLE up_features WITH (external_location = 's3://***/features/up_features/', format = 'parquet')
    as (SELECT user_id, product_id,Count(*) AS up_orders,Min(order_number) AS up_first_order, Max(order_number) AS up_last_order, Avg(add_to_cart_order) AS up_average_cart_position
        FROM order_products_prior 
        GROUP BY user_id,product_id)
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
