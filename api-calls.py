import requests
import sqlite3
import time

WIKI_API = "https://wiki.bloodontheclocktower.com/api.php"
HEADERS = {"User-Agent": "BotCTokenMaker"}
DB_PATH = "botc.db"
IMAGE_DIR = "images"


def find_chars(db):
    typelist = {"Townsfolk", "Outsiders", "Minions", "Demons"}
    
    
    # save each character
    for category in typelist:
        shouldContinue = True
        cmcontinueVals = None
        continueVals = None
    
        while shouldContinue:
            #api request with category = current category
            params = {"action" : "query", 
                      "list" : "categorymembers",
                      "cmtitle" : f"Category:{category}",
                      "cmlimit" : "50",
                      "format" : "json"}
            
            if cmcontinueVals is not None:
                contDict = {
                    "cmcontinue" : cmcontinueVals,
                    "continue" : continueVals
                }
                params |= contDict
            
            response = requests.get(WIKI_API, params=params, headers=HEADERS).json()
            if ("continue" not in response):
                shouldContinue = False
            else:
                cmcontinueVals = response["continue"]["cmcontinue"]
                continueVals = response["continue"]["continue"]
            
        
            for page in response["query"]["categorymembers"]:
                db.execute("""
                            INSERT OR IGNORE INTO characters  
                            (page_id, character_type, character_name) 
                            VALUES (?, ?, ?)
                            """, (page["pageid"], category, page["title"]))
            
            time.sleep(0.5)
            
            
def get_images(db):
    # now for each character saved,  I need to iterate on them and request each one's img download url
    
    total_chars = db.execute("""
                             SELECT page_id, character_name 
                             FROM characters
                             WHERE img_found IS NOT 1
                             """)
    
    for character in total_chars:
        (id, name) = character
        params = {"action" : "query",
                  "format" : "json",
                  "prop" : "imageinfo",
                  "iiprop" : "url",
                  "titles" : f"File:Icon_{name.lower().replace(" ", "").replace("-", "").replace("'", "")}.png"}
        
        response = requests.get(WIKI_API, params=params, headers=HEADERS).json()
        
        #get imgurl from proper place, save it
        chrpage = next(iter(response["query"]["pages"].values())) #get first val in pages list
        
        if chrpage is None or "missing" in chrpage:
            print("Error accessing image on pageid %s and character name %s", id, name)
            print(chrpage)
            continue
            
        #print(chrpage) #use for debugging if error catching isn't good enough
        imgurl = chrpage["imageinfo"][0]["url"]
        
        db.execute("""
            UPDATE characters 
            SET img_url = (?), img_found = 1
            WHERE page_id = (?)
            """, (imgurl, id)) 
        print("Found image for ", name)
        
        time.sleep(0.5)

    
def update_db(db):
    find_chars(db)
    db.execute("""
               DELETE FROM characters
               WHERE character_name = ?
               """, ("Qutler",))
    db.commit()
    get_images(db)
    db.commit()
    
def print_counts(db):
    #for checking counts
    tf = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Townsfolk'
                    """).fetchone()[0]
    out = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Outsiders'
                    """).fetchone()[0]
    mn = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Minions'
                    """).fetchone()[0]
    dem = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Demons'
                    """).fetchone()[0]
    
    print(f"Number breakdown: {tf} Townsfolk, {out} Outsiders, {mn} Minions, {dem} Demons")
    

def main():
    db = sqlite3.connect(DB_PATH)
    db.execute("""CREATE TABLE IF NOT EXISTS characters (
                    page_id         INTEGER PRIMARY KEY,
                    character_name  TEXT,
                    character_type  TEXT,
                    printed         INTEGER DEFAULT 0,
                    img_found       INTEGER DEFAULT 0,
                    img_url         TEXT DEFAULT NULL
                    )
                """)
    db.commit()
    update_db(db)
    print_counts(db)
    
if __name__ == "__main__":
    main()
