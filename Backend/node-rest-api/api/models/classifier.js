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
    // status: 
    // 0 = created
    // 1 = ready to be trained
    // 2 = training
    // 3 = finished training
    // 4 = ready to be classified
    // 5 = classifying
    // 6 = finished classifying
    status: { type: Number, default: 0 },
    nodes: [
        {
            _id: mongoose.Schema.Types.ObjectId,
            name: { type: String, required: true },
            // index: { type: Number, required: true },
            trainingData: [ { 
                type: String, 
                required: true }
             ]
        }
    ]
});

module.exports = mongoose.model('Classifier', classifierSchema);
