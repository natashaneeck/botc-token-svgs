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
non urgent:
- i forgot that i can make the .db files all the same one and just have different tables within. oops. fix that probably
- add reminder tokens as an option in the terminal runner
- put things into organized folders and fix imports and filepaths so it all still works

code only:
- finalize fonts
- update token sizes to be more dynamic and work with the 1.5 diameter norm

manual:
- figure out boxes for storage, including the grim (LASER CUT BOX SVG GENERATORS EXIST!! I JUST NEED THE DIMENSIONS AND WOOD THICKNESS) - [this one can do lids AND dividers](https://gravolab.pro/box-gen/)
- finish info cards
- dont forget the stand for the grim - model off of canvas stand designs?
- backside image for tokens, with 1/2 inch felt taken into account
- fancy designs for box ideally

created:
death shrouds
half of info cards
