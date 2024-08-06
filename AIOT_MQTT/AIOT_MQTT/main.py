import json
import os
from openai import AsyncOpenAI
import chainlit as cl

# Constants
API_KEY = os.getenv("API_KEY")
MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
TEMPERATURE = 0.7

# Global variables
memory = [{
    "role": "system",
    "content": ""  # Initialize with an empty string for now
}]

# Initialize the OpenAI client
client = AsyncOpenAI(base_url="https://api.together.xyz/v1", api_key=API_KEY)


# Function to load and format the system prompt
def load_system_prompt():
    system_prompt = open("system_prompt.md", "r", encoding="utf-8").read()
    device = open("devices.md", "r", encoding="utf-8").read()
    formatted_system_prompt = system_prompt.format(devices=device)
    return formatted_system_prompt


# Function to handle incoming messages
@cl.on_message
async def on_message(message: cl.Message):
    global memory
    memory.append({
        "role": "user",
        "content": message.content
    })
    await process_message()


# Function to process the message and get a response from the AI model
async def process_message():
    global memory
    while True:
        response = await client.chat.completions.create(
            messages=memory,
            model=MODEL,
            temperature=TEMPERATURE
        )
        try:
            res = json.loads(response.choices[0].message.content)
            await cl.Message(content=res['message']).send()
            memory.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            if res['method'] == "devices":
                pass
            break

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            memory.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            memory.append({
                "role": "user",
                "content": f"You get warned! {e} Answer Following instructor and keep in JSON format."
            })


# Function to initialize the system prompt at the start
def initialize_system_prompt():
    global memory
    formatted_system_prompt = load_system_prompt()
    memory[0]["content"] = formatted_system_prompt




# Call the initialization function
initialize_system_prompt()

