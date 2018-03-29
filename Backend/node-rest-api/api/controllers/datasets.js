const mongoose = require('mongoose');
const multer = require('multer');
var PythonShell = require('python-shell');

const fs = require('fs-extra');
const uid = require('uid');
const isImage = require('is-image');


const Order = require('../models/order');
const Product = require('../models/product');
const Dataset = require('../models/dataset');
const Classifier = require('../models/classifier');

// code from https://stackoverflow.com/questions/41462606/get-all-files-recursively-in-directories-nodejs
function traverseDirectory(dirname, callback) {
    var directory = [];
    var output = [];
    fs.readdir(dirname, function(err, list) {
        // dirname = fs.realpathSync(dirname);
        // console.log('dirname: ' + dirname);
        if (err) {
            return callback(err);
        }
        var listlength = list.length;
        list.forEach(function(file) {
            outputname = file;
            // console.log(outputname);
            // console.log("outputname is: " + outputname);
            file = dirname + file;
            // console.log("file is: " + file);
            fs.stat(file, function(err, stat) {
                if (isImage(file)) {
                    directory.push(file);
                } else {
                    file = file + "/";
                }
                output.push(outputname);
                if (stat && stat.isDirectory()) {
                    traverseDirectory(file, function(err, parsed) {
                        directory = directory.concat(parsed);
                        if (!--listlength) {
                            callback(null, directory);
                        }
                    });
                } else {
                    if (!--listlength) {
                        callback(null, directory);
                    }
                }
            });
        });
    });
}

// delete files in folder
var deleteFolderRecursive = function(path) {
    if (fs.existsSync(path)) {
      fs.readdirSync(path).forEach(function(file, index){
        var curPath = path + "/" + file;
        if (fs.lstatSync(curPath).isDirectory()) { // recurse
          deleteFolderRecursive(curPath);
        } else { // delete file
          fs.unlinkSync(curPath);
        }
      });
      fs.rmdirSync(path);
    }
  };

