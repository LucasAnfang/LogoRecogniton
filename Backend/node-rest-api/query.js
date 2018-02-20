const mongoose = require('mongoose');
const  program = require('commander');

const User = require('./api/models/user');
const Batch = require('./api/models/batch');
const Classifier = require('./api/models/classifier');

mongoose.connect(
    'mongodb://logo_detection_dev:' + 'RXR1Q4lJucDATFD7' + '@logo-detection-c0-shard-00-00-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-01-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-02-swlr9.mongodb.net:27017/test?ssl=true&replicaSet=logo-detection-c0-shard-0&authSource=admin'
);

// function range(val) {
//     return val.split('..').map(Number);
//   }
  
//   function list(val) {
//     return val.split(',');
//   }
  
//   function collect(val, memo) {
//     memo.push(val);
//     return memo;
//   }
  
//   function increaseVerbosity(v, total) {
//     return total + 1;
//   }
  
//   program
//     .version('0.1.0')
//     .usage('[options] <file ...>')
//     .option('-i, --integer <n>', 'An integer argument', parseInt)
//     .option('-f, --float <n>', 'A float argument', parseFloat)
//     .option('-r, --range <a>..<b>', 'A range', range)
//     .option('-l, --list <items>', 'A list', list)
//     .option('-o, --optional [value]', 'An optional value')
//     .option('-c, --collect [value]', 'A repeatable value', collect, [])
//     .option('-v, --verbose', 'A value that can be increased', increaseVerbosity, 0)
//     .parse(process.argv);
  
//   console.log(' int: %j', program.integer);
//   console.log(' float: %j', program.float);
//   console.log(' optional: %j', program.optional);
//   program.range = program.range || [];
//   console.log(' range: %j..%j', program.range[0], program.range[1]);
//   console.log(' list: %j', program.list);
//   console.log(' collect: %j', program.collect);
//   console.log(' verbosity: %j', program.verbose);
//   console.log(' args: %j', program.args);

  function list(val) {
    return val.split(',');
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

console.log(' model: %j', program.model);
console.log(' fields: %j', program.fields);

if(program.model === new RegExp('[uU]ser'))
/*
User.find()
    .select()
    .exec() //turn it into a real promise
    .then(docs => {
        console.log(docs);
        res.status(200).json({
            count: docs.length,
            orders: docs.map(doc => {
                return {
                    _id: doc._id,
                    name: doc.name,
                    email: doc.email,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:2000/users/' + doc._id
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
*/
// exit the process
process.exit();