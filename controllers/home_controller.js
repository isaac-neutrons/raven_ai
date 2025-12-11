const { setupAgent } = require("../services/ai_agent.js");

const home = async (req, res) => {
    const session = req.dbSession;
    // Initialize agent on startup that can be moved in the index.js
    const agent = await setupAgent(req.dbstore);
    console.log("agent.identifier", agent.identifier);
    console.log("home");

    const chat = req.dbstore.ai.conversation(agent.identifier, "Performers/",
        {parameters: {country: "France"}}
    );

    // 3. Set the user prompt
    chat.setUserPrompt("Find the employee with the largest profit and suggest a reward");

    // 4. Run the conversation (Node.js returns full response)
    const response = await chat.run();

    // 5. Access the specific property defined in your agent schema
    console.log("Suggested reward:", response.suggestedReward);

    // Optional: inspect full response object
    console.log("Full agent response:", response);

    res.json(response);

    // // Register action handler
    // chat.handle("store-performer-details", async (req, performer) => {
    //     const session = req.dbSession;
    //     await session.store(performer);
    //     await session.saveChanges();
    //     session.dispose();
    //     return {success: true};
    // });

    // chat.setUserPrompt("Find the employee with largest profit and suggest rewards");

    // // Stream the "suggestedReward" property
    // let chunkedText = "";
    // const answer = await chat.stream("suggestedReward", async (chunk) => {
    //     // Called for each streamed chunk
    //     chunkedText += chunk;
    // });

    // console.log("chunkedText", chunkedText);

    // console.log("Final answer:", answer);

    //example for db connection
    // session.load('employees/1-A')
    //     .then(employee => {
    //         if (employee) {
    //             res.send(`Employee Last Name: ${employee.LastName}`);
    //         } else {
    //             res.status(404).send('Employee not found');
    //         }
    //         return session.saveChanges();
    //     })
};

// Run the demo
//runAgentChat().catch(err => console.error(err));

module.exports = { home };
