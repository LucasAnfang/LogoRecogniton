import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from src.storage_controller.NetworkedFileSystem.input_controller import InputController
from src.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from src.storage_controller.NetworkedFileSystem.nfs_controller_config import NFS_Controller_Config
from src.storage_controller.TableManagers.table_manager import TableStorageConnector
from PIL import Image

ACTIVE_STORAGE_ACCOUNT_NAME = 'logodetectionstorage'
ACTIVE_STORAGE_ACCOUNT_KEY = 'jPJyzct+8WD1lKU5M+ZwDflWUGRu+YBpH8n/3Z6qR7WD7uc3HV2U1rtiQKesLRq2tU3jtXIe26RklAYdKzoydA=='
TEST_STORAGE_ACCOUNT_NAME = 'logodetectiontesting'
TEST_STORAGE_ACCOUNT_KEY = 'HF0EwhCG2R8BBeKGV5qrloyz5Ua0kYQlSQI/vDWsTv3AjjK2nDJOD6Y8iLPjtF6nMnJr2zQZ0xhxkDF0biCArg=='
config = NFS_Controller_Config(ACTIVE_STORAGE_ACCOUNT_NAME, ACTIVE_STORAGE_ACCOUNT_KEY)

ic = InputController(config)
table_manager = TableStorageConnector(config)

brands = ic.get_container_directories()

ipe.archiveImageDirectoryPaths(directory, has_logo = True)
ipe.archiveImageDirectoryPaths(noLogoDirectory, has_logo = False)
ic.upload_brand_training_input_IPE_FAST(logo_brand, directory, noLogoDirectory, ipe, False)

for brand in brands:
    print 'downloading workloads for ' + brand
    blobs = ic.download_brand_operational_post_entities(brand, isProcessed = False)
    for blob in blobs:
        ipe = InstagramPostEntities(isTraining = False, isClassification = True)
        ipe.deserialize(blob.content)
        print "publishing to brand " + brand
        table_manager.upload_instagram_post_entities(brand, ipe)
