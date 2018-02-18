var PythonShell = require('python-shell');

var options = {
    // mode: 'text',
    // pythonPath: 'path/to/python',
    // pythonOptions: ['-u'], // get print results in real-time
    scriptPath: './api/iron_python',
    args: ['hello', 'world'] // args: ['--buoy', '46232'] for when we want to add arges with flags
};
options.args = ['hello', 'world']


PythonShell.run('echo_args.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
});

// Original call: IGScraperTool.py -t patagonia -m 10
options.scriptPath = './api/iron_python/instagram_scraper';
options.args = ['-t', 'patagonia', '-m', '500'];
PythonShell.run('IGScraperTool.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
});