import tempfile
from openai import OpenAI
import requests
from io import BytesIO
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
import random as random
from PIL import Image
import cv2
import numpy as np
import time
from backgroundremover.bg import remove

clients = [OpenAI(api_key=os.getenv("OPENAI_API_KEY_1")), OpenAI(api_key=os.getenv("OPENAI_API_KEY_2")), OpenAI(api_key=os.getenv("OPENAI_API_KEY_3")), OpenAI(api_key=os.getenv("OPENAI_API_KEY_4"))]
client_counter = 0

def remove_bg_api(img):
    r = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': img},
        data={'size': 'auto'},
        headers={'X-Api-Key': os.getenv("REMOVE_BG_API_KEY")}
        )
    if r.status_code == 200:
        return BytesIO(r.content)
    else:
        raise Exception(f"Error from remove.bg API: {r.status_code}, {r.text}")

def remove_bg(image_bytes):
    image_array = np.frombuffer(image_bytes.getvalue(), np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    hh, ww = img.shape[:2]
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])
    thresh = cv2.inRange(img, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    mask = 255 - morph
    result = cv2.bitwise_and(img, img, mask=mask)
    _, buffer = cv2.imencode('.png', result)
    result_bytes = BytesIO(buffer.tobytes())
    return result_bytes

"""
def remove_bg(image_bytes):
    with tempfile.NamedTemporaryFile(suffix='.png') as src_img, tempfile.NamedTemporaryFile(suffix='.png') as out_img:
        src_img.write(image_bytes.getvalue())
        img = remove(src_img.name, model_name="u2net", alpha_matting=True, 
                     alpha_matting_foreground_threshold=240, 
                     alpha_matting_background_threshold=10, 
                     alpha_matting_erode_structure_size=10, 
                     alpha_matting_base_size=1000)
        with open(out_img.name, "wb") as f:
            f.write(img)
        return BytesIO(open(out_img.name, 'rb').read())
"""
        
async def generate_dalle_prompt(prompt):
    global client_counter
    client_counter = (client_counter + 1) % len(clients)
    temp = client_counter
    try:
        print("="*30)
        gpt_response = await asyncio.to_thread(clients[client_counter].chat.completions.create,
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). {prompt}"}
            ],
            max_tokens=300,
            )
    except Exception as e:
        print(e)
        print(temp)
    dalle_prompt = gpt_response.choices[0].message.content.strip()
    print(dalle_prompt)
    return dalle_prompt

async def generate_image(prompt):
    global client_counter
    client_counter = (client_counter + 1) % len(clients)
    temp = client_counter
    try:
        print("="*30)
        response = await asyncio.to_thread(clients[client_counter].images.generate,
            model="dall-e-3",
            prompt=f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {prompt}",
            size="1024x1024",
            quality="standard",
            n=1,
            )
    except Exception as e:
        print(e)
        print(temp)
    print("generated image with revised prompt:")
    print(response.data[0].revised_prompt)

    image_url = response.data[0].url
    image_bytes = BytesIO(requests.get(image_url).content)

    image_bytes = remove_bg(image_bytes)
    
    return image_bytes

async def generate_spell_frames(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style spell sprite for a game. Be creative; for example, maybe a ball of cool lights for city-style, or a ball of nature energy for forest-style. Plain white background. SUPER SIMPLE  PLEASE!! One example response: \"An 8-bit style spell sprite for a wizard game. The spell should look like a small glowing orb of energy, with pixelated effects, having a bright blue core surrounded by white sparkling pixels. The spell is simple and appears to be in mid-air as if cast by a wizard, with some small particles floating around it. The overall appearance should be retro, with sharp edges and clear blocky pixels typical of 8-bit graphics.\"")
    tasks = [generate_image(dalle_prompt) for _ in range(3)]
    res = await asyncio.gather(*tasks)
    return res

