import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
# from src.Drivers.ig_proccessing_driver import IGProccessingDriver

from src.storage_controller.NetworkedFileSystem.nfs_controller_config import NFS_Controller_Config
from src.storage_controller.NetworkedFileSystem.nfs_controller import NFS_Controller
from src.storage_controller.NetworkedFileSystem.checkpoint_controller import CheckpointController
# file_path = 'Lucas/12345678.jpg'
# print file_path
# image_path = file_path.rsplit('/', 1)[1] if ('/' in file_path) else file_path
# print image_path
#
# file_path = '12345678.jpg'
# print file_path
# image_path = file_path.rsplit('/', 1)[1] if ('/' in file_path) else file_path
# print image_path

# directory = '../test_images'
directory = '../../instagram_scraper/patagonia'
ext = '.jpg'
# file_paths = [os.path.abspath(fn) for fn in os.listdir(directory) if (fn.endswith(ext))]# for ext in included_extensions)]
# print file_paths

STORAGE_ACCOUNT_NAME = 'logodetectiontesting'
STORAGE_ACCOUNT_KEY = 'HF0EwhCG2R8BBeKGV5qrloyz5Ua0kYQlSQI/vDWsTv3AjjK2nDJOD6Y8iLPjtF6nMnJr2zQZ0xhxkDF0biCArg=='
config = NFS_Controller_Config(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
nfs = NFS_Controller(config)
cc = CheckpointController(config)
# nfs.batched_parallel_directory_upload('testing', 'patagonia', directory, '.jpg')
cc.download_checkpoints(destination_directory = './fun')
cc.upload_checkpoints('./fun')
