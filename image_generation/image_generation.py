from openai import OpenAI
import requests
from io import BytesIO
import os
import asyncio
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
    return BytesIO(r.content)

async def generate_dalle_prompt(prompt):
    gpt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"I want to generate a dalle-3 image. Please write a dalle-3 prompt (and only the prompt! DO NOT return anything else). {prompt}"}
        ],
        max_tokens=300,
    )
    dalle_prompt = gpt_response.choices[0].message.content.strip()
    print(dalle_prompt)
    return dalle_prompt

async def generate_image(prompt):
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

def generate_spell(element):
    async def generate_spell_async(element):
        tasks = [generate_spell_frames(element), generate_spell_explosion(element)]
        res = await asyncio.gather(*tasks)
        return res
    res = asyncio.run(generate_spell_async(element))
    return res

def generate_monster(element):
    async def generate_monster_async(element):
        dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style monster sprite for a game. Be creative; for example, a cute cloud slime for sky-style, or a forest golem on it for forest-style. Plain white background. {element}-style. One example response: \"An 8-bit style forest golem monster sprite for a game. The golem has a simple blocky body, is made of moss-covered rocks, and has glowing green eyes. The background is white, and the overall aesthetic is minimalist, using pixel art.\"")
        res = [await generate_image(dalle_prompt) for _ in range(2)]
        return res
    res = asyncio.run(generate_monster_async(element))
    return res

def generate_planet(element):
    async def generate_planet_async(element):
        dalle_prompt = await generate_dalle_prompt(f"I want to create a 8-bit {element}-style planet sprite for a space game. Plain white background. {element}-style. Keep it simple! One example response: \"An 8-bit pixel art fantasy planet sprite for a game, featuring a mix of green landmasses and deep blue oceans, with floating islands and magical elements like glowing crystals and ancient ruins. The planet has a circular shape with a whimsical and vibrant style, reminiscent of classic retro games. There are clouds hovering around, and tiny details like forests and mountains are visible on the landmasses.\"")
        res = await generate_image(dalle_prompt)
        return res
    res = asyncio.run(generate_planet_async(element))
    return res

def generate_shard(element):
    async def generate_shard_async(element):
        dalle_prompt = await generate_dalle_prompt(f"I want to create a simple 8-bit {element}-style shard sprite for a game. Be creative; for example, a blue gem with cool designs on it for water-style, or a green gem nested in branches for forest-style. Plain white background. {element}-style. One example response: \"A small, 8-bit shard sprite themed around a forest for a video game. The shard should be shaped like a broken piece of crystal with jagged edges, colored in earthy green and brown tones, with hints of moss and vines growing on it. The pixel art should evoke a natural, mystical feel, as if it was a part of an enchanted forest, with bright highlights to give it a gemstone-like appearance.\"")
        res = await generate_image(dalle_prompt)
        return res
    res = asyncio.run(generate_shard_async(element))
    return res

# entry point
def generate_shard_spell(element):
    frames, explosion = generate_spell(element)
    
    for i, image_bytes in enumerate(frames):
        with open(f"assets/spells/spell_{i}_{element}.png", "wb") as f:
            f.write(image_bytes.getbuffer())
            
    with open(f"assets/spells/spell_explosion_{element}.png", "wb") as f:
        f.write(explosion.getbuffer())
        
    with open(f"assets/shards/shard_{element}.png", "wb") as f:
        f.write(generate_shard(element).getbuffer())
    
    return

def generate_planet_monster(id, element):
    with open(f"assets/planets/planet_{element}_{id}.png", "wb") as f:
        f.write(generate_planet(element).getbuffer())
        
    monster_frames = generate_monster(element)
    for i, image_bytes in enumerate(monster_frames):
        with open(f"assets/monsters/monster_{i}_{element}_{id}.png", "wb") as f:
            f.write(image_bytes.getbuffer())
            
    return 


if __name__ == "__main__":
    element = "water"
    """ 
    with open(f"assets/planets/planet_{element}.png", "wb") as f:
        f.write(generate_planet(element).getbuffer())
        
    with open(f"assets/shards/shard_{element}.png", "wb") as f:
        f.write(generate_shard(element).getbuffer())
    """

    # monster_frames = generate_monster(element)
    # for i, image_bytes in enumerate(monster_frames):
    #     with open(f"monster_{i}.png", "wb") as f:
    #         f.write(image_bytes.getbuffer())
    
    generate_shard_spell("forest")
    generate_planet_monster("testing123", "forest")