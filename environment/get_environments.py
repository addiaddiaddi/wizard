import environment.dalle
from openai import OpenAI
from PIL import Image, ImageEnhance

# Load the image
def darken_image(image_path):
    # image_path = 'your_image_path.png'  # Replace with your image file path
    image = Image.open(image_path)

    # Darken the image by reducing brightness (0.0 will be completely black, 1.0 is original)
    enhancer = ImageEnhance.Brightness(image)
    darkened_image = enhancer.enhance(0.5)  # Adjust this value to control the level of darkening

    # Save or display the darkened image
    # darkened_image.show()  # To display the image
    # darkened_image.save('darkened_image.png')  # To save the image

    darkened_image.save(image_path)



    # biome_type = 'swamp' 


def get_background(idx):
    prompt = "Generate a pixel art image of a colorful galaxy in deep space. The image should feature glowing stars, some with bright flares, scattered across the dark night sky. Include hues of blue, purple, red, and pink for stars and cosmic clouds, with a focus on a central bright star radiating light. The stars and nebulae should be depicted using small square pixels to mimic the classic pixel art style, creating a vibrant, otherworldly, retro visual."
    images = environment.dalle.query_dalle(prompt, image_size="1024x1024", n=1) 
    print(images)

    environment.dalle.download_image(images[0], f"background_{0}.png")
    environment.dalle.download_image(images[0], f"background_{idx+1}.png")

    darken_image(f"background_0.png")
    return 'background_0.png' 








if __name__ == '__main__': 
    # print("FOO")


    # response = client.chat.completions.create(model="gpt-4",
    # messages=[
    #     {"role": "user", "content": "Tell me items in swamp. Limit your response to a list of 3 words. For instance for a forest, the three words could be trees, shrubs, grass"},
    #     # {"role": "user", "content": "What can you do?"}
    # ])
    # print(response)

    # The environment should reflect {biome_type} characteristics such as {response.choices[0].message}
  #  prompt = f"Generate a {biome_type} landscape tile for a 2D top-down game map. The tile should be axis-aligned with a simple top-down appearance, ensuring it seamlessly loops with other tiles. The environment should reflect {biome_type} characteristics such as {response.choices[0].message}.The aesthetic and detail level of a game like stardew valley. Use a hand-drawn pixel art style that fits with vibrant and colorful 16-bit visuals, focusing on a clear top-down perspective and minimal shading"

    prompt = "Generate a pixel art image of a colorful galaxy in deep space. The image should feature glowing stars, some with bright flares, scattered across the dark night sky. Include hues of blue, purple, red, and pink for stars and cosmic clouds, with a focus on a central bright star radiating light. The stars and nebulae should be depicted using small square pixels to mimic the classic pixel art style, creating a vibrant, otherworldly, retro visual."
    # prompt = "Generate a swamp landscape tile for a top-down game map. The tile should include murky water, patches of grass, small islands, and vines. Use dark greens and browns for the color palette. Ensure the tile loops seamlessly for a pixel or 3D game."
# 
    # revised_prompt = "Create a 256x256 pixel sprite sheet with a depth of 16-bit color and a black background. The sheet should have 8 frames, each of 32x32 size with a top-down view. These frames should contain different depictions of a lava biome, detailed with molten rocks and waves of lava. The designs should be clear and distinctive from each other, creating a diverse and interesting collection of sprite imagery. Sky should not be included in any of the frames"
# Create a 256x256 pixel sprite sheet featuring a top-down view of a lava biome in 16-bit color depth against a black background. The sprite sheet should comprise eight unique 32x32 pixel frames, each depicting a different segment of the lava biome. Exclude any representations of the sky in all frames




    for i in range(1): 
        images = environment.dalle.query_dalle(prompt, image_size="1024x1024", n=1) 
        environment.dalle.download_image(images[0], f"background_{i}.png")
        darken_image(f"background_{i}.png")



