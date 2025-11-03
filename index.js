const express = require('express');
const fs = require('fs');
const { DocumentStore } = require('ravendb');

const app = express();

// index.js
console.log("Hello!");



app.get('/', (req, res) => {
      //const authOptions = {
      //certificate: fs.readFileSync("C:\\path_to_your_pfx_file\\cert.pfx"),
      //type: "pfx", // or "pem"
      //};

      const store = new DocumentStore("http://127.0.0.1:8080", "isaac_db"); //authOptions
      store.initialize();

      const session = store.openSession('isaac_db');
      session.load('employees/1-A')
          .then(employee => {
              if (employee) {
                  res.send(`Employee Last Name: ${employee.LastName}`);
              } else {
                  res.status(404).send('Employee not found');
              }
              return session.saveChanges();
          })

          .then(() => {
              store.dispose();
          })
});

app.listen(3000, () => console.log('Server is running on http://localhost:3000'));

