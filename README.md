# Same Problem Bot

This is a bot that aims to detect comments along the lines of "I'm having the same problem" on SE questions. It currently scans the following sites:
* Stack Overflow

## Running the bot

I wrote this in Python and typically support only the most recent stable release of Python. I assume you have the following:
* The most recent stable release of Python 3.X
* Pip
* A Stack Exchange account with chat privileges
* A Stack Exchange API key

Clone the repo and `cd` into it
```none
$ https://github.com/CoconutMacaroon/same-problem-bot && cd same-problem-bot
```
Create a `.env` file, with the following contents. Other than the `API_FILTER`, fill in the rest with your information.
```none
API_KEY=YOUR API KEY
API_FILTER="!6WPIompltRXVK"
CHAT_EMAIL=YOUR CHAT EMAIL
CHAT_PASSWORD=YOUR CHAT PASSWORD
CHAT_ROOM_ID=CHATROOM TO USE
```
Install the requirements and update them if they're already installed. On some versions of Python, you may need to install these using your system package manager instead, such as `apt` or `pacman`.
```none
$ pip install --upgrade stackapi python-dotenv tqdm chatexchange beautifulsoup4 requests websocket-client
```
Once you've done that, you should be able to run the bot now
```none
$ python same_problem_bot.py
```
