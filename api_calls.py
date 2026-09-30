import sqlite3
import time

import requests

from shared import BASE_DB_PATH, KNOWN_SCRIPTS, normalize_name

WIKI_API = "https://wiki.bloodontheclocktower.com/api.php"
HEADERS = {"User-Agent": "BotCTokenMaker"}


def find_chars(db):
    typelist = {"Townsfolk", "Outsiders", "Minions", "Demons", "Travellers", "Fabled", "Loric"}
    
    
    # save each character
    for category in typelist:
        shouldContinue = True
        cmcontinueVals = None
        continueVals = None

        match category:
            case "Outsiders": singular = "Outsider"
            case "Minions": singular = "Minion"
            case "Demons": singular = "Demon"
            case "Travellers": singular = "Traveller"
            case _: singular = category
    
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
                            """, (page["pageid"], singular, page["title"]))
            
            time.sleep(0.5)

def extract_script(categories, name):
    if categories:
        for cat in categories:
            cat_name = cat["title"].removeprefix("Category:")
            if cat_name in KNOWN_SCRIPTS:
                return cat_name
        seen = [c["title"].removeprefix("Category:") for c in categories]
        print(f"  no known script for {name}, categories were: {seen}")
    return None

            
def get_images(db):
    # now for each character saved,  I need to iterate on them and request each one's img download url
    
    total_chars = db.execute("""
                             SELECT page_id, character_name 
                             FROM characters
                             WHERE script IS NULL
                             """) #WHERE img_url IS NULL
    
    for character in total_chars:
        (id, name) = character
        #special exceptions to usual naming rules for images
        if name.lower() == "big wig":
            file_title = "File:Icon_big_wig.png" #keeps the space for some reason
        else:
            file_title = f"File:Icon_{normalize_name(name)}.png"
        params = {"action" : "query",
                  "format" : "json",
                  "prop" : "imageinfo|categories",
                  "iiprop" : "url",
                  "titles" : f"{name}|{file_title}"}
        
        response = requests.get(WIKI_API, params=params, headers=HEADERS).json()
        pages = list(response["query"]["pages"].values())

        file_page = next((p for p in pages if p.get("title", "").startswith("File:")), None)
        char_page = next((p for p in pages if not p.get("title", "").startswith("File:")), None)

        if file_page is None or "missing" in file_page:
            print(f"Error accessing image on pageid {id} and character name {name}")
            print(file_page)
            continue
            
        #print(chrpage) #use for debugging if error catching isn't good enough
        imgurl = file_page["imageinfo"][0]["url"]
        script = extract_script(char_page.get("categories") if char_page else None, name)
        
        db.execute("""
            UPDATE characters 
            SET img_url = (?), script = (?)
            WHERE page_id = (?)
            """, (imgurl, script, id)) 
        print(f"Found image for {name} (script: {script})")
        
        time.sleep(0.5)

    
def update_db(db):
    find_chars(db)
    db.execute("""
               DELETE FROM characters
               WHERE character_name = ? OR character_name = ?
               """, ("Qutler", "God of Ug (Ug Mode)"))
    db.commit()
    get_images(db)
    db.commit()
    
def print_counts(db):
    #for checking counts
    tf = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Townsfolk'
                    """).fetchone()[0]
    out = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Outsider'
                    """).fetchone()[0]
    mn = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Minion'
                    """).fetchone()[0]
    dem = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Demon'
                    """).fetchone()[0]
    trv = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Traveller'
                    """).fetchone()[0]
    fab = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Fabled'
                    """).fetchone()[0]
    lor = db.execute("""
                    SELECT COUNT(*) FROM characters WHERE character_type = 'Loric'
                    """).fetchone()[0]
    
    print(f"Number breakdown: {tf} Townsfolk, {out} Outsiders, {mn} Minions, {dem} Demons, {trv} Travellers, {fab} Fabled, {lor} Loric")
    

def main():
    db = sqlite3.connect(BASE_DB_PATH)
    db.execute("""CREATE TABLE IF NOT EXISTS characters (
                    page_id         INTEGER PRIMARY KEY,
                    character_name  TEXT,
                    character_type  TEXT,
                    printed         INTEGER DEFAULT 0,
                    svg_made        INTEGER DEFAULT 0,
                    img_url         TEXT DEFAULT NULL,
                    img_filepath    TEXT DEFAULT NULL,
                    script          TEXT DEFAULT NULL
                    )
                """)
    #db.execute("ALTER TABLE characters ADD COLUMN script TEXT DEFAULT NULL")
    db.commit()
    update_db(db)
    print_counts(db)
    
if __name__ == "__main__":
    main()
