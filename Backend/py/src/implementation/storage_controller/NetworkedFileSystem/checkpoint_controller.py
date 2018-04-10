import os
import sys
import shutil


sys.path.append(os.path.join(os.path.dirname(__file__),'../Entities'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../NetworkedFileSystem'))

from nfs_controller_config import NFS_Controller_Config
from nfs_controller import NFS_Controller


from log_entries_base import LogEntriesBase
from input_log_entries import InputLogEntries
from instagram_post_entity import InstagramPostEntities
import uuid
import datetime

class CheckpointController:
	def __init__(self, config):
		try:
			import nfs_constants as constants
			self.constants = constants
		except:
			raise ValueError('Please specify networked file system contants in nfs_constants.py.')
		self.nfs_controller = NFS_Controller(config)
		self._create_checkpoint_container()

	""" Input Utility """
	def _create_checkpoint_container(self):
		self.nfs_controller.create_container(self._checkpoint_container())

	def _checkpoint_container(self):
		return self.constants.CHECKPOINTS_CONTAINER_NAME

	def get_container_directories(self):
		return self.nfs_controller.get_container_directories(self._checkpoint_container())

	def swap_out_checkpoints(self, prev, next):
		def clear_dir(name):
			for the_file in os.listdir(name):
			    file_path = os.path.join(name, the_file)
			    try:
			        if os.path.isfile(file_path):
			            os.unlink(file_path)
			    except Exception as e:
			        print(e)
		def swap_dir(prev, next):
			for the_file in os.listdir(next):
			    file_path = os.path.join(next, the_file)
			    try:
			        if os.path.isfile(file_path):
			            shutil.move(file_path, prev)
			    except Exception as e:
			        print(e)

		if os.path.isdir(prev) and os.path.isdir(next):
			clear_dir(prev)
			swap_dir(prev,next)
			clear_dir(next)
		else:
			print("one of these faild")

	""" Upload """
	def upload_checkpoints(self, origin_directory):
		self.nfs_controller.batched_parallel_directory_upload(self._checkpoint_container(), "", origin_directory, ext_filter_list = None)

	""" Download """
	def download_checkpoints(self, destination_directory = None):
		print( "download checkpoints " + destination_directory)
		self.nfs_controller.download_full_container(self._checkpoint_container(), destination_directory = destination_directory)

	def parallel_download(self, full_blob_names):
		return self.nfs_controller.parallel_download(self._input_container(), full_blob_names)

	def download_data(self, full_blob_name):
		container = self._input_container()
		return self.nfs_controller.download_data(container, full_blob_name)
