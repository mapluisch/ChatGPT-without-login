<h1 align="center">Headless-ChatGPT</h1>
<p align="center"><em>Python sample on how to access ChatGPT without API. Only for educational purposes.</em></p>

## Heads-up
[OpenAI just announced instant access to ChatGPT 3.5 without signing up](https://openai.com/blog/start-using-chatgpt-instantly); this repo contains a python script for programmatic instant access.

Instant access is currently rolling out and (based on some quick tests of mine) is currently only available in the US and Canada (IP-based).

## Setup / Dependencies
This sample relies on `pyppeteer`, a headless chromium library.

Install it using `pip install pyppeteer` (or `pip3`, depending on your setup).

Then, simply call the script with your prompt as input argument, i.e., `python3 gpt.py -p "Here goes your prompt."`.

Right now, in this first prototype, the "chat" process is really a one-off request. I will add conversation support soon-ish.

## ToDo
- [ ] support response streaming
- [ ] support conversations
- [ ] support different output formats (with / without IDs, json, prettify...)


### Disclaimer
*This python implementation is only meant for educational purposes. Please use OpenAI's API for requests.*

Also, this is a barebones example and still WIP. 
