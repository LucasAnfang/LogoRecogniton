const mongoose = require('mongoose');

const Classifier = require('../models/classifier');

exports.fetch_all_batches = (req, res, next) => {
    Classifier.find({processed: false})
    .exec()
    .then(results => {
        console.log(results);
    });
}