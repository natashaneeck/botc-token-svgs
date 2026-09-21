# botc-token-svgs

The purpose of this is to automatically take all of the characters from the blood on the clocktower wiki and put them into a file usable for lasercutting to make my own tokens.  

Using the MediaWiki API, I store the token information in SQLite, and then use python svgwrite to make the svg files

### How to Use

Create your virtual environment:  
`python3.11 -m venv .venv`  

Install dependencies with pip or some similar package manager:
`pip install -r requirements.txt`

activate your virtual environment in Windows by:  
`.\\.venv\\Scripts\\activate`

in Linux by:  
`source .venv/bin/activate`

Then run main.py to complete the program in the terminal and follow the prompts

### To do:
code only:
- finalize fonts
- add reminder tokens as an option in the terminal runner
- figure out plans for reminder tokens - get from spreadsheet
    handle multiple tokens with the same text and character
- update token sizes
- i forgot that i can make the .db files all the same one and just have different tables within. oops. fix that probably

manual:
- figure out boxes for storage, including the grim (LASER CUT BOX SVG GENERATORS EXIST!! I JUST NEED THE DIMENSIONS AND WOOD THICKNESS) - [this one can do lids AND dividers](https://gravolab.pro/box-gen/)
- figure out other pieces needed like shrouds & info cards - shrouds can rest on top in a semicircle so they can be lasercut?
- figure out token bag
- do i have to get felt
- dont forget the stand and clips for the grim
