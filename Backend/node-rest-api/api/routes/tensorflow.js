const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');
const multer = require('multer');
const TensorflowController = require('../controllers/tensorflow');

// appends timestamp to checkpoint
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
      cb(null, '././tmp_checkpoints/');
    },
    filename: function(req, file, cb) {
      cb(null, new Date().toISOString() + file.originalname);
    }
  });

  const upload = multer({
    storage: storage
  });

router.get('/training', checkAuth, TensorflowController.fetch_training_batches_and_set);
router.get('/classify', checkAuth, TensorflowController.fetch_classify_batches_and_set);
router.post('/checkpoint/upload', checkAuth, upload.single('checkpoint'), TensorflowController.store_checkpoints);
router.get('/checkpoint/fetch', checkAuth, TensorflowController.fetch_checkpoint);
// router.post('/accuracy', checkAuth, TensorflowController.store_accuracy);
router.post('/completedTraining', checkAuth, TensorflowController.set_completed_classifier_statuses);
router.post('/results', checkAuth, TensorflowController.store_results);

module.exports = router;
