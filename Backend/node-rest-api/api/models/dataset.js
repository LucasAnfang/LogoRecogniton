const mongoose = require('mongoose');

const datasetSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    isProcessed: { type: Boolean, default: false },
    uploadRequest: { 
        // userID: {  type: mongoose.Schema.Types.ObjectId, required: true },
        configuration: {
            classifiers: [ {type: mongoose.Schema.Types.ObjectId, ref: 'Dataset'} ]
        },
        uploadTimestamp: {  type : Date, default: Date.now },
    },
    completionTimestamp: {type: Date, default: Date.now },
    data: [{ rowId: mongoose.Schema.Types.ObjectId}],
    // training/ops
    datasetType: {type: Number, required: true}
});

module.exports = mongoose.model('Dataset', datasetSchema);