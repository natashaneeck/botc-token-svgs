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
TOKEN_SIZE = 2.0  # inches -- matches the circle's diameter

def embed_fonts(dwg):
    dwg.embed_font("Franklin Gothic Book", "fonts/Franklin Gothic Book.ttf")
    dwg.embed_font("Franklin Gothic Demi Cond", "fonts/Franklin Gothic Demi Cond.ttf")

def build_sheet(db, tokens, board_width_in, board_height_in, out_path):
    cols = max(1, int(board_width_in // TOKEN_SIZE))
    dwg = svgwrite.Drawing(out_path, size=(f"{board_width_in}in", f"{board_height_in}in"), profile='full')
    # embed_fonts(dwg) bring back later

    placed = 0
    for i, (name, char_type, imgPath) in enumerate(tokens):
        col, row = i % cols, i // cols
        x, y = col * TOKEN_SIZE, row * TOKEN_SIZE
        if y + TOKEN_SIZE > board_height_in:
            print(f"Board full after {placed} tokens ({cols} cols x {row} rows) — {placed} placed so far, start a new sheet for next {len(tokens) - placed}")
            break
        add_token(dwg, x, y, name, char_type, imgPath)
        placed += 1
        db.execute("UPDATE characters SET svg_made = 1 WHERE character_name = (?)", (name,))

    dwg.save()
    return placed

def add_token(dwg, x, y, name, char_type, imgPath):
    token = dwg.svg(insert=(f"{x}in", f"{y}in"), size=(f"{TOKEN_SIZE}in", f"{TOKEN_SIZE}in"))
    dwg.add(token)

    with open(imgPath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    href = f"data:image/png;base64,{b64}"

    img_size = 1.65
    circle_center = 1.0
    nudge_up = 0.2 #increase this to move image higher up
    insert_x = circle_center - img_size / 2 #horizontally centering the image
    insert_y = circle_center - img_size / 2 - nudge_up #vertically centering the image and then moving it a bit up to avoid text overlap

    #TODO try to get better font
    # https://www.fontspace.com/secrilka-font-f130492
    # https://www.fontspace.com/notulen-serif-font-f76247
    # https://www.fontspace.com/panforte-serif-font-f24708
    img = dwg.image(href, insert=(f"{insert_x}in", f"{insert_y}in"), size=(f"{img_size}in", f"{img_size}in"))
    img.fit(horiz='center', vert='middle', scale='meet')
    token.add(img)

    token.add(dwg.circle(center=("1in", "1in"), r="1in", fill="none", stroke="red", stroke_width="0.001in"))
    token.add(dwg.text(name, insert=("1in", "1.51in"), fill="black", font_size="16pt",
                        font_family="Franklin Gothic Book", text_anchor="middle"))
    token.add(dwg.text(char_type, insert=("1in", "1.6982in"), fill="black", font_size="12pt",
                        font_family="Franklin Gothic Demi Cond", font_weight="bold", text_anchor="middle"))
    
def greyscaleImg(db, name, imgUrl):
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

    db.execute("""
                UPDATE characters 
                SET img_filepath = (?)
                WHERE character_name = (?)
                """, (finalpath, name)) 

    return finalpath
    
def remove_shadow(in_path, alpha_thresh=250):
    img = Image.open(in_path).convert('RGBA')
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Shadow is an (never fully opaque) alpha gradient.
    # Icon + white stickery outline are fully opaque (alpha ~255).
    mask = alpha >= alpha_thresh

    out = arr.copy()
    out[~mask] = [255, 255, 255, 0]     # keep transparency
    out[mask, 3] = 255

    return Image.fromarray(out, 'RGBA')


def main():
    db = sqlite3.connect(DB_PATH)

    to_greyscale = db.execute("""
                             SELECT character_name, img_url 
                             FROM characters
                             WHERE img_filepath IS NULL AND img_url IS NOT NULL
                             """)
        
    for character in to_greyscale:
        (name, url) = character
        greyscaleImg(db, name, url)
    db.commit()

    db.execute("UPDATE characters SET svg_made = 0")

    board_count = 1
    done = False
    while not done:
        to_tokenize = db.execute("""
                                SELECT character_name, character_type, img_filepath 
                                FROM characters
                                WHERE svg_made IS 0 AND img_filepath IS NOT NULL
                                """).fetchall()

        if not to_tokenize:
            done = True
            break
        build_sheet(db, to_tokenize, 24, 12, f"{SVG_DIR}{FILE_SEPARATOR}board_{board_count}.svg")
        db.commit()
        board_count += 1
    
    
if __name__ == "__main__":
    main()
