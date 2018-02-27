const mongoose = require('mongoose');
const PythonShell = require('python-shell');
const uid = require('uid'); 
const fs = require('fs');

exports.fetch_images_with_hashtag = (req, res, next) => {
    try {
        console.log(req.body)
        var hashtag = req.body.hashtag;
        var outputImageDirectory = './images/' + uid() + '/';
        var options = {
            scriptPath: './api/iron_python/instagram_scraper',
            args: ['-hi', hashtag, '-d', outputImageDirectory, '-m', req.body.image_count]
        };
        PythonShell.run('IGScraperTool.py', options, function (err, results) {
            if (err) throw err;
            console.log('results: %j', results);
            outputImageDirectory = outputImageDirectory + hashtag + '/';
            outputImageDirectory = outputImageDirectory.substring(2);
            var files = fs.readdirSync(outputImageDirectory);
            fullFilenames = files.map(filename => 'http://localhost:2000/' + outputImageDirectory + filename);
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