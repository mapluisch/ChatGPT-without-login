const { GPT } = require('./gpt.js');

(async () => {
    try {
        // create gpt instance & send initial prompt
        const gptSession = new GPT("Tell me a joke.", true);

        await gptSession.start();
        
        // (optional) send additional prompts and handle them
        console.log("\n -- asking GPT to explain the joke -- \n")
        await gptSession.handlePrompt("Explain the joke.");

        // gracefully close the session again
        await gptSession.close();
    } catch (error) {
        console.error("Error in GPT session:", error);
    }
})();