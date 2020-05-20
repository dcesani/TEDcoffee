#import delle librerie per PySpark
import sys
import json
import pyspark
from pyspark.sql.functions import col, collect_list, collect_set,  array_join
#collect_list (funzione SQL avanzata) --> crea un array aggregato da una lista sparsa

#import delle librerie per Glue
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

##### FROM FILES
tedx_dataset_path = "s3://ted-coffee-data/tedx_dataset.csv"

###### READ PARAMETERS  standard
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

##### START JOB CONTEXT AND JOB standard
sc = SparkContext()

##inizializzo il job - standard
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)


#### READ INPUT FILES TO CREATE AN INPUT DATASET
tedx_dataset = spark.read.option("header","true") \
    .option("quote", "\"") \
    .option("escape", "\"") \
    .csv(tedx_dataset_path) #per il json avro .json al posto di .csv
    #il \ serve per andare a capo
    #per modificare il separatore .option("separator",";")
    #quote: permette di avere testi con dentro delle virgola 
    #escape
    
tedx_dataset.printSchema()

#### FILTER ITEMS WITH NULL POSTING KEY   -  vanno tutti ad AWS cloudWatch che mostra tutti i log
count_items = tedx_dataset.count() #conteggio
count_items_null = tedx_dataset.filter("idx is not null").count() #guardo se ho dati nulli  (la condizione è come una WHERE)

print(f"Number of items from RAW DATA {count_items}")
print(f"Number of items from RAW DATA with NOT NULL KEY {count_items_null}")


## READ TAGS DATASET
tags_dataset_path = "s3://ted-coffee-data/tags_dataset.csv"
tags_dataset = spark.read.option("header","true").csv(tags_dataset_path)


#DEVO ORA AGGREGARE I DATI E SALVARLI SU MONGODB
# CREATE THE AGGREGATE MODEL, ADD TAGS TO TEDX_DATASET
tags_dataset_agg = tags_dataset.groupBy(col("idx").alias("idx_ref")).agg(collect_list("tag").alias("tags")) #USO LA GROUP BY come in SQL
# collect_list mi restituisce un ARRAY
tags_dataset_agg.printSchema() #controllo se è giusto
#faccio ora un join (un left join)
#.drop tolgo idx_ref
#impongo l'id
#.join(testata con i tag, condizione di join, tipo di join). rinomino poi le id (_id è il classico nome che da MongoDB agli id)
tedx_dataset_agg = tedx_dataset.join(tags_dataset_agg, tedx_dataset.idx == tags_dataset_agg.idx_ref, "left") \
    .drop("idx_ref") \
    .select(col("*")) 
   # .drop("idx") \

tedx_dataset_agg.printSchema()

#leggo il file watch_next_dataset
next_dataset_path = "s3://ted-coffee-data/watch_next_dataset.csv"
next_dataset = spark.read.option("header","true").csv(next_dataset_path)


# CREATE THE AGGREGATE MODEL, ADD next_idx TO TEDX_DATASET
#collect_set dato che non vogliamo duplicati

next_dataset = next_dataset.select("*").where(col("url").like("%com/talks/%"))
next_dataset_agg = next_dataset.groupBy(col("idx").alias("idx_ref")).agg(collect_set("watch_next_idx").alias("next_idx"), collect_set("url").alias("next_url"))
next_dataset_agg.printSchema()


#join con il dataset originario (video+tags)
tedx_dataset_agg = tedx_dataset_agg.join(next_dataset_agg, tedx_dataset_agg.idx == next_dataset_agg.idx_ref, "left") \
    .drop("idx_ref") \
    .select(col("*")) \
    #.drop("idx") \

#ted.com/talks/
tedx_dataset_agg.printSchema()


#leggo il file duration_dataset
duration_dataset_path = "s3://ted-coffee-data/duration_dataset.csv"
duration_dataset = spark.read.option("header","true").csv(duration_dataset_path)

tedx_dataset_agg = tedx_dataset_agg.join(duration_dataset, tedx_dataset_agg.idx == duration_dataset.idx, "left") \
    .select(col("idx").alias("_id"), col("*")) \
    .drop("idx") \

tedx_dataset_agg.printSchema()

mongo_uri = "mongodb://mycluster-shard-00-00-ommtb.mongodb.net:27017,mycluster-shard-00-01-ommtb.mongodb.net:27017,mycluster-shard-00-02-ommtb.mongodb.net:27017"

write_mongo_options = {
    "uri": mongo_uri,
    "database": "TEDcoffeeDB",
    "collection": "tedx_data",
    "username": "TEDcoffee_TEAM",
    "password": "mWxEmLl79RMTNFTG",
    "ssl": "true",
    "ssl.domain_match": "false"}
from awsglue.dynamicframe import DynamicFrame
tedx_dataset_dynamic_frame = DynamicFrame.fromDF(tedx_dataset_agg, glueContext, "nested")

glueContext.write_dynamic_frame.from_options(tedx_dataset_dynamic_frame, connection_type="mongodb", connection_options=write_mongo_options)

