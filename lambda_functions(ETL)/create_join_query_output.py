import json 
import boto3 
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    database = 'prd' # glue catalog database
    query_output = 's3://*****/query_results/'

    query1 = """
    DROP TABLE IF EXISTS order_products_prior
    """
    
    #create table in athena, store shcema in data catalog
    #saves CTAS query in Amazon S3
    query2 = """
        CREATE TABLE order_products_prior WITH (external_location = 's3://***/features/order_products_prior/', format = 'parquet')
        as (SELECT a.*, b.product_id,
                   b.add_to_cart_order,
                   b.reordered
            FROM orders a
            JOIN order_products b
            ON a.order_id = b.order_id
            WHERE a.eval_set = 'prior')
    """
    #drop table
    response1 = athena_client.start_query_execution(
        QueryString=query1, 
        QueryExecutionContext={
            'Database': database 
        },
        ResultConfiguration={ 
            #put query output into s3
            'OutputLocation': query_output
        } 
    )
    
    # sleep 10 seconds to make sure the table is successfully dropped 
    time.sleep(10)
    
    #ETL
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
