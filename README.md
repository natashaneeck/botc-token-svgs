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

code and some manual:
- figure out plans for reminder tokens - another spreadsheet, or get from json?

manual:
- figure out boxes for storage, including the grim
- figure out other pieces needed like shrouds & info cards - shrouds can rest on top in a semicircle so they can be lasercut?
- figure out token bag
