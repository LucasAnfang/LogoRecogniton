const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const BatchController = require('../controllers/batches');

router.get('/', checkAuth, BatchController.fetch_all_batches);

router.post('/', checkAuth, BatchController.create_batch);

router.get('/:classifierId', checkAuth, BatchController.fetch_batch);

router.delete('/:classifierId', checkAuth, BatchController.delete_batch);

module.exports = router;