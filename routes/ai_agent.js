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

const agent = await store.ai.createAgent(agentConfiguration);