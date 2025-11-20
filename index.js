const routes = require("./routes/routes.js");

const express = require('express');
const fs = require('fs');
const { DocumentStore } = require('ravendb');

const RAVENDB_SERVER_URL = "http://127.0.0.1:8080"; 
const DB = "isaac_db";
const APP_PORT = process.env.PORT || 3000;

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));


const store = new DocumentStore(RAVENDB_SERVER_URL, DB);
store.initialize();

console.log("Hello!");




// middleware
app.use((req, res, next) => {
  req.dbstore = store;
  req.dbSession = store.openSession();
  next();
});

app.use((error, req, res, next) => {
  res.status(error.status || 500);
  console.log("ERROR", error);
  res.json({
    error: {
      message: error.message,
      status: error.status,
    },
  });
});


// Routes
app.use("/", routes);

//localhost and port
app.listen(APP_PORT, () => console.log(`Server is running on http://localhost:${APP_PORT}`));

