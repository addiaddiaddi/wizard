from openai import OpenAI

import requests
import os

# Initialize API Key

# Function to query DALL·E

print(os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_dalle(prompt, image_size="1024x1024", n=1):
    try:
        # Generate image
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=n,  # Number of images
            size=image_size  # Image size, e.g., "1024x1024")
        )

        print(response)
        # Extract the image URL(s)
        image_urls = [img.url for img in response.data]
        return image_urls
    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to download the image(s)
def download_image(url, file_name="generated_image.png"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Image successfully downloaded: {file_name}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Example usage
if __name__ == "__main__":
    # Step 1: Query DALL·E
    prompt_text = "A futuristic city skyline at sunset with flying cars and neon lights."
    image_urls = query_dalle(prompt_text, image_size="1024x1024", n=1)

    # Step 2: Download the images
    for idx, url in enumerate(image_urls):
        file_name = f"generated_image_{idx}.png"
        download_image(url, file_name)
