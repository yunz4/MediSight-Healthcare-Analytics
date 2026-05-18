import os
os.environ["JAVA_HOME"] = "C:\\PROGRA~1\\ECLIPS~1\\JDK-17~1.10-"
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--conf spark.driver.extraJavaOptions="
    "'--add-opens java.base/java.nio=ALL-UNNAMED "
    "--add-opens java.base/sun.nio.ch=ALL-UNNAMED "
    "--add-opens java.base/java.lang=ALL-UNNAMED "
    "--add-opens java.base/java.util=ALL-UNNAMED' "
    "pyspark-shell"
)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder \
    .appName("HealthcareETL") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Reading datasets from HDFS...")

diabetes = spark.read.csv("hdfs://localhost:9000/healthcare/raw/diabetes.csv",
                          header=True, inferSchema=True)
heart = spark.read.csv("hdfs://localhost:9000/healthcare/raw/heart.csv",
                       header=True, inferSchema=True)

print("Diabetes colonnes:", diabetes.columns)
print("Heart colonnes:", heart.columns)
print("Diabetes lignes:", diabetes.count())
print("Heart lignes:", heart.count())

diabetes_clean = diabetes \
    .fillna(0) \
    .withColumn("age", col("Age").cast("int")) \
    .withColumn("bmi", col("BMI").cast("double")) \
    .withColumn("glucose", col("Glucose").cast("double")) \
    .withColumn("disease_type", lit("Diabetes")) \
    .withColumn("label", col("Outcome").cast("int")) \
    .where(col("Glucose") > 0) \
    .select("age", "bmi", "glucose", "disease_type", "label")

heart_clean = heart \
    .dropna(subset=["target"]) \
    .withColumn("age", col("age").cast("int")) \
    .withColumn("bmi", lit(None).cast("double")) \
    .withColumn("glucose", lit(None).cast("double")) \
    .withColumn("disease_type", lit("Heart Disease")) \
    .withColumn("label", col("target").cast("int")) \
    .select("age", "bmi", "glucose", "disease_type", "label")

combined = diabetes_clean.union(heart_clean)

print("\nLignes combinées:", combined.count())
combined.show(10)

combined.write.mode("overwrite").parquet("hdfs://localhost:9000/healthcare/clean/patients")

print("\nETL terminé ! Données sauvegardées dans HDFS.")
spark.stop()