import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from src.storage_controller.NetworkedFileSystem.input_controller import InputController
from src.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from src.storage_controller.NetworkedFileSystem.nfs_controller_config import NFS_Controller_Config
from PIL import Image

STORAGE_ACCOUNT_NAME = 'logodetectiontesting'
STORAGE_ACCOUNT_KEY = 'HF0EwhCG2R8BBeKGV5qrloyz5Ua0kYQlSQI/vDWsTv3AjjK2nDJOD6Y8iLPjtF6nMnJr2zQZ0xhxkDF0biCArg=='
config = NFS_Controller_Config(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
ic = InputController(config)
test_upload = True
test_download = False

if test_upload:
    print 'extracting images'
    image_dir = '../test_images'
    image_1_path = '{}/{}'.format(image_dir,'Unknown-1.jpeg')
    image_2_path = '{}/{}'.format(image_dir,'Unknown.jpeg')
    image_1 = Image.open(image_1_path)
    image_2 = Image.open(image_2_path)

    classification_ipe = InstagramPostEntities(isClassification = True)
    classification_ipe.append({'picture' : image_1 , 'id' : image_1_path})
    classification_ipe.append({'picture' : image_2 , 'id' : image_2_path})
    print '{}:\n{}'.format('Classification', classification_ipe.posts)

    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, True)
    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, False)
    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, False)

    training_ipe = InstagramPostEntities(isTraining = True)
    training_ipe.archiveImageDirectory(image_dir)
    print '{}:\n{}'.format('Training', training_ipe.posts)

    ic.upload_brand_training_input_IPE('Audi', training_ipe, True)
    ic.upload_brand_training_input_IPE('Audi', training_ipe, False)
    ic.upload_brand_training_input_IPE('Audi', training_ipe, False)

# if test_download:
