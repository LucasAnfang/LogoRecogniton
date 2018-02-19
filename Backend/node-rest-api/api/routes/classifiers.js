const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const ClassifierController = require('../controllers/classifiers');

router.get('/', checkAuth, ClassifierController.fetch_all_classifiers);

router.post('/', checkAuth, ClassifierController.create_classifier);

router.get('/:classifierId', checkAuth, ClassifierController.fetch_classifier);

router.delete('/:classifierId', checkAuth, ClassifierController.delete_classifier);

module.exports = router;