import pandas as pd
import os
from glob import glob

def concatenate_and_clean_csv_files(folder_path):
    """
    Get all the csv files, concatenate them and clean them in order to get at the end a concatenated and clean file"""
    # 2. Get all csv files in this folder
    csv_files = glob(os.path.join(folder_path, "*.csv"))
    # 3. Read and concatenate all the files
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, sep=";")
            df = df.loc[0:199] # Only keep the 200 first LocationReference
            dfs.append(df)  # Add each DataFrame to the list dfs.
        except Exception as e:
            print(f"Error with {file} : {e}")

    # 4. Concatenate all DataFrames line by line
    if dfs:
        combined_df = pd.concat(dfs, axis=0, ignore_index=True)
        # drop potential duplicates
        combined_df = combined_df.drop_duplicates()
        # Clean columns names
        combined_df.columns = combined_df.columns.str.strip()
        # Define the Dtypes of the series
        combined_df["datetime"] = pd.to_datetime(combined_df["datetime"])
        for column in ["averageVehicleSpeed", "travelTime", "travelTimeReliability", "vehicleProbeMeasurement"] :
            combined_df[column] = combined_df[column].astype("int16")

        # 6. save in a parquet file
        combined_df.to_parquet(r"C:\Users\henin\OneDrive\Documents\Coding\My Portfolio\Projects\project4\data\Concatenated_file\final_concatenated_file.parquet", index=False, engine="pyarrow")
        print("✅ Concatenated file updated")
    else:
        print("❌ No CSV file found.")
    return None

concatenate_and_clean_csv_files(folder_path="C:/Users/henin/OneDrive/Documents/Coding/My Portfolio/Projects/project4/data/raw_data")