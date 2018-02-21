const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const ScraperController = require('../controllers/scraper');

router.post('/', ScraperController.fetch_images_with_hashtags);


module.exports = router;