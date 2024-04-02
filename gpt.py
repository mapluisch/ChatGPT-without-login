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

            await page.keyboard.down('Control')
            await page.keyboard.press('A')
            await page.keyboard.up('Control')
            await page.keyboard.press('Backspace')

            await page.type('#prompt-textarea', prompt_text)
            
            await asyncio.sleep(0.2)
            await page.click('[data-testid="send-button"]')
            await asyncio.sleep(1)  

            async def textHasStoppedChanging():
                printedLength = 0
                previousText = ""
                while True:
                    currentText = await page.evaluate('''() => {
                        const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                        const lastMessage = messages[messages.length - 1];
                        return lastMessage ? lastMessage.innerText : '';
                    }''')

                    if streaming:
                        newChunk = currentText[printedLength:]
                        print(newChunk, end='', flush=True)
                        printedLength += len(newChunk)

                    if currentText == previousText:
                        break
                    previousText = currentText
                    await asyncio.sleep(0.1)

            await textHasStoppedChanging()

            if not streaming:
                messages_info = await page.evaluate('''() => {
                    const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                    return messages.map(message => {
                        const textContent = message.innerText;
                        const messageId = message.getAttribute('data-message-id');
                        return { messageId, textContent };
                    });
                }''')

                for message in messages_info:
                    print(message["textContent"])
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