exports.fetch_all_datasets = (req, res, next) => {
    // console.log(req.userData.userId);
    Dataset.find({
        'userId': req.userData.userId
    })
        .select('_id name')
        .exec() //turn it into a real promise
        .then(docs => {
            console.log(docs);
            res.status(200).json({
                count: docs.length,
                datasets: docs.map(doc => {
                    return {
                        _id: doc._id,
                        name: doc.name,
                        cover: 'http://localhost:2000/' + 'assets/noimages.png',
                        // isProcessed: doc.isProcessed,
                        // uploadRequest: doc.uploadRequest,
                        // completionTimestamp: doc.completionTimestamp,
                        // data: doc.data,
                        // datasetType: doc.datasetType,
                        request: {
                            type: 'GET',
                            url: 'http://localhost:2000/datasets/' + doc._id
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

exports.upload_images;// = multer() => {

//}
// (req, res, next) => {
//     console.log(req.params.datasetId);
// }

exports.scrape_images = (req, res, next) => {
    const id = req.params.datasetId;
    Dataset.findById(id)
    .select('userId')
    .exec()
    .then(dataset => {
        if (!dataset) {
            res.status(400).json({
                error: 'dataset doesn\'t exist'
            });
        } else if (dataset.userId != req.userData.userId) {
            res.status(400).json({
                error: 'dataset doesn\'t belong to user'
            });
        } else {
            try {
                var hashtag = req.body.hashtag;
                var uid = req.userData.userId;
                var d_id = req.params.datasetId;
                var image_count = req.body.image_count;
                if (req.body.image_count == null) {
                    image_count = 15;
                }
                var hashtagScrapeResult = {};
        
                hashtagScrapeResult.hashtag = hashtag;
                var responseImageDirectory = 'datasets/' + d_id + '/' + hashtag +'/';
                var outputImageDirectory = 'datasets/' + d_id + '/';
                var options = {
                    scriptPath: './api/iron_python/instagram_scraper',
                    args: ['-hi', hashtag, '-d', outputImageDirectory, '-m', image_count]
                };
                PythonShell.run('IGScraperTool.py', options, function (err, results) {
                    if (err) {
                        console.log(err);
                        res.status(500).json({
                            error: err
                        });
                    }
                    var files = fs.readdirSync(responseImageDirectory);
                    fullFilenames = files.map(filename => 'http://localhost:2000/' + responseImageDirectory + filename);
                    res.status(201).json({
                        hashtag: hashtag,
                        filePaths: fullFilenames
                    });
                });
            }
            catch(err) {
                console.log(err);
                res.status(500).json({
                    error: err
                });
            }
        }
    });
}

exports.create_dataset = (req, res, next) => {
    const dataset = new Dataset({
        _id: new mongoose.Types.ObjectId(),
        name: req.body.name,
        userId: req.userData.userId,
        uploadRequest: {},
        data: {},
        datasetType: req.body.datasetType
    });
    dataset.save()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Handling POST request to /datasets',
                createdDataset: {
                    _id: result._id,
                    name: result.name,
                    datasetType: result.datasetType,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/datasets/' + result._id
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

exports.fetch_dataset = (req, res, next) => {
    var coverImage;
    console.log(req.userData.userId);
    const id = req.params.datasetId;
    Dataset.findById(id)
        .select('_id userId name isProcessed classifiers datasetType')
        // .populate('uploadRequest', 'data')
        .exec()
        .then(dataset => {
            if (!dataset) {
                res.status(404).json({message: 'No valid dataset found for provided ID'})
            } else if (dataset.userId != req.userData.userId) {
                res.status(404).json({message: 'Dataset doesn\'t belong to user'})
            } else {
                const folder = 'datasets/' + req.params.datasetId + '/'; //+ req.params.datasetId + '/';
                traverseDirectory(folder, function(err, result) {
                    console.log("traverseDirectory result is: " + result);
                    if (err) {
                        console.log(err);
                        res.status(300).json({message: 'Dataset is empty'})
                    }
                    else if (result.length != 0) {
                        coverImage = 'http://localhost:2000/' + result[0];
                        res.status(200).json({
                            dataset: dataset,
                            cover: coverImage,
                            images: result,
                            request: {
                                type: 'GET',
                                url: 'http://localhost:2000/datasets/' + dataset._id
                            }
                        });
                    } else {
                        coverImage = 'http://localhost:2000/' + 'assets/noimages.png';
                        res.status(200).json({
                            dataset: dataset,
                            cover: coverImage,
                            images: result,
                            request: {
                                type: 'GET',
                                url: 'http://localhost:2000/datasets/' + dataset._id
                            }
                        });
                    }
                    // console.log(result);
                });
            }
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({ 
                error: err 
            });
        });
}

exports.delete_dataset = (req, res, next) => {
    var id = req.params.datasetId;
    var uid = req.userData.userId;

    if (!mongoose.Types.ObjectId.isValid(id)) {
        res.status(400).json({ 
            error: "DatasetID is not a valid ID"
        });
    }
    else {
        deleteFolderRecursive('datasets/'+id);
        
        Dataset.findOne({ _id: id}, function (err, docs){
            // need to fix error codes
            
            if (docs) {
                if (docs.userId != uid) {
                    res.status(400).json({ 
                        error: "Dataset doesn't belong to user"
                    });
                } else {
                    deleteFolderRecursive('datasets/'+id);
                    Dataset.remove({ _id: id, userId: uid })
                        .exec()
                        .then(result => {
                            res.status(200).json({
                                message: 'Dataset Deleted',
                                request: {
                                    type: 'POST',
                                    url: 'http://localhost:2000/datasets'
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
            } else {
                res.status(400).json({ 
                    error: "Dataset doesn't exist"
                });
                deleteFolderRecursive('datasets/'+id);
            }
        }); 
    }
}



// classifiers
exports.create_classifier = (req, res, next) => {

    const datasetId = req.params.datasetId;
    console.log(datasetId);
    Dataset.findById(datasetId)
        .select('_id userId classifiers')
        .exec()
        .then(dataset => {
            if (!dataset) {
                return res.status(404).json({message: 'No dataset found for provided ID'})
            } else if (dataset.userId != req.userData.userId) {
                return res.status(404).json({message: 'Dataset doesn\'t belong to user'})
            } else {
                const classifier = new Classifier({
                    _id: new mongoose.Types.ObjectId(),
                    name: req.body.name,
                    userId: req.userData.userId,
                    parentDatasetId: datasetId,
                    description: req.body.description,
                    // need to figure out how to get these two automatically
                    classifierIndex: '0',
                    nodes: []
                });

                classifier.save()
                    .then(result => {
                        console.log("adding to the dataset");
                        dataset.classifiers.push(classifier._id);
                        dataset.save();
                        console.log("size is " , dataset.classifiers.length)

                        console.log(result);
                        console.log("name is ", result.name);
                        return res.status(200).json({
                            message: 'Handling POST request to /datasets/' + req.params.datasetId + '/classifiers',
                            createdClassifier: 
                            {
                                classifierId: result._id,
                                name: result.name,
                                description: result.description,
                                userId: result.userId,
                                isPublic: result.isPublic,
                                parentDatasetId: result.parentDatasetId,
                                request: {
                                    type: 'GET',
                                    url: 'http://localhost:2000/datasets/'+ result.parentDatasetId+'classifiers/' + result._id
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
        });
}

exports.fetch_dataset_classifiers = (req, res, next) => {
    const datasetId = req.params.datasetId;
    console.log("datasetId is ", datasetId);

    Classifier.find({
        'parentDatasetId': req.params.datasetId
   })
        .populate('classifiers', '_id name description parentDatasetId trainingData')
        .exec()
        .then(results => {
            if (results) {
                res.status(200).json({
                    count: results.length,
                    classifier: results.map(doc => {
                        return {
                            id: doc._id,
                            name: doc.name,
                            description: doc.description,
                            // nodes: classifier.nodes,
                            request: {
                                type: 'GET',
                                url: 'http://localhost:2000/datasets/'+doc.parentDatasetId+'/classifiers/' + doc._id //return list of classifiers
                                //url: 'http://localhost:3000/products/' + order.product //return information on ordered product
                            }
                        }
                    })
                });
            } else {
                res.status(404).json({message: 'No valid entry found for provided ID'})
            }
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
}

exports.fetch_classifier = (req, res, next) => {
    const classifierId = req.params.classifierId;
    console.log("classifierId is ", classifierId);
        Classifier.findById(classifierId)
        .select('_id, name description')
        .exec()
        .then(doc => {
            if (doc) {
                res.status(200).json({
                            id: doc._id,
                            name: doc.name,
                            description: doc.description,
                            // nodes: classifier.nodes,
                });
            } else {
                res.status(404).json({message: 'No valid classifier found for provided ID'})
            }
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
}

exports.update_classifier = (req, res, next) => {
    const classifierId = req.params.classifierId;
    // const classifier = Classifier.findById(classifierId);
    // const parent = classifier.parentDatasetId;
    const updateOps = {};
    for (const ops of Array.from(req.body)) {
        updateOps[ops.propName] = ops.value;
    }
    Classifier.update({ _id: classifierId }, { $set: updateOps}) 
        .exec()
        .then(result => {
            console.log(result);
            res.status(200).json({
                message: 'Classifier updated',
                request: {
                    type: 'GET',
                    // url: 'http://localhost:3000/datasets/' + parentDatasetId + '/classifiers/' + classifierId
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

exports.delete_classifier = (req, res, next) => {
    var id = req.params.classifierId;
    var uid = req.userData.userId;

    if (!mongoose.Types.ObjectId.isValid(id)) {
        res.status(400).json({ 
            error: "Classifier ID is not a valid ID"
        });
    }
    else {
        
        Classifier.findOne({ _id: id}, function (err, docs){
            // need to fix error codes
            if (docs) {
                if (docs.userId != uid) {
                    res.status(400).json({ 
                        error: "Classifier doesn't belong to user"
                    });
                } else {
                    Classifier.remove({ _id: id, userId: uid })
                        .exec()
                        .then(result => {
                            res.status(200).json({
                                message: 'Classifier Deleted',
                                request: {
                                    type: 'POST',
                                    url: 'http://localhost:2000/datasets'
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
            } else {
                res.status(400).json({ 
                    error: "Classifier doesn't exist"
                });
            }
        }); 
    }
}
