
from openai import OpenAI
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=api_key)


ops = {
    "CLOSE": " I sent an image to you because I was close to something, start this conversation out with 'Watch out!'",
    "PERSON": "I send an image to you because I'm talking to someone, and I want you to describe what they are wearing",
    "TEXT": "DESCRIBE"
}


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def assist(image_path, code):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": f"you are a visual aid assistant for a blind person, when I send a photo, do your best to describe it in the most concise put detailed version possible as if you are a voice assistant, and depending on the prefix, some of which can be seen in this object below, so if the prompt starts with the object key, the value is the context \n{json.dumps(ops)}:  \nOthers you can infer, based on the prefix, change your description to best fit the context"
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{code}"},
                {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
            ]
        }
    ],
    max_tokens=100)

    caption = response.choices[0].message.content
    return caption.strip()

if __name__ == "__main__":
    image_path = "close.png"
    op = "CLOSE"
    caption = assist(image_path, op)
    print("Description:", caption)
