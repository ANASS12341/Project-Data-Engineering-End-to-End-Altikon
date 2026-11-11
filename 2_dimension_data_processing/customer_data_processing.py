# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %run ./utilities

# COMMAND ----------

dbutils.widgets.text("catalog","fcmg","Catalog")
dbutils.widgets.text("datasource","customers","Datasource")

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
datasource = dbutils.widgets.get("datasource")

# we will difine the path to the data source 

base_path = f"/Volumes/fmcg/bronze/sportbar_landing/customers/{datasource}.csv"

# COMMAND ----------

# know we will create a dataframe from the data source
df = (spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(base_path)
.withColumn("read_timestamp", F.current_timestamp())
.select("*","_metadata.file_name","_metadata.file_size")
)
display(df.limit(10))

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.write\
    .format("delta") \
    .option("delta.enableChangeDataFeed","true") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{datasource}")

# COMMAND ----------

