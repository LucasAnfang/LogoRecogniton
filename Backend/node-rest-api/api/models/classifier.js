const mongoose = require('mongoose');

const classifierSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    ownerId: { type: Number, required: true },
    description: { type: String, required: true },
    // trainingsSets: [ { type: mongoose.Schema.Types.ObjectId } ],
    subscriberIds: [ { type: mongoose.Schema.Types.ObjectId } ],
    isPublic: { type: Boolean, default: false },
    // index for tensorflow
    index: { type: mongoose.Schema.Types.ObjectId, required: true },
    nodes: [
        {
            name: { type: String, required: true },
            index: { type: Number, required: true }
        }
    ]
});

module.exports = mongoose.model('Classifier', classifierSchema);
