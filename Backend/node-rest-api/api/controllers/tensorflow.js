const mongoose = require('mongoose');

const Classifier = require('../models/classifier');
const Dataset = require('../models/dataset');
const ImageObj = require('../models/image');

const fs = require('fs');
const path = require('path');

exports.fetch_checkpoint = (req, res, next) => {
    const testFolder = '././checkpoint';

    //send the checkpoint back
    fs.readdir(testFolder, (err, files) => {
        files.forEach(file => {
            console.log("file is: " + file);
            res.sendFile(file, {root: "././checkpoint/"});
        });
    })
}

exports.store_checkpoints = (req,res,next) => {
    console.log("in the function");
    const directory = '././checkpoint';
    const file = req.file;

    //in order to delete everything in the folder directory without deleting the actual folder 
    fs.readdir(directory, (err, files) => {
        if (err) throw err;

        for (const file of files) {
            fs.unlink(path.join(directory, file), err => {
            if (err) throw err;
            });
        }
    });
    const fileName = file.filename;
    console.log("fileName is: " + fileName);
    const oldPath = 'tmp_checkpoints/' + fileName;
    const newPath = 'checkpoint/' + fileName;

    //moves the file from tmp_checkpoints to checkpoint
    fs.rename(oldPath, newPath, (err) => {
        if (err) throw err;
    })

    //delete tmp checkpoint
    const tmpDirectory = '././tmp_checkpoints';
    fs.readdir(tmpDirectory, (err, files) => {
        if (err) throw err;

        for (const file of files) {
            if (file) {
                fs.unlink(path.join(tmpDirectory, file), err => {
                    if (err) throw err;
                });
            }

        }
    });


    //TODO: fix this to be a get request for the checkpoint
    res.status(200).json({
        message: "uploaded checkpoint is : " + req.file.filename
    });
}

// exports.fetch_checkpoint = (req, res, next) => {
    
// }

exports.fetch_training_batches_and_set = (req, res, next) => {
    // find all classifiers with status 1, ready to be trained
    // set all classifiers with status 1 to 2, processing
    Classifier.find(
        { status: 1 }
    )
    .exec()
    .then(results => {
        console.log(results);
        res.status(200).json({
            classifiers: results.map(doc => {
                return {
                    _id: doc._id,
                    name: doc.name, 
                    nodes: doc.nodes.map(node => {
                        return {
                            _id: node._id,
                            name: node.name,
                            trainingData: node.trainingData
                        }
                    })
                }
            })
        });
        results.forEach(item => {
            Classifier.update(
                {_id: item._id},
                { $set: {"status": 2 }}, 
                // { $set: {"status": 1 }}, // for testing purposes
                { safe: true, multi: true }
            ).exec();
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
}

exports.fetch_classify_batches_and_set = (req, res, next) => {
    Dataset.find(
        { status: 4 }
    )
    .select("_id classifiers images")
    .populate("images", "url")
    .exec()
    .then(results => {
        // ImageObj.find({"parentDatasetId": datasetId })
        //     .exec()
        //     .then(imgs => {
        //         resultsUrls = [];
        //         for(var img of imgs) {
        //             resultsUrls.push(img.url);                        
        //         }
        //         for (var i of imageUrls) {
        //             resultsUrls.push(i);
        //         }
        //         for (var r of result) {
        //             resultsUrls.push('http://localhost:2000/' + r);
        //         }
        //         res.status(200).json({
        //             message: "updated images",
        //             images: resultsUrls
        //         });
        //     });

        console.log(results);
        res.status(200).json({
            datasets: results.map(doc => {
                return {
                    _id: doc._id,
                    classifiers: doc.classifiers,
                    images: doc.images
                }
            })
        });
        results.forEach(item => {
            Dataset.update(
                {_id: item._id},
                { $set: {"status": 4 }}, 
                // { $set: {"status": 4 }}, // for testing purposes
                { safe: true, multi: true }
            ).exec();
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
}

exports.store_checkpoints = (req, res, next) => {}

exports.store_accuracy = (req, res, next) => {
    // ids = res.body.classifiers
    // Classifier.update(
        // { _id: { $in:  } },
        // { $set: { "accuracy" :  res.body.classifiers.accuracy} }
    //  )
    // .exec()
    // .then()
    // .catch();
}

exports.set_completed_classifier_statuses = (req, res, next) => {
    Classifier.find(
        {
            '_id': { $in: req.body.classifierIds}
        }
    )
    .exec()
    .then(results => {
        console.log(results);
        res.status(200).json({
            classifiers: results.map(doc => {
                return {
                    _id: doc._id,
                    name: doc.name, 
                    nodes: doc.nodes.map(node => {
                        return {
                            _id: node._id,
                            name: node.name,
                            trainingData: node.trainingData
                        }
                    })
                }
            })
        });
        results.forEach(item => {
            Classifier.update(
                {_id: item._id},
                { $set: {"status": 3 }},
                { safe: true, multi: true }
            ).exec();
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
}

exports.store_results = (req, res, next) => {
    req.body.imageObjs.forEach(img => {
        var tempResults = [];
        img.classifier_result.forEach(imgResult => {
            tempResults.push({
                values: imgResult.results,
                classifier: imgResult.classifier_name
            });
        });

        ImageObj.findOneAndUpdate(
            {"_id": img.imageId},
            {$push: {"results": tempResults}},
            {safe: true, new: true}
        )
        .exec()
        .then()
        .catch();

    });

    Dataset.findOneAndUpdate(
            { "_id": mongoose.Types.ObjectId(req.body.datasetId) }, 
            { "status": 6 }, 
            { safe: true, new: true }
        )
        .exec()
        .then(
            res.status(200).json({
                message: 'set dataset status to reflect image object',
                // createdDataset: {
                //     _id: result._id,
                //     name: result.name,
                //     datasetType: result.datasetType,
                //     request: {
                //         type: 'GET',
                //         url: 'http://localhost:2000/datasets/' + result._id
                //     }
                // }
            })
        )
        .catch();

    
        
        // for(res in img.classifier_result) {
        //     // console.log(res);
        //     results.append({
        //         values: res.results,
        //         classifier: res.classifier_name
        //     })
        // }

        // console.log(results)
        /*
            Dataset.findOneAndUpdate(
        { "_id": mongoose.Types.ObjectId(datasetId) }, 
        { $push: {"classifiers": req.body.classifierIds}}, 
        { safe: true, new: true }
        )
        */
        // ImageObj.findOneAndUpdate(
        //     {"_id": img.imageId},
        //     {$push: {"results": results}},
        //     {safe: true, new: true}
        // )
    // }
    
}

