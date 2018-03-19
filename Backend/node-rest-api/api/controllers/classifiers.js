const mongoose = require('mongoose');

const Order = require('../models/order');
const Product = require('../models/product');
const Classifier = require('../models/classifier');

exports.fetch_all_classifiers = (req, res, next) => {
    Classifier.find()
        .select('_id name ownerId description trainingSets subscriberIds isPublic index nodes')
        .populate('nodes', 'name index')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                classifiers: docs.map(doc => {
                    return {
                        _id: doc._id,
                        name: doc.name,
                        ownerId: doc.ownerId,
                        description: doc.description,
                        trainingsSets: doc.trainingsSets,
                        subscriberIds: doc.subscriberIds,
                        // index for tensorflow
                        index: doc.index,
                        nodes: doc.nodes,
                        request: {
                            type: 'GET',
                            url: 'http://localhost:2000/classifiers/' + doc._id
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

exports.create_classifier = (req, res, next) => {
    const classifier = new Classifier({
        _id: new mongoose.Types.ObjectId(),
        // need to find a way to get this from the token?
        name: req.body.name,
        ownerId: req.body.ownerId,
        description: req.body.description,
        trainingsSets: [],
        subscriberIds: [],
        // need to figure out how to get these two automatically
        index: [],
        nodes: [],
    });
    classifier.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /classifiers',
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

//TODO: make this work
exports.fetch_classifier = (req, res, next) => {
    console.log('in fetch classifier')
    const id = req.params.orderId;
    Classifier.findById(id)
        .select('name _id userId parentDatasetId description classifierIndex nodes')
        .populate('nodes', 'trainingData')
        .exec()
        .then(classifier => {
            if (classifier) {
                console.log("classifier is ", classifier);
                res.status(200).json({
                    classifier: classifier,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/classifiers/' //return list of orders
                        //url: 'http://localhost:3000/products/' + order.product //return information on ordered product
                    }
                });
            } else {
                res.status(404).json({message: 'No valid entry found for provided ID'})
            }
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.delete_classifier = (req, res, next) => {
    const id = req.params.classifierId;
    Classifier.remove({ _id: id })
        .exec()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Classifier deleted',
                request: {
                    type: 'POST',
                    url: 'http://localhost:2000/classifier/',
                    body: { classifierId: 'ID' }
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