import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession, functions as F, Window
from pyspark.sql.types import *

spark_session = SparkSession\
        .builder\
        .master("spark://spark-master:7077") \
        .appName("Popular_Journals")\
        .getOrCreate()

sc = spark_session.sparkContext
sqlContext = SQLContext(spark_session.sparkContext)

# load combined citation data
df = sqlContext.read.csv("hdfs://192.168.2.118:9000/user/ubuntu/replicate_data/SCOPUS_DATA_6x.csv",header='true',inferSchema='true').cache()
df = df.select("year", "Title", "Publisher", "Citation Count", "Scopus ASJC Code (Sub-subject Area)")
df = df.withColumnRenamed("Title", "Journal")
df = df.withColumnRenamed("Scopus ASJC Code (Sub-subject Area)", "ASJC Code")

aggregated_df=df.groupBy("year","Journal").agg(
    F.sum("Citation Count").alias("Total Citations"),
    F.first("Publisher").alias("Publisher"),
    F.first("ASJC Code").alias("ASJC Code")
)

windowSpec=Window.partitionBy("year").orderBy(F.desc("Total Citations"))
ranked_journals_df=aggregated_df.withColumn("Rank", F.rank().over(windowSpec))
# filter for the most cited journals each year
most_cited_df=ranked_journals_df.filter(ranked_journals_df.Rank==1)

# join to get the subject area
code_df = sqlContext.read.csv('hdfs://192.168.2.118:9000/user/ubuntu/input/ASJC_code.csv',header='true',inferSchema='true')
code_df = code_df.withColumnRenamed('Description','Subject Area')
code_df = code_df.select(code_df["ASJC Code"],code_df["Subject Area"])

final_df=most_cited_df.join(
    code_df,
    most_cited_df["ASJC Code"]==code_df["ASJC Code"],
    "left"
).select(most_cited_df["year"],
         most_cited_df["Journal"],
         code_df["Subject Area"],
         most_cited_df["Publisher"])

final_df=final_df.withColumnRenamed("year","Year")
final_df=final_df.orderBy("Year")
final_df.show(truncate=False)

sc.stop()