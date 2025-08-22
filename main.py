import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import config
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


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

    system_prompt = """You are a helpful AI coding agent. When a user asks a question, actively explore and investigate using your available tools to find the complete answer.

You can:
- List files and directories
- Read file contents  
- Execute Python files with optional arguments
- Write or overwrite files

Don't just plan what you would do - actually do it! Use your tools to explore the codebase thoroughly until you have enough information to provide a complete answer.

All paths should be relative to the working directory."""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
    )
    i=0
    while i < 20:
        
        try:
            response = generate_content(client, messages, user_prompt, system_prompt, available_functions)
            #print(f"DEBUG: response type is {type(response)}")
            #print(f"DEBUG: response value is {response}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue
        if response.text and not response.function_calls:
            print(response.text)
            break
        i+=1




def generate_content(client, messages, user_prompt, system_prompt, available_functions):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)    
            
    verbose = False
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt}")
        #In addition to printing the text response, print the number of tokens consumed by the interaction
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        verbose = True

    if response.function_calls:
        for function_call in response.function_calls:
            results = call_function(function_call, verbose)
            messages.append(results)
            if not results.parts[0].function_response.response:
                raise Exception("No valid response from function call")
            elif results.parts[0].function_response.response and verbose==True:
                print (f"-> {results.parts[0].function_response.response}")
        return response
    return response
    '''
    # Check if there are function calls (note: it's a list, not None check)
    if response.function_calls:
        # Iterate through all function calls
        for function_call_part in response.function_calls:
            results = call_function(function_call_part, verbose)
            content = types.Content(
                role = 'tool',
                parts=[types.Part.from_text(text=results.parts[0].function_response.response)]
            )
            messages.append(content)
            if not results.parts[0].function_response.response:
                raise Exception("No valid response from function call")
            elif results.parts[0].function_response.response and verbose==True:
                print (f"-> {results.parts[0].function_response.response}")
        return  results# Don't print text response if there are function calls
    '''

if __name__ == "__main__":
    main()
