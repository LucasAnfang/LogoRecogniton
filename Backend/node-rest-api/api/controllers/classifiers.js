const mongoose = require('mongoose');

const Order = require('../models/order');
const Product = require('../models/product');
const Classifier = require('../models/classifier');
// _id: mongoose.Schema.Types.ObjectId,
//     ownerId: { type: Number, required: true },
//     description: { type: String, required: true },
//     trainingsSets: [ { type: mongoose.Schema.Types.ObjectId } ],
//     subscriberIds: [ { type: mongoose.Schema.Types.ObjectId } ],
//     isPublic: { type: Boolean, default: false, required: true },
//     // index for tensorflow
//     index: { type: mongoose.Schema.Types.ObjectId, required: true },
//     nodes: [
//         {
//             name: { type: String, required: true },
//             index: { type: Number, required: true }
//         }
//     ]

exports.fetch_all_classifiers = (req, res, next) => {
    Classifier.find()
        .select('_id ownerId description trainingSets subscriberIds isPublic index nodes')
        .populate('nodes', 'name index')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                classifiers: docs.map(doc => {
                    return {
                        _id: doc._id,
                        ownerId: doc.ownerId,
                        description: doc.description,
                        trainingsSets: doc.trainingsSets,
                        subscriberIds: doc.subscriberIds,
                        // index for tensorflow
                        index: doc.index,
                        nodes: doc.nodes,
                        request: {
                            type: 'GET',
                            url: 'http://localhost:3000/classifiers/' + doc._id
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

exports.create_classifier = (req, res, next) => {
    const classifier = new Classifier({
        _id: new mongoose.Types.ObjectId(),
        name: req.body.name,
        price: req.body.price,
        productImage: req.file.path
    });
    classifier.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /classifiers',
                createdProduct: {
                    name: result.name,
                    price: result.price,
                    _id: result._id,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:3000/products/' + result._id
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

exports.fetch_classifier = (req, res, next) => {
    const id = req.params.orderId;
    Order.findById(id)
        .select('product _id quantity')
        .populate('product', 'price name _id')
        .exec()
        .then(order => {
            if (order) {
                res.status(200).json({
                    order: order,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:3000/orders/' //return list of orders
                        //url: 'http://localhost:3000/products/' + order.product //return information on ordered product
                    }
                });
            } else {
                res.status(404).json({message: 'No valid entry found for provided ID'})
            }
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.delete_classifier = (req, res, next) => {
    const id = req.params.orderId;
    Order.remove({ _id: id })
        .exec()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Order deleted',
                request: {
                    type: 'POST',
                    url: 'http://localhost:3000/orders/',
                    body: { productId: 'ID', quantity: 'Number' }
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