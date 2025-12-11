//in home controller
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



// Define AI Agent Configuration and Deployment
const {PutConnectionStringOperation, GetConnectionStringsOperation, AiAgentConfiguration} = require("ravendb");

async function setupAgent(store) {
    console.log("Setting up AI Agent...");


   // Get all connection strings
    const allConnectionStrings = await store.maintenance.send(new GetConnectionStringsOperation());

    // Check if Ollama connection string exists
    const existing = allConnectionStrings.aiConnectionStrings?.["ollama-local-1"];
    //console.log(allConnectionStrings.aiConnectionStrings?.["ollama-local"]);
    
    if (!existing) {
        // Create it if missing
        const ollamaConnectionString = {
            Name: "ollama-local-1",
            type: "Ai",   // MUST match what the server expects
            modelType: 'Chat',
            ollamaSettings: {
                Uri: "http://localhost:11434",
                Model: "llama3.1" //gemma3
            }
        };
            console.log("ollamaConnectionString: ", ollamaConnectionString);

            await store.maintenance.send(new PutConnectionStringOperation(ollamaConnectionString));
            console.log("Ollama connection string created successfully!");
        var ollamaSettings = ollamaConnectionString.ollamaSettings;
    }
    else{
        var ollamaSettings =  existing.ollamaSettings;
    }
    //console.log("ollamaSettings",ollamaSettings);
    //console.log(store.ai);
    // 2b. Define the Agent Configuration (AiAgentConfiguration)
    
    const agentConfig = agentConfiguration;
    agentConfig.connectionStringName="ollama-local-1";
    //  Register the Agent
    const agent = await store.ai.createAgent(agentConfig, agentConfig.sampleOutputObject);    
    console.log("AI Agent configuration and creation (Conceptual) skipped.");
    return agent;
};





const agentConfiguration = {
    name: "ravendb-ai-agent",
    connectionStringName: "<Your connection string name>",
    systemPrompt: `
        You work for a human experience manager.
        The manager uses your services to find which employee earned the largest profit
        for the company and suggest a reward for this employee.
        The manager provides you with the name of a country, or with the word "everything"
        to indicate all countries.

        Steps:
        1. Use a query tool to load all orders sent to the selected country (or all countries).
        2. Calculate which employee made the largest profit.
        3. Use a query tool to learn in what region the employee lives.
        4. Find suitable vacation sites or other rewards based on the employee's region.
        5. Use an action tool to store the employee's ID, profit, and reward suggestions in the database.

        When you're done, return these details in your answer to the user as well.
    `,
    sampleObject: JSON.stringify({
        employeeID: "the ID of the employee that made the largest profit",
        profit: "the profit the employee made",
        suggestedReward: "your suggestions for a reward"
    }),
    parameters: [
        {
            name: "country",
            description: "A specific country that orders were shipped to, or 'everywhere' to look at all countries"
        }
    ],
    maxModelIterationsPerCall: 3,
    chatTrimming: {
        tokens: {
            maxTokensBeforeSummarization: 32768,
            maxTokensAfterSummarization: 1024
        }
    },
    // Queries the agent can use
    queries: [
        {
            name: "retrieve-orders-sent-to-a-specific-country",
            description: "Retrieve all orders sent to a specific country",
            query: "from Orders as O where O.ShipTo.Country == $country select O.Employee, O.Lines.Quantity",
            parametersSampleObject: "{}"
        },
        {
            name: "retrieve-performer-living-region",
            description: "Retrieve an employee's country, city, and region by employee ID",
            query: "from Employees as E where id() == $employeeId select E.Address.Country, E.Address.City, E.Address.Region",
            parametersSampleObject: "{ \"employeeId\": \"embed the employee's ID here\" }"
        }
    ],
    // Actions the agent can perform
    actions: [
        {
            name: "store-performer-details",
            description: "Store the employee ID, profit, and suggested reward in the database.",
            parametersSampleObject: "{ \"employeeID\": \"embed the employee's ID here\", \"profit\": \"embed the employee's profit here\", \"suggestedReward\": \"embed your suggestions for a reward here\" }"
        }
    ]
};



module.exports = { setupAgent };
