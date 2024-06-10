import subprocess
from twikit import Client
from dotenv import load_dotenv
import requests
import os
import asyncio
import openCode

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

user = client.get_user_by_screen_name('ChipotleTweets')
tweets = user.get_tweets('Tweets', count=5)
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