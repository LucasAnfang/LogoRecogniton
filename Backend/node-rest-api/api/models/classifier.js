const mongoose = require('mongoose');

const classifierSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    userId: { type: mongoose.Schema.Types.ObjectId, required: true },
    parentDatasetId: {type: mongoose.Schema.Types.ObjectId, required: true},
    name: { type: String, required: true },
    description: { type: String, required: true },
    // subscriberIds: [ { type: mongoose.Schema.Types.ObjectId } ],
    isPublic: { type: Boolean, default: false },
    // index for tensorflow
    classifierIndex: { type: String, required: true },
    nodes: [
        {
            _id: mongoose.Schema.Types.ObjectId,
            name: { type: String, required: true },
            // index: { type: Number, required: true },
            trainingData: [ { type: String, required: true } ]
        }
    ]
});

module.exports = mongoose.model('Classifier', classifierSchema);
