const mongoose = require('mongoose');
const multer = require('multer');
var PythonShell = require('python-shell');

const fs = require('fs-extra');
const uid = require('uid');

const Order = require('../models/order');
const Product = require('../models/product');
const Dataset = require('../models/dataset');

exports.fetch_all_datasets = (req, res, next) => {
    // console.log(req.userData.userId);
    Dataset.find({
        'userId': req.userData.userId
    })
    .select('_id name')
    .exec() //turn it into a real promise
    .then(docs => {
        console.log(docs);
        res.status(200).json({
            count: docs.length,
            classifiers: docs.map(doc => {
                return {
                    _id: doc._id,
                    isProcessed: doc.isProcessed,
                    uploadRequest: doc.uploadRequest,
                    completionTimestamp: doc.completionTimestamp,
                    data: doc.data,
                    datasetType: doc.datasetType,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/datasets/' + doc._id
                    }
                };
            })
        });
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        });
    });
}

exports.upload_images;// = multer() => {

//}
// (req, res, next) => {
//     console.log(req.params.datasetId);
// }

exports.scrape_images = (req, res, next) => {
    try {
        var hashtag = req.body.hashtag;
        var uid = req.userData.userId;
        var d_id = req.params.datasetId;
        var image_count = 20;
        var hashtagScrapeResult = {};

        hashtagScrapeResult.hashtag = hashtag;
        var responseImageDirectory = 'datasets/' + d_id + '/' + hashtag +'/';
        var outputImageDirectory = 'datasets/' + d_id + '/';
        var options = {
            scriptPath: './api/iron_python/instagram_scraper',
            args: ['-hi', hashtag, '-d', outputImageDirectory, '-m', image_count]
        };
        PythonShell.run('IGScraperTool.py', options, function (err, results) {
            if (err) {
                console.log(err);
                res.status(500).json({
                    error: err
                });
            }
            var files = fs.readdirSync(responseImageDirectory);
            fullFilenames = files.map(filename => 'http://localhost:2000/' + responseImageDirectory + filename);
            res.status(201).json({
                hashtag: hashtag,
                filePaths: fullFilenames
            });
        });
    }
    catch(err) {
        console.log(err);
        res.status(500).json({
            error: err
        });
    }
}

exports.create_dataset = (req, res, next) => {
    // console.log(req.userData);
    const dataset = new Dataset({
        _id: new mongoose.Types.ObjectId(),
        name: req.body.name,
        userId: req.userData.userId,
        //what goes in here
        uploadRequest: {},
        //what goes in here x2
        data: {},
        datasetType: req.body.datasetType
    });
    dataset.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /datasets',
                createdDataset: {
                    _id: result._id,
                    name: result.name,
                    datasetType: result.datasetType,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/datasets/' + result._id
                    }
                }
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.fetch_dataset = (req, res, next) => {
    console.log(req.userData.userId);
    const id = req.params.datasetId;
    Dataset.findById(id)
        //maybe remove data
        .select('_id')// name')
        // .populate('uploadRequest', 'data')
        .exec()
        .then(dataset => {
            if (dataset) {
                res.status(200).json({
                    dataset: dataset,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/datasets/' + dataset._id

                    }
                });
            } else {
                res.status(404).json({message: 'No valid dataset found for provided ID'})
            }
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.create_classifier = (req, res, next) => {
    
    const classifier = new Classifier({
        _id: new mongoose.Types.ObjectId(),
        // need to find a way to get this from the token?
        name: req.body.name,
        ownerId: req.userData.userId,
        description: req.body.description,
        subscriberIds: [],
        // need to figure out how to get these two automatically
        index: [],
        nodes: [],
    });
    classifier.save()
    .then(result => {
        console.log(result);
        res.status(200).json({
            message: 'Handling POST request to /datasets/' + req.params.datasetId + '/classifiers',
            createdClassifier: {
                name: result.name,
                ownerId: result.ownerId,
                description: req.body.description,
                _id: result._id,
                request: {
                    type: 'GET',
                    url: 'http://localhost:2000/classifiers/' + result._id
                }
            }
        });
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({ 
            error: err 
        });
    });
}


exports.delete_dataset = (req, res, next) => {
    var id = req.params.datasetId;
    var uid = req.userData.userId;

    if (!mongoose.Types.ObjectId.isValid(id)) {
        res.status(400).json({ 
            error: "DatasetID is not a valid ID"
        });
    }
    else {
        Dataset.findOne({ _id: id}, function (err, docs){
            // need to fix error codes
            if (!docs) {
                res.status(400).json({ 
                    error: "Dataset doesn't exist"
                });
            } else {
                if (docs.userId != uid) {
                    res.status(400).json({ 
                        error: "Dataset doesn't belong to user"
                    });
                } else {
                    Dataset.remove({ _id: id, userId: uid })
                    .exec()
                    .then(result => {
                        res.status(200).json({
                            message: 'Dataset Deleted',
                            request: {
                                type: 'POST',
                                url: 'http://localhost:2000/datasets'
                            }
                        });
                    })
                    .catch(err => {
                        console.log(err);
                        res.status(500).json({ 
                            error: err
                        });
                    });
                }
            }
        }); 
    }
}