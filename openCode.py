import base64
from dotenv import load_dotenv
import requests
import os
import asyncio



SYS_PROMPT="""
You are an agent who's job is to extract text from images.
All output should be in the form of a single string (ex. "FREE4FREEA7Y25W)
"""

IMAGE_PROMPT="""
Extract the code from the image.
The code will be in format FREE_FREE______ (ex. "FREE4FREEA7Y25W)
Return only the code
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

async def summarize_image(path):
    load_dotenv()
    api_key = os.getenv("OPENAI")
    base64_image = encode_image(path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": f"{SYS_PROMPT}"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": IMAGE_PROMPT,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            },
        ],
        "max_tokens": 2000,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return ""

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(summarize_image("downloaded_image.png"))
    print(result)
