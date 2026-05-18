import os
os.environ["JAVA_HOME"] = "C:\\PROGRA~1\\ECLIPS~1\\JDK-80~1.9-H"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder \
    .appName("LoadMySQL") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    .config("spark.jars", "C:/tools/mysql/current/lib/mysql-connector-j-9.2.0.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Lecture des données Parquet depuis HDFS
df = spark.read.parquet("hdfs://localhost:9000/healthcare/clean/patients")

print("Données chargées depuis HDFS :", df.count(), "lignes")
df.show(5)

# Ajout des clés étrangères
df_final = df \
    .withColumn("disease_id", when(col("disease_type") == "Diabetes", 1).otherwise(2)) \
    .withColumn("age_group_id",
        when(col("age") <= 30, 1)
        .when(col("age") <= 50, 2)
        .otherwise(3)) \
    .select("age", "bmi", "glucose", "disease_id", "age_group_id", "label")

# Chargement dans MySQL
jdbc_url = "jdbc:mysql://localhost:3306/healthcare_db?useSSL=false&allowPublicKeyRetrieval=true"
props = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.cj.jdbc.Driver"
}

df_final.write.jdbc(url=jdbc_url, table="fact_patients", mode="append", properties=props)

print("Données chargées dans MySQL avec succès !")
spark.stop()