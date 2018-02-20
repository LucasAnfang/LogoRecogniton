const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const productRoutes = require('./api/routes/products');
const ordersRoutes = require('./api/routes/orders');
const userRoutes = require('./api/routes/users');
const classifierRoutes = require('./api/routes/classifiers');
const batchRoutes = require('./api/routes/batches');
const serviceRoutes = require('./api/routes/services');

mongoose.connect(
    'mongodb://logo_detection_dev:' + process.env.MONGO_ATLAS_PW + '@logo-detection-c0-shard-00-00-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-01-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-02-swlr9.mongodb.net:27017/test?ssl=true&replicaSet=logo-detection-c0-shard-0&authSource=admin'
);

mongoose.Promise = global.Promise;

app.use(morgan('dev'));
// make the upload url available
app.use('/uploads', express.static('uploads'))
app.use('/uploads', express.static('images'))
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
app.use('/batches', batchRoutes);
app.use('/services', serviceRoutes);

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