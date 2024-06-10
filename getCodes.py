import subprocess
from twikit import Client
from dotenv import load_dotenv
import requests
import os
import asyncio
import openCode
import time

load_dotenv()
USER = os.getenv("USER")
PASS = os.getenv("PASS")
PHONE = os.getenv("PHONE")

client = Client('en-US')
client.login(
    auth_info_1=USER,
    auth_info_2=PHONE,
    password=PASS
)

def get_tweets_with_backoff(user, max_retries=5):
    base_sleep = 1  # Base sleep time in seconds
    for i in range(max_retries):
        try:
            return user.get_tweets('Tweets', count=2)
        except Exception as e:
            print(f"Attempt {i+1}: Failed to fetch tweets, retrying in {base_sleep} seconds. Error: {e}")
            time.sleep(base_sleep)
            base_sleep *= 2  # Double the sleep time for the next retry
    raise Exception("Failed to fetch tweets after several retries")

user = client.get_user_by_screen_name('ChipotleTweets')
tweets = get_tweets_with_backoff(user)
seen = set()
try:
    with open('images/seen.txt', 'r') as file:
        seen = set(line.strip() for line in file)
except:
    print("Error opening set file")

async def textCode(tweet):
    if tweet.media and tweet.id not in seen:
        image_url = tweet.media[0]['media_url_https']
        response = requests.get(image_url)
        path = f'images/{tweet.id}.png'
        with open(path, 'wb') as handler:
            handler.write(response.content)
        code = await openCode.summarize_image(path)
        command = ["osascript", "sendMessage.applescript", "888222", code]
        subprocess.run(command, check=True)
        with open('images/seen.txt', 'a') as file:
            file.write(f"{tweet.id}\n")

async def main():
    tasks = [textCode(tweet) for tweet in tweets[:5]]
    await asyncio.gather(*tasks)
    print("Program ran")

if __name__ == "__main__":
    asyncio.run(main())