const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const TensorflowController = require('../controllers/tensorflow');

router.get('/training', checkAuth, TensorflowController.fetch_new_batches_and_set);
router.post('/checkpoints', checkAuth, TensorflowController.store_checkpoints);
router.post('/results', checkAuth, TensorflowController.store_results);

module.exports = router;
