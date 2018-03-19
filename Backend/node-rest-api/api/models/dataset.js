const mongoose = require('mongoose');

const datasetSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    name: { type: String, required: true },
    userId: {  type: String, required: true },
    isProcessed: { type: Boolean, default: false },
    classifiers: [ {type: mongoose.Schema.Types.ObjectId, ref: 'Dataset'} ],
    uploadRequest: { 
        configuration: {
            // classifiers: [ {type: mongoose.Schema.Types.ObjectId, ref: 'Dataset'} ]
        },
        uploadTimestamp: {  type : Date, default: Date.now },
    },
    completionTimestamp: {type: Date, default: Date.now },
    // images: [{ type: String, required: true }],
    // training/ops
    datasetType: { type: Number, required: true }
});

module.exports = mongoose.model('Dataset', datasetSchema);