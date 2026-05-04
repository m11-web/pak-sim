import pandas as pd
import sqlite3
import os

csv_file = 'data.csv' 
db_file = 'database.db'

if os.path.exists(csv_file):
    print("Database ban raha hai...")
    conn = sqlite3.connect(db_file)
    # 1 lakh records ke liye chunking use kar rahe hain
    for chunk in pd.read_csv(csv_file, chunksize=10000):
        chunk.to_sql('details', conn, if_exists='append', index=False)
    
    # Yahan 'Mobile' column par index banaya hai (M capital)
    conn.execute("CREATE INDEX idx_mobile ON details(Mobile)")
    conn.close()
    print("Mubarak ho! database.db tayyar hai.")
else:
    print("Error: data.csv nahi mili!")
