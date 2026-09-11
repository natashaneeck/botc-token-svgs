import pandas as pd
import sqlite3
import openpyxl


SHARED_DB_PATH = "botc.db"
SEPARATE_DB_PATH = "custom.db"


def read_xlsx(path):
    return pd.read_excel(path)

def read_csv(path):
    return pd.read_csv(path)

def add_to_db(db, df):
    for row in range(df.shape[0]):
        name = df.at[row, "Character Name"]
        type = df.at[row, "Type"]
        url = df.at[row, "Image URL"]
        db.execute("""
                    INSERT OR IGNORE INTO characters  
                    (character_name, character_type, img_url) 
                    VALUES (?, ?, ?)
                    """, (name, type, url))
        #print(name, type, url)
    db.commit()

def main():
    db = sqlite3.connect(SEPARATE_DB_PATH) # ask if want separate db, if so, ask for name of script for cleaner storage, assign SEPARATE_DB_PATH to that + .db, and use, otherwise SHARED_DB_PATH
    db.execute("""CREATE TABLE IF NOT EXISTS characters (
                    page_id         INTEGER PRIMARY KEY,
                    character_name  TEXT,
                    character_type  TEXT,
                    printed         INTEGER DEFAULT 0,
                    svg_made        INTEGER DEFAULT 0,
                    img_url         TEXT DEFAULT NULL,
                    img_filepath    TEXT DEFAULT NULL
                    )
                """)
    db.commit()

    df = read_xlsx("fall_of_rome.xlsx")
    add_to_db(db, df)
    
if __name__ == "__main__":
    main()

# helping source: https://sscc.wisc.edu/sscc/pubs/dwp/Reading_Data.html
