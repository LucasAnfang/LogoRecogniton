const mongoose = require('mongoose');
const PythonShell = require('python-shell');
const uid = require('uid'); 
const fs = require('fs');

exports.fetch_images_with_hashtags = (req, res, next) => {

    for(const hashtag in req.params.hashtags) {
        var outputImageDirectory = '../../images/' + uid() + '/';
        var options = {
            scriptPath: '../iron_python/instagram_scraper',
            args: ['-t', hashtag, '-d', outputImageDirectory, '-m', req.params.image_count]
        };
        
        PythonShell.run('IGScraperTool.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            console.log('results: %j', results);
        });
        const fs = require('fs');

        fs.readdir(testFolder, (err, files) => {
            files.forEach(file => {
                console.log(file);
            });
        });
    }
}