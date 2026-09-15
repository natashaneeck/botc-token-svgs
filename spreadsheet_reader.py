import sqlite3

import openpyxl
import pandas as pd


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

def main(filepath, script_name, xlsx:bool):
    db = sqlite3.connect(f"{script_name}.db")
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

    if xlsx:
        df = read_xlsx(filepath)
    else:
        df = read_csv(filepath)
    add_to_db(db, df)
    
if __name__ == "__main__":
    main()

# helping source: https://sscc.wisc.edu/sscc/pubs/dwp/Reading_Data.html
