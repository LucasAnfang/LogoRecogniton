const mongoose = require('mongoose');

const batchSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    isProcessed: { type: Boolean, default: false },
    uploadRequest: { 
        userID: {  type: mongoose.Schema.Types.ObjectId, required: true },
        configuration: {
            classifiers: [
                {type: mongoose.Schema.Types.ObjectId, ref: 'Classifier'}
            ]
        },
        uploadTimestamp: {  type : Date, default: Date.now },
    },
    completionTimestamp: {type: Date, default: Date.now },
    data: [{ rowId: mongoose.Schema.Types.ObjectId}],
    // training/ops
    batchType: {type: Number, required: true}
});

module.exports = mongoose.model('Classifier', batchSchema);