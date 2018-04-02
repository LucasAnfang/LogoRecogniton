const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const ClassifierController = require('../controllers/classifiers');

router.post('/', checkAuth, ClassifierController.fetch_all_classifiers);

module.exports = router;