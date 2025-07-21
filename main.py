import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types




def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "What is the meaning of life?"')
        sys.exit(1)
    user_prompt = " ".join(args)
    #print(f"user prompt: {user_prompt}")
    

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    #print(f"messages: {messages}")
    generate_content(client, messages, user_prompt)


def generate_content(client, messages, user_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt}")
        #In addition to printing the text response, print the number of tokens consumed by the interaction
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == "__main__":
    main()
