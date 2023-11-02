import findspark
findspark.init()
from pyspark.sql.functions import col, regexp_replace
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
SparkSession.builder.config(conf=SparkConf())
from pyspark.sql.functions import sha2,concat_ws, datediff, current_date,to_date, round
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType,BinaryType
from pyspark.sql.functions import from_json,explode
from cassandra.cluster import Cluster

spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4") \
    .getOrCreate()



df = spark.readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "randomuser_data") \
  .option("startingOffsets", "earliest") \
  .load()


value_df = df.selectExpr("CAST(value AS STRING)")



data_schema = StructType([
    StructField("results", ArrayType(
        StructType([
            StructField("gender", StringType(), True),
            StructField("name", StructType([
                StructField("title", StringType(), True),
                StructField("first", StringType(), True),
                StructField("last", StringType(), True)
            ]), True),
            StructField("location", StructType([
                StructField("street", StructType([
                    StructField("number", IntegerType(), True),
                    StructField("name", StringType(), True)
                ]), True),
                StructField("city", StringType(), True),
                StructField("state", StringType(), True),
                StructField("country", StringType(), True),
                StructField("postcode", IntegerType(), True),
                StructField("coordinates", StructType([
                    StructField("latitude", StringType(), True),
                    StructField("longitude", StringType(), True)
                ]), True),
            ]), True),
            StructField("email", StringType(), True),
            StructField("login", StructType([
                StructField("uuid", StringType(), True),
                StructField("username", StringType(), True),
                StructField("password", StringType(), True)
            ]), True),
            StructField("dob", StructType([
                StructField("date", StringType(), True),
                StructField("age", IntegerType(), True)
            ]), True),
            StructField("registered", StructType([
                StructField("date", StringType(), True),
                StructField("age", IntegerType(), True)
            ]), True),
            StructField("phone", StringType(), True),
            StructField("cell", StringType(), True),
            StructField("nat", StringType(), True)
        ]), True),
    True)
])


selected_df = value_df.withColumn("values", from_json(value_df["value"], data_schema)).selectExpr("explode(values.results) as results_exploded")

result_df = selected_df.select(
    F.col("results_exploded.login.uuid").alias("id"),
    F.col("results_exploded.gender").alias("gender"),
    F.col("results_exploded.name.title").alias("title"),
    concat_ws(" ",
            F.col("results_exploded.name.last"),
            F.col("results_exploded.name.first")).alias("fullname"),
    F.col("results_exploded.login.username").alias("username"),
    F.col("results_exploded.email").alias("email"),
    F.col("results_exploded.phone").alias("phone"),
    concat_ws(", ",
            F.col("results_exploded.location.city"),
            F.col("results_exploded.location.state"),
            F.col("results_exploded.location.country")).alias("address"),
    round(datediff(current_date(), to_date(F.col("results_exploded.dob.date")))/365).alias("age"),
    F.col("results_exploded.registered.date").alias("inscription"),
    F.col("results_exploded.nat").alias("nationality")
)

#  encrypt  email,passowrd,phone,cell using SHA-256
result_df = result_df.withColumn("email", sha2(result_df["email"], 256))
result_df = result_df.withColumn("phone", sha2(result_df["phone"], 256))



query = result_df.writeStream.outputMode("append").format("console").start()
query.awaitTermination()
