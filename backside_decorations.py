import base64
import os

import svgwrite

from shared import TOKEN_BUFFER, TOKEN_SIZE, ensure_dir

CUSTOM_SVG_DIR = "custom_svgs"

def build_sheet(imgPath, board_width_in, board_height_in, out_path):
    ensure_dir(out_path)
    cols = max(1, int(board_width_in // TOKEN_BUFFER))
    dwg = svgwrite.Drawing(out_path, size=(f"{board_width_in}in", f"{board_height_in}in"), profile='full')

    placed = 0
    for i in range(max(100, board_height_in / TOKEN_BUFFER * board_width_in / TOKEN_BUFFER)):
        col, row = i % cols, i // cols
        x = board_width_in - TOKEN_SIZE - (col * TOKEN_BUFFER)
        y = board_height_in - TOKEN_SIZE - (row * TOKEN_BUFFER)
        if y < 0:
            break
        add_token(dwg, x, y, imgPath)
        placed += 1

    rows_used = -(-placed // cols) if placed else 0
    print(f"Board completed after {placed} decorations ({cols} cols x {rows_used} rows)")
    dwg.save()
    return placed

def add_token(dwg, x, y, imgPath):
    token = dwg.svg(insert=(f"{x}in", f"{y}in"), size=(f"{TOKEN_SIZE}in", f"{TOKEN_SIZE}in"))
    dwg.add(token)

    with open(imgPath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    href = f"data:image/png;base64,{b64}"

    #as long as these values stay the same as in svgmaker.py
    img_size = 1.65
    circle_center = 1.0
    insert = circle_center - img_size / 2 

    img = dwg.image(href, insert=(f"{insert}in", f"{insert}in"), size=(f"{img_size}in", f"{img_size}in"))
    img.fit(horiz='center', vert='middle', scale='meet')
    token.add(img)

    

def main(**kwargs):
    name = kwargs.get("name", "decorated_back")
    width = kwargs.get("width", 24)
    height = kwargs.get("height", 12)
    decoration = kwargs.get("path", "basic_backside")

    build_sheet(decoration, width, height, f"{name}.svg")
    
    
if __name__ == "__main__":
    main()
