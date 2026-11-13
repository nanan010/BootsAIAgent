import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise Exception("Open router api key not found")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt,}
        ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools = available_functions
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                #print(f"Calling function: {tool_call.function.name}({function_args})")

        else:
            prompt_token = response.usage.prompt_tokens
            completion_token = response.usage.completion_tokens
            if args.verbose:
                print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token}\nResponse tokens: {completion_token}\nResponse:")
            print(f"-> {message.content}")
            break
    else:
        print("Error: Maximum iterations reached without a final response.")
        exit(1)