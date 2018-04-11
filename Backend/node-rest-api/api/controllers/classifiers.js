const mongoose = require('mongoose');

const Order = require('../models/order');
const Product = require('../models/product');
const Classifier = require('../models/classifier');

exports.fetch_all_classifiers = (req, res, next) => {
    Classifier.find({ 'userId': req.userData.userId })
        .select('_id name description parentDatasetId trainingData')
        // .populate('classifiers', '_id name description parentDatasetId trainingData')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                classifiers: docs.map(doc => {
                    return {
                        id: doc._id,
                            name: doc.name,
                            description: doc.description,
                            // nodes: classifier.nodes,
                            request: {
                                type: 'GET',
                                url: 'http://localhost:2000/datasets/'+doc.parentDatasetId+'/classifiers/' + doc._id //return list of classifiers
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

exports.fetch_all_trained_classifiers = (req, res, next) => {
    Classifier.find({ 
            'userId': req.userData.userId,
            'status': 3 
        })
        .select('_id name description parentDatasetId trainingData')
        // .populate('classifiers', '_id name description parentDatasetId trainingData')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                classifiers: docs.map(doc => {
                    return {
                        id: doc._id,
                            name: doc.name,
                            description: doc.description,
                            // nodes: classifier.nodes,
                            request: {
                                type: 'GET',
                                url: 'http://localhost:2000/datasets/'+doc.parentDatasetId+'/classifiers/' + doc._id //return list of classifiers
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