import os
import config
import sys
from functions.declarations import available_functions
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function

def main():
    load_dotenv()

    if len(sys.argv)<2:
        print("No prompt given")
        exit(1)
    
    
    verbose = "--verbose" in sys.argv
    
    
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
        
    user_prompt = " ".join(args)        #this basicaly covers if a user types without "" around his prompt, it will make it into a string.
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
    


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=config.model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=config.system_prompt, 
            )
        
    )
    
    if verbose == True: 
        print(f"User prompt:", {user_prompt} )
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    if response.function_calls:
        for function_call_part in response.function_calls:
            try:
                function_call_result = call_function(function_call_part, verbose)
                print(f"-> {function_call_result.parts[0].function_response.response}")
            except KeyError as e:
                raise Exception(f'.parts[0].function_response.response does not exist, {e}')
            except Exception as e:
                raise Exception( f"Error calling function: {e}")
                
    if not response.function_calls:
        print(response.text)


if __name__ == "__main__":
    main()
