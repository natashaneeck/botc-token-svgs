import base64
import os
import sqlite3

import pandas as pd
import svgwrite

from shared import ensure_dir

TOKEN_SIZE = 0.75
TOKEN_BUFFER = TOKEN_SIZE + 0.1

REMINDER_DIR = "reminder_tokens"

def build_sheet(db, tokens, board_width_in, board_height_in, out_path):
    ensure_dir(out_path)
    cols = max(1, int(board_width_in // TOKEN_BUFFER))
    dwg = svgwrite.Drawing(out_path, size=(f"{board_width_in}in", f"{board_height_in}in"), profile='full')
    # embed_fonts(dwg) bring back later

    placed = 0
    for i, (token_id, token_text, imgPath) in enumerate(tokens):
        # get character imgPath
        # iterate over columns
        col, row = i % cols, i // cols
        x, y = col * TOKEN_BUFFER, row * TOKEN_BUFFER
        if y + TOKEN_BUFFER > board_height_in:
            break
        add_token(dwg, x, y, token_text, imgPath)
        placed += 1
        db.execute("UPDATE reminder_tokens SET svg_made = 1 WHERE id = ?", (token_id,))

    rows_used = -(-placed // cols) if placed else 0
    print(f"Board completed after {placed} tokens ({cols} cols x {rows_used} rows) — {placed} placed, {len(tokens) - placed} left")
    dwg.save()
    return placed

def add_token(dwg, x, y, token_text, imgPath):
    token = dwg.svg(insert=(f"{x}in", f"{y}in"), size=(f"{TOKEN_SIZE}in", f"{TOKEN_SIZE}in"))
    dwg.add(token)

    with open(imgPath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    href = f"data:image/png;base64,{b64}"

    img_size = 0.25
    center = TOKEN_SIZE / 2
    nudge_up = 0.05 #increase this to move image higher up
    insert_x = center - img_size / 2 #horizontally centering the image
    insert_y = center - img_size / 2 - nudge_up #vertically centering the image and then moving it a bit up to avoid text overlap

    img = dwg.image(href, insert=(f"{insert_x}in", f"{insert_y}in"), size=(f"{img_size}in", f"{img_size}in"))
    img.fit(horiz='center', vert='middle', scale='meet')
    token.add(img)

    token.add(dwg.circle(center=(f"{center}in", f"{center}in"), r=f"{center}in", fill="none", stroke="red", stroke_width="0.001in"))
    token.add(dwg.text(token_text, insert=(f"{center}in", f"{TOKEN_SIZE - 0.05}in"), fill="black", font_size="6pt",
                        font_family="Franklin Gothic Book", text_anchor="middle"))


def main(img_db, spreadsheet = "base_and_carousel.xlsx", **kwargs):
    script = kwargs.get("script_name", "board")
    width = kwargs.get("width", 24)
    height = kwargs.get("height", 12)

    db = sqlite3.connect("reminders.db")
    db.execute("""CREATE TABLE IF NOT EXISTS reminder_tokens (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_name  TEXT,
                    token_text      TEXT,
                    svg_made        INTEGER DEFAULT 0,
                    img_filepath    TEXT DEFAULT NULL
                    )
                """)
    db.commit()
    df = pd.read_excel(spreadsheet)
    token_cols = [c for c in df.columns if c == "Token" or c.startswith("Token.")]

    img_db = sqlite3.connect(img_db)

    for row in range(df.shape[0]):
        name = df.at[row, "Name"]
        result = img_db.execute("""
                        SELECT img_filepath 
                        FROM characters
                        WHERE character_name IS ?
                        """, (name,)).fetchone()
        if result is None:
            print(f"No image found for {name}, skipping")
            continue

        img = result[0]

        token_cols = [c for c in df.columns if c == "Token" or c.startswith("Token.")]
        for col in token_cols:
            token_text = df.at[row, col]
            if pd.isna(token_text):
                continue   # character just has fewer than the max number of tokens
            db.execute("INSERT INTO reminder_tokens (character_name, token_text, img_filepath) VALUES (?, ?, ?)",
                    (name, token_text, img))
    db.commit()


    board_count = 1
    done = False
    while not done:
        to_tokenize = db.execute("""
                                SELECT id, token_text, img_filepath
                                FROM reminder_tokens
                                WHERE svg_made IS 0 AND img_filepath IS NOT NULL
                                """).fetchall()
        if not to_tokenize:
            done = True
            break
        build_sheet(db, to_tokenize, width, height, os.path.join(REMINDER_DIR, f"{script}_{board_count}.svg"))
        db.commit()
        board_count += 1
    
    
if __name__ == "__main__":
    main("botc.db")

