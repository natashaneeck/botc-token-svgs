import svgwrite
from PIL import Image
import sqlite3
import os
import urllib.request
import numpy as np
import base64

DB_PATH = "botc.db"
IMAGE_DIR = "images"
SVG_DIR = "svgs"
FILE_SEPARATOR = os.path.sep

def constructToken(db, name, type, imgPath):
    dwg = svgwrite.Drawing(f"{SVG_DIR}{FILE_SEPARATOR}{name}.svg", profile = 'tiny')

    with open(imgPath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    href = f"data:image/png;base64,{b64}"

    #TODO update insert point and set so it centers horizontally
    img = dwg.image(href,insert=("0.4237in", "0.1905in"), size=("1.5in", "1.5in")) #ensuring it wont overreach: 1.1526in
    img.fit(horiz='center', vert='middle', scale='meet')
    dwg.add(img)
    
    
    circ = dwg.circle(center=("1in", "1in"), r="1in", fill="none", stroke="red", stroke_width="0.001in")
    dwg.add(circ)
    
    #TODO try to get better font
    charName = dwg.text(name,insert=("1in", "1.50in"), fill="black", font_size="16pt", text_anchor="middle", 
                        font_family="Franklin Gothic Book")
    dwg.add(charName)
    
    charType = dwg.text(type,insert=("1in", "1.7in"), fill="black", font_size="12pt", text_anchor="middle",
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
    finalpath = f"{IMAGE_DIR}{FILE_SEPARATOR}{filename}"
    
    urllib.request.urlretrieve(imgUrl, finalpath)
    remove_shadow(finalpath).save(finalpath)

    img = Image.open(finalpath) 
    img = img.convert("LA") 

    source = img.split()
    darkness = source[0].point(lambda i: 0 if i < 200 else 255)
    img = Image.merge("LA", (darkness, source[1]))
    img.save(finalpath)

    return finalpath
    
def remove_shadow(in_path, alpha_thresh=250):
    img = Image.open(in_path).convert('RGBA')
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Shadow is a real (but never fully opaque) alpha gradient.
    # Subject + white sticker outline are fully opaque (alpha ~255).
    mask = alpha >= alpha_thresh

    out = arr.copy()
    out[~mask] = [255, 255, 255, 0]     # keep transparency
    out[mask, 3] = 255

    return Image.fromarray(out, 'RGBA')


def main():
    db = sqlite3.connect(DB_PATH)

    #TODO iterate over db doing greyscaleImg then constructToken, updating db to say token made/where token address is
    imgPath = greyscaleImg(db, "Washerwoman")
    img2Path = greyscaleImg(db, "Preacher")
    constructToken(db, "Washerwoman", "Townsfolk", imgPath)
    constructToken(db, "Preacher", "Townsfolk", img2Path)
    #db.commit()
    
    
if __name__ == "__main__":
    main()
