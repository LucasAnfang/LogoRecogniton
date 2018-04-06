const mongoose = require('mongoose');

const Classifier = require('../models/classifier');

exports.fetch_new_batches_and_set = (req, res, next) => {
    // find all classifiers with status 1, ready to be trained
    // set all classifiers with status 1 to 2, processing
    Classifier.find(
        { status: 1 }
    )
    .exec()
    .then(results => {
        console.log(results);
        res.status(200).json({
            classifiers: results.map(doc => {
                return {
                    _id: doc._id,
                    name: doc.name, 
                    nodes: doc.nodes.map(node => {
                        return {
                            _id: node._id,
                            name: node.name,
                            trainingData: node.trainingData
                        }
                    })
                }
            })
        });
        results.forEach(item => {
            Classifier.update(
                {_id: item._id},
                // { $set: {"status": 2 }}, 
                { $set: {"status": 1 }}, // for testing purposes
                { safe: true, multi: true }
            ).exec();
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
}

exports.store_results = (req, res, next) => {
}

exports.store_checkpoints = (req, res, next) => {
}