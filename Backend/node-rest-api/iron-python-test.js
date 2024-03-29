var PythonShell = require('python-shell');
const uid = require('uid'); 
const fs = require('fs');

var hashtagScrapeResult = {};

var hashtag = 'patagonia';
hashtagScrapeResult.hashtag = hashtag;
image_count = 100;
var outputImageDirectory = './datasets/' + uid() + '/';
var options = {
    scriptPath: './api/iron_python/instagram_scraper',
    args: ['-hi', hashtag, '-d', outputImageDirectory, '-m', image_count]
};

PythonShell.run('IGScraperTool.py', options, function (err, results) {
    if (err) throw err;
    // console.log('results: %j', results);
    outputImageDirectory = outputImageDirectory + hashtag + '/';
    var files = fs.readdirSync(outputImageDirectory);
    fullFilenames = files.map(filename => outputImageDirectory + filename);
    hashtagScrapeResult.fullPaths = fullFilenames;
    console.log(hashtagScrapeResult);
});



// var options = {
//     // mode: 'text',
//     // pythonPath: 'path/to/python',
//     // pythonOptions: ['-u'], // get print results in real-time
//     scriptPath: './api/iron_python',
//     args: ['hello', 'world'] // args: ['--buoy', '46232'] for when we want to add arges with flags
// };
// options.args = ['hello', 'world']


// PythonShell.run('echo_args.py', options, function (err, results) {
//     if (err) throw err;
//     // results is an array consisting of messages collected during execution
//     console.log('results: %j', results);
// });