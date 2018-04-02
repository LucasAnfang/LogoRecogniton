const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const TensorflowController = require('../controllers/tensorflow');

// router.get('/', checkAuth, ClassifierController.fetch_all_classifiers);

module.exports = router;