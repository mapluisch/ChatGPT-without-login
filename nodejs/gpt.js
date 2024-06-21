const { firefox } = require('playwright');
const { program } = require('commander');

class GPT {
    constructor(prompt, streaming = true, proxy = null) {
        this.prompt = prompt;
        this.streaming = streaming;
        this.proxy = proxy;
        this.browser = null;
        this.page = null;
        this.sessionActive = true;
        this.lastMessageId = null;
    }

    delay(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }

    async start() {
        const launchOptions = { headless: true };
        if (this.proxy) {
            launchOptions.proxy = { server: this.proxy };
        }

        this.browser = await firefox.launch(launchOptions);
        const contextOptions = {
            userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1"
        };
        const context = await this.browser.newContext(contextOptions);
        this.page = await context.newPage();
        await this.page.goto('https://chat.openai.com', { waitUntil: 'networkidle' });
        await this.handlePrompt(this.prompt);
    }

    async handlePrompt(promptText) {
        const promptTextarea = await this.page.$('#prompt-textarea');
        if (!promptTextarea) {
            console.log("Cannot find the prompt input on the webpage. Please check whether you have access to chat.openai.com without logging in via your browser.");
            this.sessionActive = false;
            await this.close();
            return;
        }

        await this.page.type('#prompt-textarea', promptText, { delay: 100 });

        try {
            await this.page.click('[data-testid="send-button"]');
        } catch (e) {
            console.log(`Failed to click the send button: ${e}`);
        }

        await this.waitForAndPrintNewResponse();
    }

    async waitForAndPrintNewResponse() {
        await this.waitForInitialResponse();
        await this.handleStreamingResponse();
    }

    async waitForInitialResponse() {
        const timeout = 30000;
        const startTime = Date.now();
        while ((Date.now() - startTime) < timeout) {
            const assistantMessages = await this.page.$$('[data-message-author-role="assistant"]');
            if (assistantMessages.length > 0) {
                const lastMessage = assistantMessages[assistantMessages.length - 1];
                const isThinking = await lastMessage.$('.result-thinking');
                if (!isThinking) {
                    this.lastMessageId = await this.page.evaluate(element => element.getAttribute('data-message-id'), lastMessage);
                    return;
                }
            }
            await this.delay(100);
        }
        console.log("Timed out waiting for the initial response.");
    }

    async handleStreamingResponse() {
        let previousText = "";
        let completeResponse = "";
        let newContentDetected = false;
        while (!newContentDetected) {
            const assistantMessages = await this.page.$$('[data-message-author-role="assistant"]');
            if (assistantMessages.length > 0) {
                const lastMessage = assistantMessages[assistantMessages.length - 1];
                const currentMessageId = await this.page.evaluate(element => element.getAttribute('data-message-id'), lastMessage);
                
                if (currentMessageId === this.lastMessageId) {
                    const currentText = await this.page.evaluate(element => element.textContent, lastMessage);
                    if (currentText !== previousText) {
                        const newText = currentText.substring(previousText.length);
                        if (this.streaming) {
                            process.stdout.write(newText);
                        } else {
                            completeResponse += newText;
                        }
                    }

                    previousText = currentText;
                    const isStreaming = await lastMessage.$('.result-streaming');
                    if (!isStreaming) {
                        newContentDetected = true;
                    }
                } else {
                    this.lastMessageId = currentMessageId;
                }
            }
            await this.delay(100);
        }
        
        if (!this.streaming) {
            console.log(completeResponse.trim());
        }
    }

    async close() {
        await this.page.close();
        await this.browser.close();
    }
}

async function readLine(question = '') {
    return new Promise((resolve) => {
        process.stdout.write(question);
        process.stdin.resume();
        process.stdin.once('data', (data) => {
            process.stdin.pause();
            resolve(data.toString().trim());
        });
    });
}

function configureCLI() {
    program
        .option('-p, --prompt <type>', 'The initial prompt text to send to ChatGPT', "Hello, GPT")
        .option('-x, --proxy <type>', 'Proxy server to use, e.g. http://proxyserver:port')
        .option('-ns, --no-streaming', 'Disable streaming of ChatGPT responses', false);
    program.parse(process.argv);
    
    const options = program.opts();
    options.streaming = !options.noStreaming;

    return options;
}

if (require.main === module) {
    (async () => {
        const options = configureCLI();
        const session = new GPT(options.prompt, options.streaming, options.proxy);
        await session.start();
    
        while (session.sessionActive) {
            const line = await readLine('\n►: ');
            if (line.toLowerCase() === 'exit') {
                await session.close();
                break;
            } else {
                await session.handlePrompt(line);
            }
        }
        process.exit(0);
    
    })().catch(e => {
        console.error(e);
        process.exit(1);
    });
}

module.exports = { GPT };
