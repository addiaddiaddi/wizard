from openai import OpenAI

client = OpenAI() 

def query_gpt4(prompt):
    """
    Queries the GPT-4 model using the OpenAI API with the given prompt.

    Parameters:
    prompt (str): The input prompt for the GPT-4 model.
    api_key (str): Your OpenAI API key.

    Returns:
    str: The GPT-4 model's response to the prompt.
    """

    # Set your API key
    # openai.api_key = api_key

    try:
        # Make a request to the GPT-4 API
        response = client.chat.completions.create(
            model="gpt-4",              # Use GPT-4 chat model
            messages=[                  # Input prompt in message format
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,              # Maximum number of tokens in the response
            n=1,                         # Number of responses to generate
            stop=None,                   # Set stop sequence if required
            temperature=0.7              # Controls the creativity of the output (0.7 is a balanced setting)
        )
        # Return the text of the response
        return response.choices[0].message

    except Exception as e:
        return f"An error occurred: {e}"