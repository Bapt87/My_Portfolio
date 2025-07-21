import psycopg2 as pg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='C:/Users/henin/OneDrive/Documents/Coding/My Portfolio/Projects/project4/.gitignore/.env')

try:
    conn = pg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("✅ Successful connection")
except Exception as e:
    print("❌ Error :", e)

try :
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS road_traffic_Rennes(" \
        "datetime TIMESTAMP WITH TIME ZONE NOT NULL," \
        "predefinedLocationReference VARCHAR(50) NOT NULL," \
        "averageVehicleSpeed SMALLINT," \
        "travelTime SMALLINT," \
        "travelTimeReliability SMALLINT," \
        "trafficStatus VARCHAR(50) NOT NULL," \
        "vehicleProbeMeasurement SMALLINT" \
        ")"
    )
except Exception as e:
    print("Database creation error :", e)
    raise

try :
    df = pd.read_parquet(r"C:\Users\henin\OneDrive\Documents\Coding\My Portfolio\Projects\project4\data\Concatenated_file\final_concatenated_file.parquet", engine="pyarrow")
except Exception as e:
    print("Parquet file read error :", e)
    raise

try :
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO road_traffic_Rennes (datetime, predefinedLocationReference, averageVehicleSpeed, travelTime, travelTimeReliability, trafficStatus, vehicleProbeMeasurement)" \
            "VALUES" \
            "(%s, %s, %s, %s, %s, %s, %s);",
            (row['datetime'], row['predefinedLocationReference'], int(row['averageVehicleSpeed']), int(row['travelTime']), int(row['travelTimeReliability']), row['trafficStatus'], int(row['vehicleProbeMeasurement']))
        )
except Exception as e:
    print("Error sending requests :", e)
    raise

# Commit and close
conn.commit()
cur.close()
conn.close()