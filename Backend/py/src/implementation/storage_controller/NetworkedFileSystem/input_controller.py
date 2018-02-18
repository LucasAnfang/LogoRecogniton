import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../..'))
from src.implementation.storage_controller.Entities.log_entries_base import LogEntriesBase
from src.implementation.storage_controller.Entities.input_log_entries import InputLogEntries
from src.implementation.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from nfs_controller_config import NFS_Controller_Config
from nfs_controller import NFS_Controller
import uuid
import datetime

class InputController:
	def __init__(self, config):
		try:
			import nfs_constants as constants
			self.constants = constants
		except:
			raise ValueError('Please specify networked file system contants in nfs_constants.py.')
		self.nfs_controller = NFS_Controller(config)
		self._create_input_container()

	""" Input Utility """
	def _create_input_container(self):
		self.nfs_controller.create_container(self._input_container())

	def _create_path_to_bucket(self, brand_name, level):
		return '{}/{}/{}=={}'.format(brand_name, level, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

	def _get_bucket_image_directory(self, prefix):
		return '{}/[IMAGES]'.format(prefix)

	def _get_bucket_post_entities_file(self, prefix):
		return '{}/post_entities.txt'.format(prefix)

	def _input_container(self):
		return self.constants.INPUT_CONTAINER_NAME

	def get_container_directories(self):
		return self.nfs_controller.get_container_directories(self._input_container())

	""" Upload: input """
	def upload_brand_training_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(brand, self.constants.TRAINING_DIRECTORY_NAME, IPE, isProcessed)

	def upload_brand_training_input_IPE_FAST(self, brand, logo_dir, no_logo_dir, IPE, isProcessed):
		bucket_path = self._create_path_to_bucket(brand, self.constants.TRAINING_DIRECTORY_NAME)
		bucket_post_entities_full_path = self._get_bucket_post_entities_file(bucket_path)
		bucket_images_base_path = self._get_bucket_image_directory(bucket_path)
		print 'bucket_path: {}\nbucket_post_entities_full_path: {}\nbucket_images_base_path: {}\n'.format(bucket_path, bucket_post_entities_full_path, bucket_images_base_path)
		self.nfs_controller.batched_parallel_directory_upload(self._input_container(), bucket_images_base_path, logo_dir)
		self.nfs_controller.batched_parallel_directory_upload(self._input_container(), bucket_images_base_path, no_logo_dir)
		for element in IPE.posts:
			path = '{}/{}'.format(bucket_images_base_path, element['picture_id_with_extension'])
			element['image_path'] = path
		self.nfs_controller.upload_text(self._input_container(), bucket_post_entities_full_path, IPE.serialize())
		self.log(bucket_path, isProcessed)
		return  bucket_path

	def upload_brand_classification_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(brand, self.constants.CLASSIFICATION_DIRECTORY_NAME, IPE, isProcessed)

	def upload_IPE_to_bucket(self, brand, directory, IPE, isProcessed):
		bucket_path = self._create_path_to_bucket(brand, directory)
		bucket_post_entities_full_path = self._get_bucket_post_entities_file(bucket_path)
		bucket_images_base_path = self._get_bucket_image_directory(bucket_path)
		for element in IPE.posts:
			print(element.keys())
			if('picture' in element and 'picture_id' in element):
				path = '{}/{}'.format(bucket_images_base_path, element['picture_id'])
				image_path = self.nfs_controller.upload_image(self._input_container(), path, element['picture'])
				element.pop('picture', None)
				element['image_path'] = image_path
		self.nfs_controller.upload_text(self._input_container(), bucket_post_entities_full_path, IPE.serialize())
		self.log(bucket_path, isProcessed)
		return  bucket_path

	""" Download """
	def download_brand_training_post_entities(self, brand, isProcessed = None):
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		return self.download_brand_post_entities(brand, path, isProcessed = isProcessed)

	def download_brand_classification_post_entities(self, brand, isProcessed = None):
		path = '{}/{}'.format(brand, self.constants.CLASSIFICATION_DIRECTORY_NAME)
		return self.download_brand_post_entities(brand, path, isProcessed = isProcessed)

	def download_brand_post_entities(self, brand, prefix, isProcessed = None):
		blobs = []
		container_name = self._input_container()
		logs = self.retrieve_log_entities(prefix, isProcessed = isProcessed, paths_only = True)
		for log in logs:
			print log
			blobs.append(self.nfs_controller.download_data(container_name, '{}/{}'.format(log, 'post_entities.txt')))
		return blobs

	def parallel_download(self, full_blob_names):
		return self.nfs_controller.parallel_download(self._input_container(), full_blob_names)

	def download_data(self, full_blob_name):
		container = self._input_container()
		return self.nfs_controller.download_data(container, full_blob_name)

	""" log """
	def log(self, path, isProcessed):
		processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
		entry = { LogEntriesBase.PATH : path, InputLogEntries.PROCESSING_STATUS : processing_status }
		self.nfs_controller.update_log(self._input_container(), entry)

	def retrieve_log_entities(self, path, isProcessed = None, paths_only = False):
		container = self._input_container()
		if(isProcessed == None):
			filter = None
		else:
			processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
			filter = { InputLogEntries.PROCESSING_STATUS : processing_status }
		log_entries = self.nfs_controller.retrieve_log_entities(container, path, filter = filter)
		if(paths_only == True and isProcessed == None): #if isProcessed is not None, it will be paths only already
			return [log_entry[LogEntriesBase.PATH] for log_entry in log_entries.log_entries]
		elif(paths_only == True): #if isProcessed is not None, it will be paths only already
			return [log_entry[LogEntriesBase.PATH] for log_entry in log_entries]
		return log_entries

	def update_log_entries(self, paths, isProcessed):
		processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
		entries = []
		for path in paths:
			entry = { LogEntriesBase.PATH : path, InputLogEntries.PROCESSING_STATUS : processing_status }
			entries.append(entry)
		self.nfs_controller.update_logs(self._input_container(), entries)
