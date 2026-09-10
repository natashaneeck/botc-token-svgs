import pandas as pd
import sqlite3


SHARED_DB_PATH = "botc.db"
SEPARATE_DB_PATH = "custom.db"




def read_xlsx(path):
    df = pd.read_excel(path)

def read_csv(path):
    df = pd.read_csv(path)



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
    
if __name__ == "__main__":
    main()


#todo: make template xlsx and csv files, then make settings specific so that pandas can read them, put them into db properly etcetc, check it works with svgmaker.py

# helping source: https://sscc.wisc.edu/sscc/pubs/dwp/Reading_Data.html
