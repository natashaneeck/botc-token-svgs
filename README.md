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

code and some manual:
- figure out plans for reminder tokens - another spreadsheet, or get from json?
    get from spreadsheet, and tokenize (skip inbetween db). use this for base3: https://www.scribd.com/document/929649954/BotC-Box-Contents and this for carousel: https://bloodontheclocktower.com/collections/carousel-reminder-tokens?page=7 
    handle multiple tokens with the same text and character

manual:
- figure out boxes for storage, including the grim (LASER CUT BOX SVG GENERATORS EXIST!! I JUST NEED THE DIMENSIONS AND WOOD THICKNESS) - storage boxes may require some tinkering
- figure out other pieces needed like shrouds & info cards - shrouds can rest on top in a semicircle so they can be lasercut?
- figure out token bag
- do i have to get felt