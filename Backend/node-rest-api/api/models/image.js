const mongoose = require('mongoose');

const imageSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    userId: { type: mongoose.Schema.Types.ObjectId, required: true },
    parentDatasetId: {type: mongoose.Schema.Types.ObjectId, required: true, ref: 'Dataset'},
    url: { type: String, required: true },
    results: [{ type: String, required: true}]
});

module.exports = mongoose.model('ImageObj', imageSchema);