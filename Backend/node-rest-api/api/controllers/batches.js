const mongoose = require('mongoose');

const Order = require('../models/order');
const Product = require('../models/product');
const Batch = require('../models/batch');
// const batchSchema = mongoose.Schema({
//     _id: mongoose.Schema.Types.ObjectId,
//     isProcessed: { type: Boolean, default: false },
//     uploadRequest: { 
//         userID: {  type: mongoose.Schema.Types.ObjectId, required: true },
//         configuration: {
//             classifiers: [
//                 {type: mongoose.Schema.Types.ObjectId, ref: 'Classifier'}
//             ]
//         },
//         uploadTimestamp: {  type : Date, default: Date.now },
//     },
//     completionTimestamp: {type: Date, default: Date.now },
//     data: [{ rowId: mongoose.Schema.Types.ObjectId}],
//     // training/ops
//     batchType: {type: Number, required: true}
// });


exports.fetch_all_batches = (req, res, next) => {
    Batches.find()
        //mayhaps remove data
        .select('_id isProcessed uploadRequest completionTimestamp data batchType')
        .populate('uploadRequest', 'data')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                classifiers: docs.map(doc => {
                    return {
                        _id: doc._id,
                        isProcessed: doc.isProcessed,
                        uploadRequest: doc.uploadRequest,
                        completionTimestamp: doc.completionTimestamp,
                        data: doc.data,
                        batchType: doc.batchType,
                        request: {
                            type: 'GET',
                            url: 'http://localhost:3000/batches/' + doc._id
                        }
                    };
                })
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({
                error: err
            });
        });
}

exports.create_batch = (req, res, next) => {
    const batch = new Batch({
        _id: new mongoose.Types.ObjectId(),
        //what goes in here
        uploadRequest: {

        },
        //what goes in here x2
        data: {

        },
        batchType: req.body.batchType
    });
    batch.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /batches',
                createdBatch: {
                    name: result.name,
                    _id: result._id,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:3000/batches/' + result._id
                    }
                }
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.fetch_batch = (req, res, next) => {
    const id = req.params.orderId;
    Batch.findById(id)
        //maybe remove data
        .select('_id isProcessed uploadRequest completionTimestamp data batchType')
        .populate('uploadRequest', 'data')
        .exec()
        .then(batch => {
            if (batch) {
                res.status(200).json({
                    batch: batch,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:3000/batches/' + batch._id

                    }
                });
            } else {
                res.status(404).json({message: 'No valid batch found for provided ID'})
            }
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.delete_batch = (req, res, next) => {
    const id = req.params.batchId;
    Order.remove({ _id: id })
        .exec()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Batch deleted',
                request: {
                    type: 'POST',
                    url: 'http://localhost:3000/batches/',
                    body: { productId: 'ID' }
                }
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}