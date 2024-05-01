import asyncio

async def input_prompt(prompt):
    print(prompt, end='', flush=True)
    return await asyncio.to_thread(input)

asyncio.run(input_prompt("Prompt: "))