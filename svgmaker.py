import base64
import os
import sqlite3
import urllib.request

import numpy as np
import svgwrite
from PIL import Image

from shared import (
    BASE_DB_PATH,
    BASE_IMAGE_DIR,
    BASE_SVG_DIR,
    TOKEN_BUFFER,
    TOKEN_SIZE,
    embed_fonts,
    ensure_dir,
    normalize_name
)

CUSTOM_DB_PATH = "custom.db"
CUSTOM_IMAGE_DIR = "custom_images"
CUSTOM_SVG_DIR = "custom_svgs"

# Ratios from the values that worked at TOKEN_SIZE = 2in so that we can actually do dynamic scaling now
IMG_SIZE_RATIO = 1.55 / 2          # 0.775
NUDGE_UP_RATIO = 0.2 / 2           # 0.1
NAME_Y_RATIO = 1.51 / 2            # 0.755
TYPE_Y_RATIO = 1.6982 / 2          # 0.8491
NAME_FONT_PT_PER_IN = 16 / 2       # 8pt per inch of token size
TYPE_FONT_PT_PER_IN = 12 / 2       # 6pt per inch of token size

def build_sheet(db, tokens, board_width_in, board_height_in, out_path):
    ensure_dir(out_path)
    cols = max(1, int(board_width_in // TOKEN_BUFFER))
    dwg = svgwrite.Drawing(out_path, size=(f"{board_width_in}in", f"{board_height_in}in"), profile='full')
    # embed_fonts(dwg) bring back later

    placed = 0
    for i, (name, char_type, imgPath) in enumerate(tokens):
        col, row = i % cols, i // cols
        x, y = col * TOKEN_BUFFER, row * TOKEN_BUFFER
        if y + TOKEN_BUFFER > board_height_in:
            break
        add_token(dwg, x, y, name, char_type, imgPath)
        placed += 1
        db.execute("UPDATE characters SET svg_made = 1 WHERE character_name = (?)", (name,))

    rows_used = -(-placed // cols) if placed else 0
    print(f"Board completed after {placed} tokens ({cols} cols x {rows_used} rows) — {placed} placed, {len(tokens) - placed} left")
    dwg.save()
    return placed

def add_token(dwg, x, y, name, char_type, imgPath):
    token = dwg.svg(insert=(f"{x}in", f"{y}in"), size=(f"{TOKEN_SIZE}in", f"{TOKEN_SIZE}in"))
    dwg.add(token)

    with open(imgPath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    href = f"data:image/png;base64,{b64}"

    img_size = TOKEN_SIZE * IMG_SIZE_RATIO
    circle_center = TOKEN_SIZE / 2
    nudge_up = TOKEN_SIZE * NUDGE_UP_RATIO #increase this to move image higher up
    insert_x = circle_center - img_size / 2 #horizontally centering the image
    insert_y = circle_center - img_size / 2 - nudge_up #vertically centering the image and then moving it a bit up to avoid text overlap

    #TODO try to get better font
    # https://www.fontspace.com/secrilka-font-f130492
    # https://www.fontspace.com/notulen-serif-font-f76247
    # https://www.fontspace.com/panforte-serif-font-f24708
    img = dwg.image(href, insert=(f"{insert_x}in", f"{insert_y}in"), size=(f"{img_size}in", f"{img_size}in"))
    img.fit(horiz='center', vert='middle', scale='meet')
    token.add(img)

    token.add(dwg.circle(center=(f"{circle_center}in", f"{circle_center}in"), r=f"{circle_center}in", fill="none", stroke="red", stroke_width="0.001in"))
    token.add(dwg.text(name, insert=(f"{circle_center}in", f"{TOKEN_SIZE * NAME_Y_RATIO}in"), fill="black", font_size=f"{TOKEN_SIZE * NAME_FONT_PT_PER_IN}pt",
                        font_family="Franklin Gothic Book", text_anchor="middle"))
    token.add(dwg.text(char_type, insert=(f"{circle_center}in", f"{TOKEN_SIZE * TYPE_Y_RATIO}in"), fill="black", font_size=f"{TOKEN_SIZE * TYPE_FONT_PT_PER_IN}pt",
                        font_family="Franklin Gothic Demi Cond", font_weight="bold", text_anchor="middle"))
    
def greyscaleImg(db, name, imgUrl, IMAGE_DIR):
    filename = f"{normalize_name(name)}.png"
    finalpath = os.path.join(IMAGE_DIR, filename)
    ensure_dir(finalpath)
    
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


def main(custom:bool = False, **kwargs):
    script = kwargs.get("script_name")

    if not custom:
        DB_PATH = BASE_DB_PATH
        SVG_DIR = BASE_SVG_DIR
        IMAGE_DIR = BASE_IMAGE_DIR
    elif kwargs.get("script_name"):
        DB_PATH = f"{script}.db"
        SVG_DIR = f"{script}_svgs"
        IMAGE_DIR = f"{script}_images"
    else:
        DB_PATH = CUSTOM_DB_PATH
        SVG_DIR = CUSTOM_SVG_DIR
        IMAGE_DIR = CUSTOM_IMAGE_DIR

    width = kwargs.get("width", 24)
    height = kwargs.get("height", 12)

    db = sqlite3.connect(DB_PATH)

    to_greyscale = db.execute("""
                             SELECT character_name, img_url 
                             FROM characters
                             WHERE img_filepath IS NULL AND img_url IS NOT NULL
                             """)
        
    for character in to_greyscale:
        (name, url) = character
        greyscaleImg(db, name, url, IMAGE_DIR)
    db.commit()

    if not kwargs.get("new_only"): #if arg DNE, then do all. if exists and says yes new only, then won't run
        db.execute("UPDATE characters SET svg_made = 0")

    board_count = 1
    done = False
    while not done:
        if script:
            to_tokenize = db.execute("""
                                    SELECT character_name, character_type, img_filepath 
                                    FROM characters
                                    WHERE svg_made IS 0 AND img_filepath IS NOT NULL AND script is (?)
                                    """, (script,)).fetchall()
        else:
            to_tokenize = db.execute("""
                                    SELECT character_name, character_type, img_filepath 
                                    FROM characters
                                    WHERE svg_made IS 0 AND img_filepath IS NOT NULL
                                    """).fetchall()

        if not to_tokenize:
            done = True
            break
        if script:
            build_sheet(db, to_tokenize, width, height, os.path.join(SVG_DIR, f"{script}_{board_count}.svg"))
        else:
            build_sheet(db, to_tokenize, width, height, os.path.join(SVG_DIR, f"board_{board_count}.svg"))
        db.commit()
        board_count += 1
    
    
if __name__ == "__main__":
    #main()
    main(False, script_name="Trouble Brewing")
