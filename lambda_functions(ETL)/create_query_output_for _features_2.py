import json 
import boto3 
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    database = 'prd'
    query_output = 's3://*****/query_results/'
    # TODO implement
    query1 = """
    DROP TABLE IF EXISTS prd_features
    """
    
    query2 = """
    CREATE TABLE prd_features WITH (external_location = 's3://***/features/prd_features/', format = 'parquet')
    as (SELECT product_id,Count(*) AS prod_orders,Sum(reordered) AS prod_reorders,
        Sum(CASE WHEN product_seq_time = 1 THEN 1 ELSE 0 END) AS prod_first_orders, Sum(CASE WHEN product_seq_time = 2 THEN 1 ELSE 0 END) AS prod_second_orders
        FROM (SELECT *, Rank()OVER (partition BY user_id, product_id ORDER BY order_number) AS product_seq_time
              FROM order_products_prior)
        GROUP BY product_id)
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
