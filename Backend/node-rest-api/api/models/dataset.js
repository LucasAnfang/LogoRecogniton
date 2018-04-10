const mongoose = require('mongoose');

const datasetSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    name: { type: String, required: true },
    userId: {  type: String, required: true },
    isProcessed: { type: Boolean, default: false },
    classifiers: [ {type: mongoose.Schema.Types.ObjectId, ref: 'Classifiers'} ],
    uploadRequest: { 
        configuration: {
            // classifiers: [ {type: mongoose.Schema.Types.ObjectId, ref: 'Dataset'} ]
        },
        uploadTimestamp: {  type : Date, default: Date.now },
    },
    completionTimestamp: {type: Date, default: Date.now },
    // images: [{ type: String, required: true }],
    // training/ops
    datasetType: { type: Number, required: true },
    images: [
        { type: mongoose.Schema.Types.ObjectId, ref: 'ImageObj'}
    ],
    // status: 
    // 0 = created
    // 1 = ready to be trained
    // 2 = training
    // 3 = finished training
    // 4 = ready to be classified
    // 5 = classifying
    // 6 = finished classifying
    status: { type: Number, default: 0 }
});

module.exports = mongoose.model('Dataset', datasetSchema);