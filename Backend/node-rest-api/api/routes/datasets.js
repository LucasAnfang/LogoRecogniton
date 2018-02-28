const express = require('express');
const router = express.Router();
const multer = require('multer');
const checkAuth = require('../middleware/check-auth');

var PythonShell = require('python-shell');
const uid = require('uid'); 
const fs = require('fs');

// File upload code
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './datasets/' + uid + '/uploads/');
        //get the userid from the token
        //get the dataset id
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

const DatasetController = require('../controllers/datasets');

// TODO: return only the datasets for a uid
router.get('/', checkAuth, DatasetController.fetch_all_datasets);
// router.get('/', DatasetController.fetch_all_datasets);
router.post('/', checkAuth, DatasetController.create_dataset);
// router.post('/', DatasetController.create_dataset);
// router.post('/upload/:datasetId', checkAuth, upload.single('trainingImage'), DatasetController.upload_dataset);
router.post('/:datasetId/upload', checkAuth, DatasetController.upload_images);

router.post('/:datasetId/scrape', checkAuth, DatasetController.scrape_images);

router.get('/:datasetId', checkAuth, DatasetController.fetch_dataset);
// router.get('/:datasetId', DatasetController.fetch_dataset);
router.delete('/:datasetId', checkAuth, DatasetController.delete_dataset);
// router.delete('/:datasetId', DatasetController.delete_dataset);

module.exports = router;