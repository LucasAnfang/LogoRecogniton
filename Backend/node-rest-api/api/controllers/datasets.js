const mongoose = require('mongoose');
const multer = require('multer');
var PythonShell = require('python-shell');

const fs = require('fs-extra');
const uid = require('uid');

const Order = require('../models/order');
const Product = require('../models/product');
const Dataset = require('../models/dataset');

exports.fetch_all_datasets = (req, res, next) => {
    Dataset.find({ uid: req.userData.userId })
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

exports.upload_images;// = multer() => {

//}
// (req, res, next) => {
//     console.log(req.params.datasetId);
// }

exports.scrape_images = (req, res, next) => {
    try {
        console.log(req.body)
        var hashtag = req.body.hashtag;
        var uid = req.userData.userId;
        var did = req.params.datasetId;
        var image_count = 20;
        var hashtagScrapeResult = {};

        hashtagScrapeResult.hashtag = hashtag;
        var responseImageDirectory = 'datasets/' + uid + '/' + did + '/' + hashtag +'/';
        var outputImageDirectory = 'datasets/' + uid + '/' + did + '/';
        // console.log('Output Image Directory: ' + outputImageDirectory);
        // console.log(process.cwd());
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
    console.log(req.userData);
    const dataset = new Dataset({
        _id: new mongoose.Types.ObjectId(),
        name: req.body.name,
        uid: req.userData.userId,
        //what goes in here
        uploadRequest: {

        },
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