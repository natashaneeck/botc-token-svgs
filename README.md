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

Then run the api-calls.py file followed by the svgmaker.py file

### To do:
- finalize fonts
- add support for custom inputs, like a spreadsheet organized with name, type, and link to icon
- make some sort of better user experience like you input your board size and it does everything auto - include a question like "do you want to print all or just ones you havent before"