async def generate_spell_explosion(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style explosion sprite for a game. Be creative; for example, a cool explosion of vapor for sky-style, or a nature energy explosion for forest-style. Plain white background. Make sure it's roughly circular shaped. {element}-style. One example response: \"An 8-bit style explosion sprite for a wizard game, appearing after a spell hits something. The explosion should be small but dynamic, with pixelated effects. It features a bright yellow and orange core, with pixelated red and white fragments flying outward in a circular pattern. The design should be simple, retro, and in line with 8-bit pixel graphics, with sharp blocky pixels and a classic video game look.\"")
    res = await generate_image(dalle_prompt)
    return res

async def generate_monster_frames(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style monster sprite for a game. Be creative; for example, a cute cloud slime for sky-style, or a forest golem on it for forest-style. Plain white background. {element}-style. One example response: \"An 8-bit style forest golem monster sprite for a game. The golem has a simple blocky body, is made of moss-covered rocks, and has glowing green eyes. The background is white, and the overall aesthetic is minimalist, using pixel art.\"")
    res = [await generate_image(dalle_prompt) for _ in range(2)]
    return res

async def generate_planet(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to create a 8-bit {element}-style planet sprite for a space game. Plain white background. {element}-style. Keep it simple! One example response: \"An 8-bit pixel art fantasy planet sprite for a game, featuring a mix of green landmasses and deep blue oceans, with floating islands and magical elements like glowing crystals and ancient ruins. The planet has a circular shape with a whimsical and vibrant style, reminiscent of classic retro games. There are clouds hovering around, and tiny details like forests and mountains are visible on the landmasses.\"")
    res = await generate_image(dalle_prompt)
    return res

async def generate_shard(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style shard sprite for a game. Be creative; for example, a blue gem with cool designs on it for water-style, or a green gem nested in branches for forest-style. Plain white background. {element}-style. One example response: \"A small, 8-bit shard sprite themed around a forest for a video game. The shard should be shaped like a broken piece of crystal with jagged edges, colored in earthy green and brown tones, with hints of moss and vines growing on it. The pixel art should evoke a natural, mystical feel, as if it was a part of an enchanted forest, with bright highlights to give it a gemstone-like appearance.\"")
    res = await generate_image(dalle_prompt)
    return res

async def generate_assets(element):
    tasks = [generate_spell_frames(element), generate_spell_explosion(element), generate_shard(element)]
    for i in range(5):
        tasks.append(generate_monster_frames(element))
    for i in range(5):
        tasks.append(generate_planet(element))
    res = await asyncio.gather(*tasks)
    image_files = [
        (f"assets/spells/{element}_0.png", res[0][0]),
        (f"assets/spells/{element}_1.png", res[0][1]),
        (f"assets/spells/{element}_2.png", res[0][2]),
        (f"assets/spells/{element}_explosion.png", res[1]),
        (f"assets/shards/{element}.png", res[2]),
        ]
    for i in range(5):
        image_files.append((f"assets/monsters/{element}_{i}_0.png", res[i+3][0]))
        image_files.append((f"assets/monsters/{element}_{i}_1.png", res[i+3][1]))
    for i in range(5):
        image_files.append((f"assets/planets/{element}_{i}.png", res[i+8]))

    for file_path, image in image_files:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "wb") as f:
            print(image)
            f.write(image.getbuffer())

# generates planets/{id}.png, spells/{id}_0.png, spells/{id}_1.png, spells/{id}_2.png, spells/{id}_explosion.png, monsters/{id}_0.png, monsters/{id}_1.png, shards/{id}.png
if __name__ == "__main__":
    """
    image_path = "assets/spells/spell_1.png"
    with open(image_path, "rb") as img_file:
        image_bytes = BytesIO(img_file.read())
    image_bytes = remove_bg(image_bytes)
    image_result = Image.open(image_bytes)
    image_result.show() 
    """

    for element in ["ice", "desert", "fairy", "moutain", "mushroom", "gemstones", "flowerland"]:
        print(element)
        asyncio.run(generate_assets(element))
        time.sleep(60)