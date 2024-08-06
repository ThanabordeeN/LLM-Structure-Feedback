import json
import serial
import os
from openai import AsyncOpenAI
import chainlit as cl

system_prompt = open("system_prompt.md", "r", encoding="utf-8").read()
device = open("devices.md", "r", encoding="utf-8").read()
# Parse the device data as JSON
formatted_system_prompt = system_prompt.format(devices=device)
memory = [{
    "role": "system",
    "content": formatted_system_prompt}]

client = AsyncOpenAI(base_url="https://api.together.xyz/v1", api_key=os.getenv("API_KEY"))

settings = {
    "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "temperature": 0.7,
}

def connect_serial():


@cl.on_message
async def on_message(message: cl.Message):
    global memory
    memory.append({
        "role": "user",
        "content": message.content
    })
    while True:
        response = await client.chat.completions.create(
            messages=memory,
            **settings
        )
        try:
            res = json.loads(response.choices[0].message.content)
            await cl.Message(content=res['message']).send()
            memory.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            break

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            memory.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            memory.append({
                "role": "user",
                "content": "You get warned! {e} Answer Following instructor and keep in JSON format.".format(e=e)
            })

