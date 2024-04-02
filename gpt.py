import asyncio
from pyppeteer import launch
import argparse

parser = argparse.ArgumentParser(description='Headless ChatGPT Access with Interactive Conversation Option')
parser.add_argument('-p', '--prompt', type=str, required=True, help='The initial prompt text to send to ChatGPT')
parser.add_argument('-s', '--streaming', action='store_true', help='Enable streaming of ChatGPT responses')
parser.add_argument('-c', '--conversation', action='store_true', help='Enable conversation mode to continue interacting without reloading the page')
args = parser.parse_args()

async def main(prompt, streaming, conversation):
    browser = await launch(headless=True)
    page = await browser.newPage()

    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1"
    await page.setUserAgent(user_agent)

    await page.goto('https://chat.openai.com', waitUntil='networkidle0')

    async def handle_prompt_submission(prompt_text):
        element = await page.querySelector('#prompt-textarea')
        if element:
            await element.focus()

            await page.type('#prompt-textarea', prompt_text)
            await page.click('[data-testid="send-button"]')
            await asyncio.sleep(1)
            
            is_gpt_thinking = await page.querySelector('.result-thinking')
            if is_gpt_thinking:
                await page.waitForSelector('.result-thinking', options={'hidden': True})


            async def textHasStoppedChanging():
                printedLength = 0
                previousText = ""
                while True:
                    gpt_chunk = await page.evaluate('''() => {
                        const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                        const lastMessage = messages[messages.length - 1];
                        return lastMessage ? lastMessage.innerText : '';
                    }''')

                    if streaming:
                        newChunk = gpt_chunk[printedLength:]
                        print(newChunk, end='', flush=True)
                        printedLength += len(newChunk)

                    if gpt_chunk == previousText:
                        break
                    previousText = gpt_chunk
                    await asyncio.sleep(0.1)

            await textHasStoppedChanging()

            if not streaming:
                gpt_response = await page.evaluate('''() => {
                    const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                    const lastMessage = messages[messages.length - 1];
                    return lastMessage ? lastMessage.innerText : 'No messages found.';
                }''')

                print(gpt_response)
        else:
            print('Error: Could not find #prompt-textarea on the page.')

    await handle_prompt_submission(prompt)

    if conversation:
        try:
            while True:
                next_prompt = input("\n|>: ")
                if next_prompt.lower() == 'exit':
                    break
                await handle_prompt_submission(next_prompt)
        except KeyboardInterrupt:
            pass

    await browser.close()

asyncio.run(main(args.prompt, args.streaming, args.conversation))
