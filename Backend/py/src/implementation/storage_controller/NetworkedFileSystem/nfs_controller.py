import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../..'))
from azure.storage.blob import PublicAccess
from azure.storage import CloudStorageAccount
from azure.storage.blob import (
    ContentSettings,
    BlobBlock,
    BlockListType,
)
from src.implementation.storage_controller.Entities.log_entries_base import LogEntriesBase
from nfs_controller_config import NFS_Controller_Config
import uuid
import datetime
import json
from io import BytesIO
import zlib
import threading
import base64
from PIL import Image

class NFS_Controller:
	def __init__(self, config):
		self.config = config
		self.account = CloudStorageAccount(account_name=config.storage_account_name, account_key=config.storage_account_key)
		self.service = self.account.create_block_blob_service()

	""" utility functions """
	def get_containers(self):
		containers = self.service.list_containers()
		return containers

	def get_container_directories(self, container_name):
		bloblistingresult = self.service.list_blobs(container_name=container_name, delimiter='/')
		return [blob.name.rsplit('/', 1)[0] for blob in bloblistingresult]

	def create_container(self, container_name):
		self.service.create_container(container_name)

	def get_parent_directory(self, path):
		return path.rsplit('/', 1)[0]

	def exists(self, container, full_blob_name = None):
		return self.service.exists(container, full_blob_name)

	def generate_uid(self):
		r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
		return r_uuid.replace('=', '')

	""" Upload: """
	def parallel_chunky_upload(self, container_name, full_blob_name, data, chunks = 5):
		debug = False
		threads = []
		block_ids = []
		chunk_size = len(data) / chunks
		chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]
		for chunk in chunks:
			uid = self.generate_uid()
			block_ids.append(BlobBlock(id=uid))
			t = threading.Thread(target=self._upload_block, args=(container_name,full_blob_name,chunk,uid,))
			threads.append(t)
			t.start()
		[t.join() for t in threads]
		self.service.put_block_list(container_name, full_blob_name, block_ids)
		return full_blob_name

	def _upload_block(self, container_name, full_blob_name, chunk, uid):
		self.service.put_block(container_name, full_blob_name, chunk, uid)

	def upload_text(self, container_name, full_blob_name, data):
		if not(self.exists(container_name)):
			self.create_container(container_name)
		self.service.create_blob_from_text(container_name, full_blob_name, data)
		return full_blob_name

	def upload_image(self, container_name, path, data):
		if not(self.exists(container_name)):
			self.create_container(container_name)
		full_blob_name = '{}{}'.format(path, '.jpeg')
		with BytesIO() as output:
			data.save(output, 'jpeg')
			image_bytes = output.getvalue()
		self.parallel_chunky_upload(container_name, full_blob_name, image_bytes)
		return full_blob_name

	def upload_from_path(self, container_name, base_nfs_path, file_path):
		if not(self.exists(container_name)):
			self.create_container(container_name)
		path = file_path.rsplit('/', 1)[1] if ('/' in file_path) else file_path
		if(base_nfs_path == ""):
			full_blob_name = '{}'.format(path)
		else:
			full_blob_name = '{}/{}'.format(base_nfs_path, path)
		self.service.create_blob_from_path(container_name, full_blob_name, file_path)

	def batched_parallel_directory_upload(self, container_name, base_nfs_path, dirpath, ext_filter_list = ['.jpeg', '.png', '.jpg']):
		print dirpath
		if(ext_filter_list == None):
			file_paths = [os.path.realpath('{}/{}'.format(dirpath,fn)) for fn in os.listdir(dirpath)]
		else:
			file_paths = [os.path.realpath('{}/{}'.format(dirpath,fn)) for fn in os.listdir(dirpath) if any(fn.endswith(extension_filter) for extension_filter in ext_filter_list)]
		# print file_paths
		total_files_count = len(file_paths)
		current_index = 0
		batch_size = 30
		if not(self.exists(container_name)):
			self.create_container(container_name)
		batch_number = 1
		while(True):
			indices = [(current_index + i) for i in range(batch_size)]
			file_paths_batch = [file_paths[i] for i in indices if (i < total_files_count)]
			current_index += len(file_paths_batch)
			if(len(file_paths_batch) == 0):
				break
			threads = []
			index = indices[0]
			for file_path in file_paths_batch:
				print '[Batch {}: Percent of total {}]Uploading image from file path: {}'.format(batch_number, (((index * 1.0)/ (total_files_count - 1)) * 100.0), file_path)
				t = threading.Thread(target=self.upload_from_path, args=(container_name, base_nfs_path, file_path))
				threads.append(t)
				index = index + 1
				t.start()
			[t.join() for t in threads]
			batch_number = batch_number + 1

	""" Download """
	def parallel_download(self, container_name, full_blob_names):
		if(full_blob_names == None):
			return None
		threads = []
		results = []
		for full_blob_name in full_blob_names:
			result = {'blob': None}
			t = threading.Thread(target=self._download_blob_helper, args=(container_name,full_blob_name, result))
			results.append(result)
			threads.append(t)
			t.start()
		[t.join() for t in threads]
		blobs = [result['blob'] for result in results if result['blob'] != None]
		return blobs

	def _download_blob_helper(self, container_name, full_blob_name, result):
		if(self.exists(container_name, full_blob_name)):
			result['blob'] = self.download_data(container_name, full_blob_name)
		else:
			return None

	def download_data(self, container_name, full_blob_name):
		print "Full blob name: " + full_blob_name
		if not(self.exists(container_name)):
			self.create_container(container_name)
			return None
		blob = self.service.get_blob_to_bytes(container_name, full_blob_name)
		return blob

	def download_full_container(self, container_name, destination_directory = None):
		if not(destination_directory == None):
			destination_directory = os.path.realpath(destination_directory)
			if not (os.path.isdir(destination_directory)):
				os.makedirs(destination_directory)
		else:
			destination_directory = os.getcwd()
		if not(self.exists(container_name)):
			raise ValueError('Container does not exist')
		blobs = self.service.list_blobs(container_name)
		#code below lists all the blobs in the container and downloads them one after another
		for blob in blobs:
			print(blob.name)
			print("{}".format(blob.name))
			#check if the path contains a folder structure, create the folder structure
			if "/" in "{}".format(blob.name):
				print("there is a path in this")
				#extract the folder path and check if that folder exists locally, and if not create it
				head, tail = os.path.split("{}".format(blob.name))
				print(head)
				print(tail)
				if (os.path.isdir(destination_directory+ "/" + head)):
					#download the files to this directory
					print("directory and sub directories exist")
					self.service.get_blob_to_path(container_name,blob.name,destination_directory+ "/" + head + "/" + tail)
				else:
					#create the diretcory and download the file to it
					print("directory doesn't exist, creating it now")
					os.makedirs(destination_directory+ "/" + head)
					print("directory created, download initiated")
					self.service.get_blob_to_path(container_name,blob.name,destination_directory+ "/" + head + "/" + tail)
			else:
				self.service.get_blob_to_path(container_name,blob.name,destination_directory + "/" + blob.name)

	""" Logging """
	def retrieve_log_entities(self, container_name, path, filter = None):
		log_path = '{}/log.txt'.format(path)
		log_entries = LogEntriesBase()
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		if(filter != None):
			log_entries = log_entries.get_logs(filter=filter)
		return log_entries

	def update_log(self, container_name, entry):
		path = self.get_parent_directory(entry[LogEntriesBase.PATH])
		log_path = '{}/log.txt'.format(path)
		log_entries = LogEntriesBase()
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		log_entries.update(entry)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	def update_logs(self, container_name, entries):
		log_paths = {'{}/log.txt'.format(self.get_parent_directory(log_entry[LogEntriesBase.PATH])) for log_entry in entries}
		if len(log_paths) > 1:
			raise ValueError('Logs being updated must be of the same log file')
		log_path = log_paths[0]
		if not self.exists(container_name,log_path):
			raise ValueError('Log file {} under container {} does not exist'.format(log_path, container_name))
		log_entries = LogEntriesBase()
		log_file = self.service.get_blob_to_text(container_name, log_path)
		raw_logs = log_file.content
		log_entries.deserialize(raw_logs)
		for entry in entries:
			log_entries.update(entry)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	""" Avoid Using this: It is not efficient and you should always update a log directly after resource use """
	def update_multiple_log_files(self, container_name, entries):
		log_paths = {'{}/log.txt'.format(self.get_parent_directory(log_entry[LogEntriesBase.PATH])) for log_entry in entries}
		for log_path in log_paths:
			entries = [log_entry for log_entry in entries if '{}/log.txt'.format(self.get_parent_directory(log_entry[LogEntriesBase.PATH])) == log_path]
			self.update_logs(container_name, entries)
