# Cloud-based recommendation system

This project is based on cloud services to create data lake, ETL process, train and deploy learning model to implement a recommendation system.

## Purpose

One Web app can return if the consumer will buy the product or not when providing user ID and corresponding product SKU.

## Services

This project will use services:

AWS: lambda function, Step functions, Glue (job,notebook,crawler), Athena, SNS, S3, Sagemaker, IAM, Dynamodb, API Gateway.

Confluent cloud (kafka) for streaming data.


## Project description

1. Create a bucket on S3 as the storage location of the data lake, store the raw data in the bucket (raw data zone), and then return the data after ETL to the same bucket (curated zone).

2. Preview the data, determine the data is useful and meaningful for our project. Use AWS Glue crawler to grab corresponding data catalog (in created database and generated table info). Use Athena to do SQL query. This like Apache Hive, it does not change raw data, but do operations above the raw data.

3. Create and store stream data. Create a kafka topic on Clonfluent cloud and set schema registry for the corresponding stream data, schema sets as ___*confluent_cloud_kafka-->confluent_kafka_topic_schema.json*___. Set the kafka producer as ___*confluent_cloud_kafka-->confluent_kafka_producer_lambda.py*___ to push stream data to corresponding kafka topic in different partitions (because this project does not have exact source giving real stream data, we produce stream data manually). Set the consumer (confluent connector with AWS lambda) as ___*confluent_cloud_kafka-->confluent_kafka_consumer_lambda.py*___ to poll the stream data in kafka topic and store them in Dynamodb table.

4. ETL process. Use lambda function to do data transformation operations based on SQL, corresponding scripts in file ___*lambda_functions(ETL)*___. Create Glue job to integrate new dataset and store in curated zone in data lake, scripts is in ___*glue_job-->glue_job_ETL.py*___. Use step fuctions to orchestrate ETL workflow based on above lambda functions, ASL script is in ___*step_function(workflow)-->step_functions_for_curated.json*___.

    This part is based on spark, and it is similar with the project in repo: https://github.com/Yi-Ding111/spark-ETL-based-databricks-aws. 

5. Train learning model (XGBoost). Use sagemaker notebook instance to do some kinds more operations like: EDA and feature engineering, use XGBoost framework to train the data, adjust parameters and try different attributes combinations to find the best one. Scripts is in ___*sagemaker-->xgboost_deploy_sagemaker.ipynb*___.

6. Deploy learning model. Get deploy endpoint after machine learning. Create lambda function to invoke the sagemaker endpoint to use the trained model, scripts is in ___*sagemaker-->endpoint_interact_lambda.py*___. Let the lambda function integrate with API gatway (proxy integration) as the backend. Deploy the API gatewat and use the invoked URL for web applications to do interactions.

7. Store the application output. Use SNS to publish the output to lambda and update the information into Dynamodb table, scripts is in ___*sagemaker-->prediction_store_dynamodb.py*___

___

## Acknowledgement

This project is completed with the guidance from Leo Lee (JR academy)

___

Author: YI DING, Leo Lee

Created at: Dec 2021

Contact: dydifferent@gmail.com

