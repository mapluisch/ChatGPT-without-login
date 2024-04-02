<div align="center">
  <h1 align="center">Scripts for using ChatGPT without login</h1>
  <img src="https://github.com/mapluisch/ChatGPT-without-login/assets/31780571/2852ec02-9971-409b-8050-0101c9b2e856">
  <p align="center"><em>Example for accessing ChatGPT (3.5) without an account or API access via Python. Only for educational purposes.</em></p>
</div>
<hr>


## Heads-up
[OpenAI just announced instant access to ChatGPT 3.5 without signing up](https://openai.com/blog/start-using-chatgpt-instantly); this repo contains scripts in multiple programming languages for programmatic instant access, i.e., headless chats with ChatGPT via https://chat.openai.com (without signing up or requiring API keys).

Instant access is currently rolling out and (based on some quick tests of mine) is currently only available in the US and Canada (IP-based).

## Supported Languages

- Python
- JavaScript (Node.js)

## Python

### Setup / Dependencies
Grab the `gpt.py` script from within the `python` directory.

The script relies on `pyppeteer`, a headless chromium library.

Install it using `pip install pyppeteer` (or `pip3`, depending on your setup).

### Usage

#### Calling it from your own script
With my `gpt.py` in the same directory, you can call it using some prompt using this example:
```python
import asyncio
from gpt import GPT

async def run_session():
    session = GPT(prompt="Tell me a joke.", streaming=True)
    
    await session.start() 
    
    # send additional prompts and handle them optionally
    # await session.handle_prompt("Explain the joke.")

    await session.close()

asyncio.run(run_session())
```

The first prompt of a *new* session always takes a bit longer, as the headless browser has to init. Subsequent prompts are handled as fast as you know it from the typical GPT browser UI.

#### CLI Arguments
You can also chat with GPT using CLI; just call `python3 gpt.py` with the following args:

- `-p`, `--prompt` (required)
  - the initial prompt text to send to ChatGPT.
  - **type**: `str`
  
- `-ns`, `--no-streaming`
  - if true, the script doesn't print GPT's response in chunks ("streaming"-esque), but rather waits until it is fully typed out before printing it.
  - **type**: bool (`store_true`)
  - **default**: false

A minimal example for a streaming-based conversation would be `python3 gpt.py -p "Hello, GPT"`.

## Node.js

### Setup / Dependencies
Grab the `gpt.js` script from within the `nodejs` directory.

The Node.js script relies on `puppeteer`, a headless chromium library, and `commander`.

Install both using `npm install puppeteer commander`.

### Usage

#### Calling it from your own script
With `gpt.js` in the same directory, you can call it using some prompt using this example:
```javascript
const { GPT } = require('./gpt.js');

(async () => {
    try {
        // create gpt instance & send initial prompt
        const gptSession = new GPT("Tell me a joke.", true);

        await gptSession.start();
        
        // (optional) send additional prompts and handle them
        await gptSession.handlePrompt("Explain the joke.");

        await gptSession.close();
    } catch (error) {
        console.error("Error in GPT session:", error);
    }
})();
```

The first prompt of a *new* session always takes a bit longer, as the headless browser has to init. Subsequent prompts are handled as fast as you know it from the typical GPT browser UI.

#### CLI Arguments
You can also chat with GPT using Node CLI; call `node gpt.js` with the following args:

- `-p`, `--prompt` (required)
  - the initial prompt text to send to ChatGPT.
  - **type**: `str`
  
- `-ns`, `--no-streaming`
  - if true, the script doesn't print GPT's response in chunks ("streaming"-esque), but rather waits until it is fully typed out before printing it.
  - **type**: bool (`store_true`)
  - **default**: false

A minimal example for a streaming-based conversation would be `node gpt.js -p "Hello, GPT"`.

## ToDo
- [x] support response streaming
- [x] support conversations
- [ ] support different output formats (with / without IDs, json, prettify...)


### Disclaimer
*This project is only meant for educational purposes. Please use OpenAI's API for requests.*

Also, this is a barebones example and still WIP - if you find issues / bugs, please report them 😊
