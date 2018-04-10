import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
import storage.rest_controller as RestController
import preprocessing.image_controller as ImageController

class ProcessController:
    def __init__(self):
        # initialize the configuration file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        print("Initializing Rest Controller...")
        self.restcontroller = RestController.RestController(self.config)
        print("Initializing Image Controller...")
        self.imagecontroller = ImageController.ImageController(self.config)
        print("Initializing Tensorflow Controller...")
        pass

    def prepare_training(self):
        res = self.restcontroller.get_training_images()
        tfrecord = self.imagecontroller.prepare_training(res, 'storage/tfrecords')

def main():
    # initialize the processing Controller
    process = ProcessController()
    process.prepare_training()
    pass

if __name__ == '__main__':
    sys.exit(main())
