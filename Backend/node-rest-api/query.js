const mongoose = require('mongoose');
const  program = require('commander');

const User = require('./api/models/user');
const Batch = require('./api/models/batch');
const Classifier = require('./api/models/classifier');

mongoose.connect(
    'mongodb://logo_detection_dev:' + 'RXR1Q4lJucDATFD7' + '@logo-detection-c0-shard-00-00-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-01-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-02-swlr9.mongodb.net:27017/test?ssl=true&replicaSet=logo-detection-c0-shard-0&authSource=admin'
);
mongoose.Promise = global.Promise;

function list(val) {
return val.replace(',', ' ');
}

program
  .version('0.1.0')
  .option('-m --model <model>', 'model', /^([uU]ser|[bB]atch|[cC]lassifier)$/i, '')
  .option('-f, --fields <fields>', 'A list of fields (comma delimited)', list)
  .parse(process.argv);
 
// validate the model exists
if (program.model === '') {
    console.error('no real model provided');
    process.exit(1);
}
var fields = (program.fields === undefined) ? '' : program.fields;

console.log(' model: %j', program.model);
console.log(' fields: %j', fields);

var model;
if(program.model.match(/[uU]ser/i)) {
    model = User;
}
else if(program.model.match(/[bB]atch/i)) {
    model = Batch;
}
else if(program.model.match(/[cC]lassifier/i)) {
    model = Classifier;
}

//mongoose get all docs
model.find(fields, function (err, results) {
    assert.equal(null, err);
    console.log(results);
});

// exit the process
process.exit();