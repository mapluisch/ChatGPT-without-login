import asyncio
from gpt import GPT

async def run_session():
    session = GPT(prompt="Tell me a joke.", streaming=True)
    
    await session.start() 
    # send additional prompts and handle them optionally
    print("\n -- asking GPT to explain the joke -- \n")
    await session.handle_prompt("Explain the joke.")

    await session.close()

asyncio.run(run_session())
