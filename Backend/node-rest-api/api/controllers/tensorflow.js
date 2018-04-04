const mongoose = require('mongoose');

const Classifier = require('../models/classifier');
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
exports.fetch_new_batches_and_set = (req, res, next) => {
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
                { safe: true, multi: true }
            ).exec();
        });
    })
    .catch(err => {
        res.status(500).json({
            err: err
        });
    });
    // Classifier.update( 
    //     { status: 2 }, 
    //     { $set: { status: 1 } },
    //     { safe: true, multi: true }
    // )
    // .exec()
    // .then(results => {
    //     console.log(results);
    //     res.status(200).json({
    //         results: results
    //     });
    // })
    // .catch(err => {
    //     res.status(500).json({
    //         err: err
    //     });
    // });
}