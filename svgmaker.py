import svgwrite
from PIL import Image
import sqlite3
import os
import urllib.request

DB_PATH = "botc.db"
IMAGE_DIR = "images"
FILE_SEPARATOR = os.path.sep

def constructToken(db, name, type, imgPath):
    dwg = svgwrite.Drawing(f"{name}.svg", profile = 'tiny')
    img = dwg.Image(imgPath,insert=("0.4237in", "0.1905in"), size=("1.1526in", "1.1526in"))
    img.fit(horiz='center', vert='middle', scale='meet')
    dwg.add(img)
    
    
    circ = dwg.Circle(center=("1in", "1in"), r="1in", fill="none", stroke="red", stroke_width="0.001in")
    dwg.add(circ)
    
    #how to modify text size/boldness/font?
    charName = dwg.Text(name,insert=("1in", "1.51in"), fill="black", font_size="16pt",
                        font_family="Franklin Gothic Book")
    dwg.add(charName)
    
    charType = dwg.Text(type,insert=("1in", "1.6982in"), fill="black", font_size="12pt",
                        font_family="Franklin Gothic Demi Cond", font_weight="bold")
    dwg.add(charType)
    
    dwg.save()
    
def greyscaleImg(db, name):
    imgUrl = db.execute("""
                             SELECT img_url 
                             FROM characters
                             WHERE character_name IS ?
                             """, (name,)).fetchone()[0]
    
    filename = f"{name.lower().replace(" ", "").replace("-", "").replace("'", "")}.png"
    fullpath = f"{IMAGE_DIR}{FILE_SEPARATOR}{filename}"
    
    urllib.request.urlretrieve(imgUrl, fullpath)
    
    img = Image.open(fullpath)
    img = img.convert("1")  
    img.save(fullpath)
    
    return fullpath
    
    
def main():
    db = sqlite3.connect(DB_PATH)
    imgPath = greyscaleImg(db, "Washerwoman")
    constructToken(db, "Washerwoman", "Townsfolk", imgPath)
    db.commit()
    
    
if __name__ == "__main__":
    main()
