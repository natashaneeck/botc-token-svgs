# botc-token-svgs

The purpose of this is to automatically take all of the characters from the blood on the clocktower wiki and put them into a file usable for lasercutting to make my own tokens.  

Using the MediaWiki API, I store the token information in SQLite, and then use python svgwrite to make the svg files

### How to Use

Install dependencies with pip or some similar package manager:
- requests
- sqlite3
- numpy
- svgwrite
- PIL (pillow)
- openpyxl

Then run the api-calls.py file followed by the svgmaker.py file

### To do:
code only:
- finalize fonts
- make some sort of better user experience like you input your board size and it does everything auto - include a question like "do you want to print all or just ones you havent before"?
- make requirements manager

code and some manual:
- figure out plans for reminder tokens - another spreadsheet, or get from json?

manual:
- figure out boxes for storage, including the grim
- figure out other pieces needed like shrouds & info cards - shrouds can rest on top in a semicircle so they can be lasercut?
- figure out token bag
