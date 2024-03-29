const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const productRoutes = require('./api/routes/products');
const ordersRoutes = require('./api/routes/orders');
const userRoutes = require('./api/routes/users');
const classifierRoutes = require('./api/routes/classifiers');
const datasetRoutes = require('./api/routes/datasets');
const scraperRoutes = require('./api/routes/scraper');
const tensorflowRoutes = require('./api/routes/tensorflow');

mongoose.connect(
    'mongodb://logo_detection_dev:' + process.env.MONGO_ATLAS_PW + '@logo-detection-c0-shard-00-00-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-01-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-02-swlr9.mongodb.net:27017/LogoDetection?ssl=true&replicaSet=logo-detection-c0-shard-0&authSource=admin'
);

mongoose.Promise = global.Promise;

app.use(morgan('dev'));
// make the upload url available
app.use('/uploads', express.static('uploads'));
app.use('/images', express.static('images'));
app.use('/datasets', express.static('datasets'));
app.use('/assets', express.static('assets'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Avoid CORS errors
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header( 
        'Access-Control-Allow-Headers',  
        'Origin, X-Requested-With, Content-Type, Accept, Authorization' 
    );
    if(req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Methods', 'PUT, POST, PATCH, DELETE, GET')
        return res.status(200).json({});
    }
    next();
});

// routes that handle requests
app.use('/products', productRoutes);
app.use('/orders', ordersRoutes);
app.use('/users', userRoutes);
app.use('/classifiers', classifierRoutes);
app.use('/datasets', datasetRoutes);
app.use('/scraper', scraperRoutes);
app.use('/tensorflow', tensorflowRoutes)

app.use((req, res, next) => {
    const error = new Error('Not found');
    error.status = 404;
    next(error);
});

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
        error: {
            message: error.message
        }
    })
});

module.exports = app;