#as the publisher of kafka topic
from confluent_kafka import Producer
#from confluent_kafka.schema_registry import RegisteredSchema
import boto3
import io
import gzip
import logging
import urllib.parse
import os
import time
import json
import os
import re
import boto3


s3=boto3.client('s3')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


#confluent cluster API KEY SECRET to connect confluent kafka topic
cf_key=os.environ['APIKEY']
cf_sec=os.environ['APISECRET']


prod = Producer({
               'bootstrap.servers': 'pkc-ldvj1.ap-southeast-2.aws.confluent.cloud:9092',
               'batch.num.messages': 500,
                'linger.ms':5,
               'compression.type':'zstd',
               'security.protocol': 'SASL_SSL',
               'sasl.mechanisms' : 'PLAIN',
               'sasl.username': cf_key,
               'sasl.password': cf_sec     
                })




def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        pass
        #logging.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))




def lambda_handler(event, context):
    

                 

    s3 = boto3.client('s3')
    s3.download_file('imba-yiding', 'model_output/test_final.csv', '/tmp/test_final.csv')
    with open('/tmp/test_final.csv', 'r') as f:
        i = 0
        for line in f:
            #print(line)
            tokens = line.split(',',2)
            prod.produce('imba-yiding', value = json.dumps({'user_id':tokens[1], 'product_id':tokens[0],'feature':tokens[2].rstrip()}) , on_delivery = None, callback=delivery_report)
            i += 1
            if i == 1000:
                break

    prod.poll(0)

    
    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    prod.flush()
   
   
    return {'submit' : 'ok'}
