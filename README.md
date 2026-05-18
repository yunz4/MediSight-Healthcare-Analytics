# 🏥 MediSight — Healthcare BI & Predictive Analytics Platform

End-to-end data pipeline for healthcare analytics and disease risk prediction.

## 🏗️ Architecture
Raw Data (CSV) → HDFS Data Lake → Spark ETL → MySQL Data Warehouse → ML Models → Power BI Dashboard

## 📊 Dataset
- Pima Indians Diabetes Dataset — 768 patients
- Heart Disease Cleveland Dataset — 302 patients (after deduplication)
- Total processed : 1,788 records

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Data Lake | Hadoop HDFS 3.3.6 |
| ETL | Apache Spark 3.1.2 (PySpark) |
| Data Warehouse | MySQL 9.2 — Star Schema |
| Machine Learning | Scikit-learn, Pandas |
| BI Dashboard | Power BI Desktop |
| Environment | Windows, Java 8, Anaconda |

## 🤖 ML Results
| Model | Dataset | AUC |
|---|---|---|
| Gradient Boosting | Diabetes | 0.8259 |
| Random Forest | Heart Disease | 0.8680 |

## 📁 Project Structure
MediSight/
├── etl/
│   ├── etl_healthcare.py    # Spark ETL pipeline
│   └── load_mysql.py        # MySQL loader
├── ml/
│   └── ml_v2.py             # ML training (5 models)
├── sql/
│   └── schema.sql           # Star schema DDL
└── README.md


## 🚀 How to Run
1. Start HDFS : `start-dfs.cmd`
2. Run ETL : `spark-submit etl/etl_healthcare.py`
3. Load MySQL : `spark-submit --jars mysql-connector.jar etl/load_mysql.py`
4. Train ML : `python ml/ml_v2.py`
5. Open Power BI and connect to MySQL healthcare_db