<h1 align="center">Headless-ChatGPT</h1>
<p align="center"><em>Python sample on how to access ChatGPT without API. Only for educational purposes.</em></p>

## Heads-up
[OpenAI just announced instant access to ChatGPT 3.5 without signing up](https://openai.com/blog/start-using-chatgpt-instantly); this repo contains a python script for programmatic instant access.

Instant access is currently rolling out and (based on some quick tests of mine) is currently only available in the US and Canada (IP-based).

## Setup / Dependencies
This sample relies on `pyppeteer`, a headless chromium library.

Install it using `pip install pyppeteer` (or `pip3`, depending on your setup).

Then, clone this repo and run `python3 gpt.py` with the arguments described below.

## Usage
### Arguments
- `-p`, `--prompt` (required)
  - the initial prompt text to send to ChatGPT.
  - **type**: `str`
  
- `-s`, `--streaming`
  - if true, the script prints out the response from ChatGPT as it's being generated, creating a "streaming" effect.
  - **type**: bool (`store_true`)
  - **default**: false
  
- `-c`, `--conversation`
  - if true, allows the user to send new prompts after receiving a response, facilitating an ongoing conversation with GPT.
  - **type**: bool (`store_true`)
  - **Default**: false

For one-off queries, simply call the script with your prompt as input argument `-p / --prompt`, i.e., `python3 gpt.py -p "Here goes your prompt."`.

Add the other arguments if you want "streaming"-esque responses and / or conversations.


## ToDo
- [x] support response streaming
- [x] support conversations
- [ ] support different output formats (with / without IDs, json, prettify...)


### Disclaimer
*This python implementation is only meant for educational purposes. Please use OpenAI's API for requests.*

Also, this is a barebones example and still WIP. 
