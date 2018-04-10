import configparser
import requests
import os

class RestController:
    def __init__(self, config):
        self.config = config

    # GET training images
    def get_training_images(self):
        headers = {"Authorization": self.config['Auth']['JWT']}
        res = requests.get(self.config['Routes']['Training'], headers=headers)
        if res.status_code == requests.codes.ok:
            print("Retrieved training images from REST API...")
        else:
            print("Error retrieving training images from REST API")
        return res

    # POST training results


    # GET tensorflow checkpoint
    def get_checkpoint(self):
        headers = {"Authorization": auth['JWT']}
        res = requests.get(routes['Checkpoint'], headers=headers)

        if res.status_code == requests.codes.ok:
            print("Retrieved checkpoint from Rest API")
            
    # POST tensorflow checkpoint


    # GET operations data

    # POST operations results

def main():
    RestController().get_training_images()

if __name__ == "__main__":
    main()
