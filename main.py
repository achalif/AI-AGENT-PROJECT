from system_prompt import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function
def main():
     from google.genai import types
     import argparse
     import os
     from dotenv import load_dotenv
     load_dotenv()
     api_key = os.environ.get("GEMINI_API_KEY")

     parser = argparse.ArgumentParser(description="Chatbot")
     parser.add_argument("user_prompt", type=str, help="User prompt")
     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
     args = parser.parse_args()
     
     messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
     if api_key is None:
            raise RuntimeError("GEMINI_API_KEY not found.")
     from google import genai
     client = genai.Client(api_key=api_key)
     
     for _ in range(20):
         response = client.models.generate_content(
	    model = "gemini-2.5-flash",
	    contents = messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0)
         )
         if response.candidates:
             for candidate in response.candidates:
                 messages.append(candidate.content)
             
         if response.usage_metadata is None:
             raise RuntimeError("Metadata is missing.")
         if args.verbose:
             print(f"User prompt: {args.user_prompt}")
             print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
             print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
     
         if response.function_calls:
             function_responses = []
             for function_call in response.function_calls:
             
                 #Call function using helper and store the result
                 function_call_results = call_function(function_call, args.verbose) 
        
                 #Ensure the parts list is not empty
                 if not function_call_results.parts:
                     raise Exception("The function can result contains no parts.")
        
                 #Store the first part of the function_response object 
                 part = function_call_results.parts[0]
         
                 #Check the first part of the function_response object
                 if part.function_response is None:
                     raise Exception("The first part of the result is not a valid FunctionResponse")
         
                 #Check the .response field of the FunctionResponse object
                 if part.function_response.response is None:
                     raise Exception("The FunctionResponse object has no response data.")  
         
                 #Add .parts[0] to a list of function results
                 function_responses.append(function_call_results.parts[0])
        
                 if args.verbose:
                     print(f"-> {function_call_results.parts[0].function_response.response}")
        
             messages.append(types.Content(role="user", parts=function_responses))
         else:
             print("Final response:")
             print(response.text)
             return
     #If the program gets here, the loop finished without returning
     print("Maximum iterations reached without a final response")
     sys.exit(1)
if __name__ == "__main__":
    main()
