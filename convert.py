import pandas as pd
import sqlite3
import os

csv_file = 'data.csv' # Aapki file ka naam
db_file = 'database.db'

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)
    df.to_sql('details', conn, if_exists='replace', index=False)
    conn.execute("CREATE INDEX idx_num ON details(number)")
    conn.close()
    print("DB Created!")
  
