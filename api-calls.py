import requests
import sqlite3
import time
import os

WIKI_API = "https://wiki.bloodontheclocktower.com/api.php"
HEADERS = {"User-Agent": "BotCTokenMaker"}
DB_PATH = "botc.db"
IMAGE_DIR = "images"

def init_db(conn):
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
            
            response = requests.get(WIKI_API, params).json()
            if ("continue" in response["query"]):
                shouldContinue = False
            else:
                cmcontinueVals = response["query"]["continue"]["cmcontinue"]
                continueVals = response["query"]["continue"]["continue"]
            
            
            #save result in sqlite, probably saving pageid, character type, and title. 
            # I want to initialize any new entries to "printed" = false & imgfound = false
            
    # now for each character saved,  I need to iterate on them and request each one's img download url
    for character in database:
        params = {"action" : "query",
                  "format" : "json",
                  "prop" : "imageinfo",
                  "iiprop" : "url",
                  "titles" : f"File:Icon_{character.lower()}.png"}
        
        response = requests.get(WIKI_API, params).json()
        
        #get imgurl from proper place, save it
        chrpage = next(iter(response["query"]["pages"].values())) #get first val in pages list
        imgurl = chrpage["imageinfo"][0]["url"]
        
            
        #if pagekey = -1, log an error because couldnt find the page
    
    conn.execute("""
                 
                 
                 """)

def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)