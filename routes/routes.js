const express = require("express");
const router = express.Router();
const { home } = require("../controllers/home_controller.js");


router.get('/', home);

module.exports = router;
