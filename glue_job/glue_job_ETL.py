import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job



def main():

    # create glue context first
    glueContext = GlueContext(SparkContext.getOrCreate())
    
    
    # creating dataframes from existing athena catelog
    up_features = glueContext.create_dynamic_frame.from_catalog(database="prd", table_name="up_features")
    prd_features = glueContext.create_dynamic_frame.from_catalog(database="prd", table_name="prd_features")
    user_features_1 = glueContext.create_dynamic_frame.from_catalog(database="prd", table_name="user_features_1")
    user_features_2 = glueContext.create_dynamic_frame.from_catalog(database="prd", table_name="user_features_2")
    
    # join user features together
    users = Join.apply(user_features_1.rename_field('user_id','user_id1'), user_features_2, 'user_id1', 'user_id').drop_fields(['user_id1'])
    
    # join everything together
    df = Join.apply(Join.apply(up_features, users.rename_field('user_id','user_id1'), 'user_id','user_id1').drop_fields(['user_id1']),
                    prd_features.rename_field('product_id','product_id1'), 'product_id','product_id1').drop_fields(['product_id1'])
          
    # convert glue dynamic dataframe to spark dataframe
    df_spark = df.toDF()
    
    # inte data into one single file
    df_spark.repartition(1).write.mode('overwrite').format('csv').save("s3://***/output", header = 'true')
    
if __name__ == '__main__':
    main()
