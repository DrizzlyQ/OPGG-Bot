# League of Legends Account Search Discord Bot

## About ##
League of Legends Discord Bot that can search a League of Legends Profile on OP.GG without API Key needed on every League of Legends Server!

## Usage ##
1. Right Click inside the folder and Press "Open Powershell Window Here"
2. Run this: ```python -m pip install -r requirements.txt```
3. After that's done, head to the folder called "secret" and place your token under 'TOKEN' field on "secret_token.py"
4. Run with ```python bot.py```


## Features ##
  - LoL champion build [Usage: /build [lane] [champion]]
      - Uses http://lol.lukegreen.xyz/ API to scrape op.gg data
      - Sends top five builds for champion in specified lane
      - Sends most popular runes, scraped using Selenium
