import os
import svgwrite
import base64

CUSTOM_SVG_DIR = "custom_svgs"
BASE_SVG_DIR = "base_svgs"
TOKEN_SIZE = 2.0  # inches -- matches the circle's diameter
TOKEN_BUFFER = TOKEN_SIZE + .1

def ensure_dir(filepath):
    d = os.path.dirname(filepath)
    if d:
        os.makedirs(d, exist_ok=True)

def build_sheet(tokens, imgPath, board_width_in, board_height_in, out_path):
    ensure_dir(out_path)
    cols = max(1, int(board_width_in // TOKEN_BUFFER))
    dwg = svgwrite.Drawing(out_path, size=(f"{board_width_in}in", f"{board_height_in}in"), profile='full')

    placed = 0
    for i in range(tokens):
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

    

def main():
    base = False

    if base:
        SVG_DIR = BASE_SVG_DIR
    else:
        SVG_DIR = CUSTOM_SVG_DIR

    build_sheet(55, os.path.join("base_images", "amnesiac.png"), 24, 12, os.path.join(SVG_DIR, "decorated_back.svg"))
    
    
if __name__ == "__main__":
    main()


#Note: decoration file size should probably be a square 