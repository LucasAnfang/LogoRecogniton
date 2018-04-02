const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const TensorflowController = require('../controllers/tensorflow');

router.get('/training', checkAuth, TensorflowController.fetch_new_batches_and_set);

module.exports = router;