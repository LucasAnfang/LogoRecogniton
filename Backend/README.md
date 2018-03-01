# Backend 

Setup
##
Logo detection REST API using Node.js and mongo

Pull this project and 'npm install' on your machine (in the Backend/node-rest-api folder) to finish setup if you want to work on the rest api component.

Image processing is done un the python section (in py) 

Tutorial link: https://www.youtube.com/watch?v=0oXYLzuucwE&t=7s

Instagram Scraper requirements setup
##
In order to use the instagram scraper, you must install the dependencies. This can be done on a virtual env with the following comands.

// install a virtualenv inside the backend folder
pip install virtualenv
cd Backend
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate
pip install -r py/src/requirements.txt
 
Server startup
##
To start the node server, enter the Backend/node-rest-api folder and type:
npm start


##
To set up MongoDB Compass (database GUI), copy this string to your clipboard and then open the application. It will populate all information automatically.

```mongodb://logo_detection_dev:RXR1Q4lJucDATFD7@logo-detection-c0-shard-00-00-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-01-swlr9.mongodb.net:27017,logo-detection-c0-shard-00-02-swlr9.mongodb.net:27017/test?ssl=true&replicaSet=logo-detection-c0-shard-0&authSource=admin"```
