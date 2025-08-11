import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import config
from functions.get_files_info import schema_get_files_info



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

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
    )

    generate_content(client, messages, user_prompt, system_prompt, available_functions)


def generate_content(client, messages, user_prompt, system_prompt, available_functions):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt}")
        #In addition to printing the text response, print the number of tokens consumed by the interaction
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Check if there are function calls (note: it's a list, not None check)
    if response.function_calls:
        # Iterate through all function calls
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        return  # Don't print text response if there are function calls
    print(response.text)

if __name__ == "__main__":
    main()
