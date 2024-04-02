const puppeteer = require('puppeteer');
const { program } = require('commander');
const readline = require('readline');

class GPT {
    constructor(prompt, streaming = true) {
        this.prompt = prompt;
        this.streaming = streaming;
        this.browser = null;
        this.page = null;
    }

    delay(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }

    async start() {
        this.browser = await puppeteer.launch({headless: true});
        this.page = await this.browser.newPage();
        await this.page.setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1");
        await this.page.goto('https://chat.openai.com', { waitUntil: 'networkidle0' });
        await this.handlePrompt(this.prompt);
    }

    async handlePrompt(promptText) {
        await this.page.waitForSelector('#prompt-textarea', {timeout: 5000});
        await this.page.type('#prompt-textarea', promptText);
        await this.page.waitForSelector('[data-testid="send-button"]', {timeout: 5000});
        await this.page.click('[data-testid="send-button"]');
        await this.delay(1000);

        let isGptThinking = await this.page.$('.result-thinking');
        if (isGptThinking) {
            await this.page.waitForSelector('.result-thinking', { hidden: true });
        }

        await this.streamingResponse();
    }

    async streamingResponse() {
        let previousText = "";
        let printedLength = 0;
        while (true) {
            let currentText = await this.page.evaluate(() => {
                const messages = Array.from(document.querySelectorAll('[data-message-id]'));
                const lastMessage = messages[messages.length - 1];
                return lastMessage ? lastMessage.innerText : '';
            });

            let chunk = currentText.slice(printedLength);
            if (this.streaming) process.stdout.write(chunk);
            printedLength += chunk.length;

            if (currentText === previousText) {
                if (!this.streaming) console.log(currentText);
                console.log("\n");
                break;
            }
            previousText = currentText;
            await this.delay(100);
        }
    }

    async close() {
        if (this.browser !== null) {
            await this.browser.close();
        }
    }
}

function configureCLI() {
    program
        .requiredOption('-p, --prompt <type>', 'The initial prompt text to send to ChatGPT')
        .option('-ns, --no-streaming', 'Disable streaming of ChatGPT responses');
    program.parse(process.argv);
    
    const options = program.opts();

    return options;
}

if (require.main === module) {
    (async () => {
        const options = configureCLI();
        const session = new GPT(options.prompt, options.streaming);
        await session.start();
    
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            prompt: '|>: '
        });

        rl.prompt();
    
        rl.on('line', async (line) => {
            if (line.toLowerCase() === 'exit') {
                await session.close();
                process.exit(0);
            } else {
                await session.handlePrompt(line);
                rl.prompt();
            }
        }).on('close', () => {
            console.log('Conversation ended.');
        });
    
    })().catch(e => {
        console.error(e);
        process.exit(1);
    });
}

module.exports = {GPT};