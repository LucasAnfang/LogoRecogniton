const express = require('express');
const router = express.Router();

const ServicesController = require('../controllers/services');

router.get('/', ServicesController.fetch_hashtag);


module.exports = router;