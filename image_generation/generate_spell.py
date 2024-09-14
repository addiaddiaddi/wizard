from openai import OpenAI
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def remove_bg(img):
    r = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': img},
        data={'size': 'auto'},
        headers={'X-Api-Key': os.getenv("REMOVE_BG_API_KEY")}
        )
    if r.status_code == 200:
        return BytesIO(r.content)

def generate(element):
    gpt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). I want to create a simple 8-bit {element}-style spell sprite for a game. For example, a fireball for fire-style, or a ball of nature energy for forest-style. Plain white background. Very simple please!! One example response: \"An 8-bit style spell sprite for a wizard game. The spell should look like a small glowing orb of energy, with pixelated effects, having a bright blue core surrounded by white sparkling pixels. The spell is simple and appears to be in mid-air as if cast by a wizard, with some small particles floating around it. The overall appearance should be retro, with sharp edges and clear blocky pixels typical of 8-bit graphics.\""}
        ],
        max_tokens=300,
    )
    dalle_prompt = gpt_response.choices[0].message.content.strip()
    print(dalle_prompt)

    res = []
    for i in range(3):
        response = client.images.generate(
            model="dall-e-3",
            prompt=dalle_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        print(response.data[0].revised_prompt)

        image_url = response.data[0].url
        image_bytes = BytesIO(requests.get(image_url).content)
        image_bytes = remove_bg(image_bytes)
        res.append(image_bytes)
    return res

for i, image_bytes in enumerate(generate("water")):
    with open(f"sprite_{i}.png", "wb") as f:
        f.write(image_bytes.getbuffer())
    print(f"Image saved as sprite_{i}.png")