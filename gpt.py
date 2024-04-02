import asyncio
from pyppeteer import launch
import argparse

class GPT:
    def __init__(self, prompt, streaming=True):
        self.prompt = prompt
        self.streaming = streaming
        self.browser = None
        self.page = None

    async def start(self):
        self.browser = await launch(headless=True)
        self.page = await self.browser.newPage()
        await self.page.setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1")
        await self.page.goto('https://chat.openai.com', waitUntil='networkidle0')
        await self.handle_prompt(self.prompt)

    async def handle_prompt(self, prompt_text):
        await self.page.type('#prompt-textarea', prompt_text)
        await self.page.click('[data-testid="send-button"]')
        await asyncio.sleep(1)
        
        is_gpt_thinking = await self.page.querySelector('.result-thinking')
        if is_gpt_thinking:
            await self.page.waitForSelector('.result-thinking', options={'hidden': True})

        await self.streaming_response()

    async def streaming_response(self):
        printedLength = 0
        previousText = ""
        while True:
            currentText = await self.page.evaluate('() => { const messages = Array.from(document.querySelectorAll("[data-message-id]")); const lastMessage = messages[messages.length - 1]; return lastMessage ? lastMessage.innerText : ""; }')
            chunk = currentText[printedLength:]
            # print response chunk-by-chunk (if streaming = true, which it is by default)
            if self.streaming: print(chunk, end='', flush=True)
            printedLength += len(chunk)

            # text hasnt changed, i.e. response is fully printed out
            if currentText == previousText:
                # print response in full (if streaming is manually set to false via -ns // --no-streaming)
                if not self.streaming: print(currentText)
                break
            previousText = currentText
            await asyncio.sleep(0.1)

    async def close(self):
        await self.browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Headless ChatGPT Access with Interactive Conversation Option')
    parser.add_argument('-p', '--prompt', type=str, required=True, help='The initial prompt text to send to ChatGPT')
    parser.add_argument('-ns', '--no-streaming', dest='streaming', action='store_false', help='Disable streaming of ChatGPT responses')
    args = parser.parse_args()

    async def main():
        session = GPT(args.prompt, args.streaming)
        await session.start()
        try:
            while True:
                next_prompt = input("\n|>: ")
                if next_prompt.lower() == 'exit':
                    break
                await session.handle_prompt(next_prompt)
        except KeyboardInterrupt:
            pass
        await session.close()

    asyncio.run(main())
