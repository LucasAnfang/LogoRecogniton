const mongoose = require('mongoose');
const multer = require('multer');
var PythonShell = require('python-shell');

const fs = require('fs');
const uid = require('uid');

const Order = require('../models/order');
const Product = require('../models/product');
const Dataset = require('../models/dataset');

exports.fetch_all_datasets = (req, res, next) => {
    Dataset.find()
        .select('_id isProcessed uploadRequest completionTimestamp data datasetType')
        .populate('uploadRequest', 'data')
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

exports.upload_images = (req, res, next) => {
    // var imageFileName = new Date().toISOString() + file.originalname;
    console.log(req.body);
    
    // File upload code
    const storage = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, './datasets/' + req.userData.userId + '/' + req.datasetId + '/uploads/');
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
        fileFilter: fileFilter,
        onFileSizeLimit: function (file) {
            // but res (response) object is not existing here
            file.error = {
                message: "Upload failed",
                status: MARankings.Enums.Status.FILE_TOO_LARGE
                // status: -6
            };
        }, onFileUploadComplete: function (file, req, res) {
            if (file.error){
                res.send(file.error);
            }
        }
    });

    upload.array('trainingImages');
    // .then(result => {
    //     console.log(result);
    //     res.status(200).json({
    //         message: 'Handling POST request to /datasets',
    //         uploadedImage: {
    //             // name: result.name,
    //             // price: result.price,
    //             // _id: result._id,
    //             // request: {
    //             //     type: 'GET',
    //             //     url: 'http://localhost:2000/products/' + result._id
    //             // }
    //         }
    //     });
    // });
}

exports.scrape_images = (req, res, next) => {
    var hashtag = req.body.hashtag;
    var uid = req.userData.userId;
    var image_count = 100;
    var hashtagScrapeResult = {};

    hashtagScrapeResult.hashtag = hashtag;
    
    var outputImageDirectory = './datasets/' + uid + '/' + req.params.datasetId + '/';
    console.log('Output Image Directory: ' + outputImageDirectory);
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
        console.log('Scrape results: %j', results);
        var files = fs.readdirSync(outputImageDirectory);
        scrapedImages = files.map(filename => outputImageDirectory + results);
        hashtagScrapeResult.fullPaths = scrapedImages;
        res.status(200).json({
            hashtagScrapeResult
        });
    })
    // .end(function (err) {
    //     if (err) {
    //         console.log(err);
    //         res.status(500).json({
    //             error: err
    //         });
    //     }
    //     console.log('Scrape results: %j', results);
    //     var files = fs.readdirSync(outputImageDirectory);
    //     scrapedImages = files.map(filename => outputImageDirectory + results);
    //     hashtagScrapeResult.fullPaths = scrapedImages;
    //     res.status(200).json({
    //         hashtagScrapeResult
    //     });
    // });
    // .then(result => {
    //     res.status(200).json({
    //                 message: 'Handling POST request to /datasets/hashtag',
    //                 uploadedImage: {
    //                     // name: result.name,
    //                     // price: result.price,
    //                     // _id: result._id,
    //                     // request: {
    //                     //     type: 'GET',
    //                     //     url: 'http://localhost:2000/products/' + result._id
    //                     // }
    //                 }
    //             });
    // });
}

exports.create_dataset = (req, res, next) => {
    console.log(req.userData);
    const dataset = new Dataset({
        _id: new mongoose.Types.ObjectId(),
        //what goes in here
        uploadRequest: {

        },
        //what goes in here x2
        data: {

        },
        datasetType: req.body.datasetType
    });
    dataset.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /datasets',
                createdDataset: {
                    name: result.name,
                    _id: result._id,
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
    const id = req.params.orderId;
    Dataset.findById(id)
        //maybe remove data
        .select('_id isProcessed uploadRequest completionTimestamp data datasetType')
        .populate('uploadRequest', 'data')
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

exports.delete_dataset = (req, res, next) => {
    const id = req.params.datasetId;
    Dataset.remove({ _id: id })
        .exec()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Dataset deleted',
                request: {
                    type: 'POST',
                    url: 'http://localhost:2000/datasets/',
                    body: { productId: 'ID' }
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