const mongoose = require('mongoose');

const Classifier = require('../models/classifier');

exports.fetch_new_batches = (req, res, next) => {
    // find all classifiers with status 1, ready to be trained
    // set all classifiers with status 1 to 2, processing
    Classifier.find({ status: 1 })
    .exec()
    .then(results => {
        console.log(results);
        res.status(200).json({
            results: results
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
}