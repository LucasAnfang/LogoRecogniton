const express = require('express');
const multer = require('multer');
const router = express.Router();

const checkAuth = require('../middleware/check-auth');
const DatasetController = require('../controllers/datasets');

const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './datasets/' + req.userData.userId + '/' + req.body.datasetId + '/uploads');
    },
    filename: function(req, file, cb) {
        cb(null, new Date().toISOString() + file.originalname);
    }
});

const fileFilter = (req, file, cb) => {
    // reject a file
    if (file.mimetype === 'image/jpeg' || file.mimetype === 'image/png') {
        cb(null, true); 
    }
    else { 
        cb(null, false); 
    }
};

const upload = multer({
    storage: storage, 
    limits: {
        fileSize: 600 * 600 * 5
    },
    fileFilter: fileFilter
});


//datasets
router.get('/', checkAuth, DatasetController.fetch_all_datasets);
router.post('/', checkAuth, DatasetController.create_dataset);
router.post('/:datasetId/upload', checkAuth, upload.array('trainingImages'));
router.post('/:datasetId/scrape', checkAuth, DatasetController.scrape_images);
router.get('/:datasetId', checkAuth, DatasetController.fetch_dataset);
router.delete('/:datasetId', checkAuth, DatasetController.delete_dataset);

//classifiers
router.post('/:datasetId/classifiers', checkAuth, DatasetController.create_classifier);
router.get('/:datasetId/classifiers', checkAuth, DatasetController.fetch_dataset_classifiers);
// router.get('/:datasetId/classifiers/:classifierId', checkAuth, DatasetController.fetch_dataset_classifiers);
// router.patch('/:datasetId/classifiers/:classifierId', checkAuth, DatasetController.update_classifier);

module.exports = router;