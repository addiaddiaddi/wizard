from openai import OpenAI
import requests
from io import BytesIO
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key="")

def remove_bg(img):
    r = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': img},
        data={'size': 'auto'},
        headers={'X-Api-Key': ''}
        )
    return BytesIO(r.content)

async def generate_dalle_prompt(prompt):
    gpt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
    )
    dalle_prompt = gpt_response.choices[0].message.content.strip()
    print(dalle_prompt)
    return dalle_prompt

async def generate_image(prompt):
    print("generating image with prompt")
    response = await asyncio.to_thread(client.images.generate,
        model="dall-e-3",
        prompt=f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {prompt}",
        size="1024x1024",
        quality="standard",
        n=1,
        )
    print("generated image with revised prompt:")
    print(response.data[0].revised_prompt)

    image_url = response.data[0].url
    image_bytes = BytesIO(requests.get(image_url).content)
    # image_bytes = remove_bg(image_bytes)
    return image_bytes

async def generate_spell_frames(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). I want to create a simple 8-bit {element}-style spell sprite for a game. Be creative; for example, maybe a ball of cool lights for city-style, or a ball of nature energy for forest-style. Plain white background. SUPER SIMPLE  PLEASE!! One example response: \"An 8-bit style spell sprite for a wizard game. The spell should look like a small glowing orb of energy, with pixelated effects, having a bright blue core surrounded by white sparkling pixels. The spell is simple and appears to be in mid-air as if cast by a wizard, with some small particles floating around it. The overall appearance should be retro, with sharp edges and clear blocky pixels typical of 8-bit graphics.\"")
    tasks = [generate_image(dalle_prompt) for _ in range(3)]
    res = await asyncio.gather(*tasks)
    return res

async def generate_spell_explosion(element):
    dalle_prompt = await generate_dalle_prompt(f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). I want to create a simple 8-bit {element}-style explosion sprite for a game. Be creative; for example, a cool explosion of vapor for sky-style, or a nature energy explosion for forest-style. Plain white background. {element}-style. One example response: \"An 8-bit style explosion sprite for a wizard game, appearing after a spell hits something. The explosion should be small but dynamic, with pixelated effects. It features a bright yellow and orange core, with pixelated red and white fragments flying outward in a circular pattern. The design should be simple, retro, and in line with 8-bit pixel graphics, with sharp blocky pixels and a classic video game look.\"")
    res = await generate_image(dalle_prompt)
    return res

def generate_spell(element):
    async def generate_spell_async(element):
        tasks = [generate_spell_frames(element), generate_spell_explosion(element)]
        res = await asyncio.gather(*tasks)
        return res
    
    res = asyncio.run(generate_spell_async(element))
    return res

def generate_monster(element):
    async def generate_monster_async(element):
        dalle_prompt = await generate_dalle_prompt(f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). I want to create a simple 8-bit {element}-style monster sprite for a game. Be creative; for example, a cute cloud slime for sky-style, or a forest golem on it for forest-style. Plain white background. {element}-style. One example response: \"An 8-bit style forest golem monster sprite for a game. The golem has a simple blocky body, is made of moss-covered rocks, and has glowing green eyes. The background is white, and the overall aesthetic is minimalist, using pixel art.\"")
        res = [await generate_image(dalle_prompt) for _ in range(2)]
        return res
    
    res = asyncio.run(generate_monster_async(element))
    return res

if __name__ == "__main__":
    element = "forest"
    frames, explosion = generate_spell(element)
    
    for i, image_bytes in enumerate(frames):
        with open(f"assets/spells/spell_{i}.png", "wb") as f:
            f.write(image_bytes.getbuffer())
            
    with open(f"assets/spells/spell_explosion.png", "wb") as f:
        f.write(explosion.getbuffer())
        
    monster_frames = generate_monster(element)
    for i, image_bytes in enumerate(monster_frames):
        with open(f"assets/monsters/monster_{i}.png", "wb") as f:
            f.write(image_bytes.getbuffer())