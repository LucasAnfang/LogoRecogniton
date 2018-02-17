const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    // Call next if we auth with JWT and error if not (Protect routes to auth users)
    // If there is no token or it is invalid error is auth failed thrown 
    try { 
        const token = req.headers.authorization.split(' ')[1];
        console.log(token);
        const decoded = jwt.verify(token, process.env.JWT_KEY);
        req.userData = decoded;
        next();
    } catch (error) {
        return res.status(401).json({
            message: 'Auth failed'
        });
    }
};