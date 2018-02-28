const mongoose = require('mongoose');

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
    // const product = new Product({
    //     _id: new mongoose.Types.ObjectId(),
    //     name: req.body.name,
    //     price: req.body.price,
    //     productImage: req.file.path
    // });
    // product.save()
    //     .then(result => {
    //         console.log(result);
    //         res.status(200).json({
    //             message: 'Handling POST request to /products',
    //             createdProduct: {
    //                 name: result.name,
    //                 price: result.price,
    //                 _id: result._id,
    //                 request: {
    //                     type: 'GET',
    //                     url: 'http://localhost:2000/products/' + result._id
    //                 }
    //             }
    //         });
    //     })
    //     .catch(err => {
    //         console.log(err);
    //         res.status(500).json({ 
    //             error: err 
    //         });
    //     });
}

exports.create_dataset = (req, res, next) => {
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