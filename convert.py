import pandas as pd
import sqlite3
import os

csv_file = 'data.csv' 
db_file = 'database.db'

if os.path.exists(csv_file):
    print("CSV ko Database mein convert kiya ja raha hai...")
    # 1 lakh records ke liye chunking behtar hai
    conn = sqlite3.connect(db_file)
    for chunk in pd.read_csv(csv_file, chunksize=10000):
        chunk.to_sql('details', conn, if_exists='append', index=False)
    
    # Yahan humne 'mobile' column par index banaya hai
    conn.execute("CREATE INDEX idx_mobile ON details(mobile)")
    conn.close()
    print("Mubarak ho! Database tayyar hai.")
else:
    print("Error: data.csv file nahi mili!")
    
