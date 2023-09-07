from stackapi import StackAPI
from time import time, sleep
from dotenv import load_dotenv
from os import getenv
from tqdm import trange
from typing import List
from chatexchange import Client, rooms

# load the .env file
load_dotenv()

# the time between scan rotations
# one scan rotation is the time it takes to scan all sites in SITES
# an API call will be made every SCAN_DELAY/len(SITES) seconds
#
# SCAN_DELAY must be divisible by len(SITES)
# SCAN_DELAY/len(SITES) must be greater than or equal to 60 seconds
SCAN_DELAY: int = 180

# the list of sites to be monitored
SITES: list = ["stackoverflow"]

# bypass the filters, post all comments to chat
# this is useful for testing
BYPASS_FILTERS: bool = True

# ensure SCAN_DELAY is valid
if not(SCAN_DELAY % len(SITES) == 0):
    raise ValueError("SCAN_DELAY must be divisible by len(SITES).")

if not(SCAN_DELAY / len(SITES) >= 60):
    raise ValueError("SCAN_DELAY/len(SITES) must be greater than or equal to 60 seconds.")

# create the API objects
APIs: List[StackAPI] = [StackAPI(site, key=getenv("API_KEY")) for site in SITES]

# set up chat
chat_client: Client = Client("stackexchange.com")

chat_room: rooms.Room = chat_client.get_room(getenv("CHAT_ROOM_ID"))

chat_room.send_message("[Same Problem Bot] Bot started.")
chat_client.login(getenv("CHAT_EMAIL"), getenv("CHAT_PASSWORD"))

def truncate_string(text: str, length: int) -> str:
    """
    Truncates a string to a given length.
    """
    if len(text) <= length:
        return text
    else:
        return text[:(length - 3)] + "..."


def seconds_since_epoch() -> int:
    """
    Returns the number of seconds since the unix epoch.
    """
    return int(time())


def sleep_progress(seconds: int) -> None:
    """
    Sleeps for a given number of seconds, and displays a progress bar indicating time elapsed.
    """
    for i in trange(seconds, desc="Sleeping"):
        sleep(1)


def check_comment(comment: str) -> bool:
    """
    Checks if a comment is a "same problem" comment.
    """
    if BYPASS_FILTERS:
        return True
    
    if ("same problem" in comment.lower()) and (len(comment) < 45):
        return True
    return False


def scan_site(site: StackAPI) -> None:
    """
    Scans a site for "same problem" comments.
    """
    sleep_progress(SCAN_DELAY / len(SITES))
    
    current_time = seconds_since_epoch()
    comments = site.fetch(
        "comments",
        filter=getenv("API_FILTER"),
        todate=current_time,
        fromdate=last_query,
    )
    
    for comment in comments["items"]:
        if comment["owner"]["reputation"] < 50:
            continue
        if check_comment(comment["body"]):
            chat_room.send_message(f"[Same Problem Bot] Potentially bad comment detected '{truncate_string(comment['body'], 100)}'")
    
    last_query = current_time
    


last_query: int = seconds_since_epoch()

while True:
    for site in APIs:
        scan_site(site)
