import asyncio
from pyppeteer import launch
import argparse

parser = argparse.ArgumentParser(description='Headless ChatGPT Access')
parser.add_argument('-p', '--prompt', type=str, required=True, help='The prompt text to send to ChatGPT')
args = parser.parse_args()

async def main(prompt):
    browser = await launch(headless=True)
    page = await browser.newPage()

    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1"
    await page.setUserAgent(user_agent)

    await page.goto('https://chat.openai.com', waitUntil='networkidle0')
    
    element = await page.querySelector('#prompt-textarea')
    if element:
        await page.type('#prompt-textarea', prompt)
        
        await asyncio.sleep(0.2)

        await page.click('[data-testid="send-button"]')

        # wait for a sec before the response starts to fill up
        await asyncio.sleep(1)

        async def textHasStoppedChanging():
            previousText = None
            while True:
                # grab latest message
                currentText = await page.evaluate('''() => {
                    const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                    const lastMessage = messages[messages.length - 1];
                    return lastMessage ? lastMessage.innerText : '';
                }''')
                
                if currentText == previousText:
                    # text stopped changing -> exit the loop
                    break  
                previousText = currentText
                # await/check again for changes after a short idle time
                await asyncio.sleep(0.1)

        await textHasStoppedChanging()

        # as soon as the response has stopped changing, retrieve the info
        messages_info = await page.evaluate('''() => {
            const messages = Array.from(document.querySelectorAll('[data-message-id]'));
            return messages.map(message => {
                const textContent = message.innerText;
                const messageId = message.getAttribute('data-message-id');
                return { messageId, textContent };
            });
        }''')
        
        for message in messages_info:  
            print(f'Message ID: {message["messageId"]}, Message Text: {message["textContent"]}')
    else:
        print('Error: Could not find #prompt-textarea on the page - are you sure GPT instant access is available for you?')

    await browser.close()

asyncio.run(main(args.prompt))
