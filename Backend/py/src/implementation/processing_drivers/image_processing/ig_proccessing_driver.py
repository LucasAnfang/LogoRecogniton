import os
import io
from PIL import Image
from array import array
import numpy as np
import math
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from src.storage_controller.NetworkedFileSystem.storage_manager import LogoStorageConnector
from src.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from src.storage_controller.TableManagers.table_manager import TableStorageConnector
from src.models import train_image_classifier as train
from src.models import test_build as test
from src.models.datasets import convert_my as convert
class IGProccessingDriver:
	def __init__(self):
		self.storage_manager = LogoStorageConnector()
		self.table_manager = TableStorageConnector()

	def start_processing(self):
		print("starting driver...")
		self.brand_names = self.retrieve_supported_brands()
		for brand in self.brand_names:
			 training_post_entities_blobs = self.retrieve_unproccessed_training_post_entities(brand)
			 if(len(training_post_entities_blobs) != 0):
			 	training_post_entities_list = self.extract_post_entities_data(training_post_entities_blobs, isTraining = True)
			 	# self.process_training_post_entries(brand, training_post_entities_list)
			 else:
			 	print("No training data to be processed")

			operational_post_entities_blobs = self.retrieve_unproccessed_operational_post_entities(brand)
			if(len(operational_post_entities_blobs) != 0):
				operational_post_entities_list = self.extract_post_entities_data(operational_post_entities_blobs, isOperational = True)
				self.process_operational_post_entries(brand, operational_post_entities_list)
			else:
				print("No operational data to be processed")
			# self.update_log_files(training_post_entities_blobs, operational_post_entities_blobs)


	def update_log_files(self, training_post_entities_blobs, operational_post_entities_blobs):
		training_bucket_names = [blob.name.rsplit('/', 1)[0] for blob in training_post_entities_blobs]
		operational_bucket_names = [blob.name.rsplit('/', 1)[0] for blob in operational_post_entities_blobs]
		bucket_logs_to_update = []
		if(len(training_bucket_names) != 0):
			print ("training_bucket_names: ", training_bucket_names)
			bucket_logs_to_update.extend(training_bucket_names)
		if(len(operational_bucket_names) != 0):
			print ("training_bucket_names: ", operational_bucket_names)
			bucket_logs_to_update.extend(operational_bucket_names)

		# Activate when sure
		self.storage_manager.update_log_entries(bucket_logs_to_update, True)

	def process_operational_post_entries(self, brand, post_entities_list):
		for post_entities in post_entities_list:
			image_paths = [post_entity['image_path'] for post_entity in post_entities.posts]
			batch_size = 30
			r2d2 = R2D2(self.storage_manager)
			r2d2.set_image_paths(image_paths, batch_size = batch_size)
			current_index = 0
			testvar = False
			while(True):
				indices = [(current_index + i) for i in range(batch_size)]
				images = [r2d2.get_image_with_path(post_entities.posts[i]['image_path']) for i in indices if (i < len(post_entities.posts))]
				current_index += len(images)
				if(len(images) == 0):
					break
				print("images type ", type(images))
				results = test.classify("../../resources/train",images,reuse=testvar)
				print("results type ", type(results))
				testvar = True
				names = ["Not Patagonia","Patagonia"]
				patching_index = indices[0]
				for probabilities in results:
					print("probabilities type ", type(probabilities))
					for i in range(len(names)):
						print('Probability %0.2f => [%s]' % (probabilities[i], names[i]))
					post_entities.setAccuracyAtIndex(patching_index, float(probabilities[1]))
				 	#post_entities.setImageContextAtIndex(patching_index, probabilities)
				 	post_entities.setHasLogoAtIndex(patching_index, bool(round(probabilities[1])))
					patching_index += 1
			self.table_manager.upload_instagram_post_entities(brand, post_entities)
		print("Classification completed for brand: ", brand)

	def process_training_post_entries(self, brand, post_entities_list):
		for post_entities in post_entities_list:

			no_logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] == False]
			logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] == True]

			no_logo_image_paths = [post_entity['image_path'] for post_entity in no_logo_post_entities]
			logo_image_paths = [post_entity['image_path'] for post_entity in logo_post_entities]

			no_logo_r2d2 = R2D2(self.storage_manager)
			logo_r2d2 = R2D2(self.storage_manager)

			no_logo_r2d2.set_image_paths(no_logo_image_paths)
			logo_r2d2.set_image_paths(logo_image_paths)

			no_logo_images = []
			logo_images = []

			for post_entity in no_logo_post_entities:
				image_bytes = no_logo_r2d2.get_image_with_path(post_entity['image_path'])
				image = image_bytes #image = Image.open(io.BytesIO(image_bytes))
				print ("processing no logo image from ", post_entity['image_path'])
				no_logo_images.append(image)
			for post_entity in logo_post_entities:
				image_bytes = logo_r2d2.get_image_with_path(post_entity['image_path'])
				image = image_bytes
				print ("processing logo image from ", post_entity['image_path'])
				logo_images.append(image)

			labels = [1 for i in logo_images] + [0 for i in no_logo_images]
			images = []
			for image in logo_images:
				images.append(image)
			for image in no_logo_images:
				images.append(image)
			#call bryces interfaces here
			print("len of image",len(images))
			print("len of labels",len(labels))
			#convert.convert_to("../../resources/tfrecord",images,labels)
			train.train("../../resources/checkpoints/inception_v4.ckpt","../../resources/train","../../resources/tfrecord", logo_name= brand.capitalize())
		print("Training completed for brand: ", brand)


	def retrieve_supported_brands(self):
		return self.storage_manager.get_container_directories("input")

	def extract_post_entities_data(self, post_entities_blobs, isTraining = False, isOperational = False):
		if(isTraining == isOperational):
			raise ValueError('IG post entities has to be either training or operational (not both)')
		post_entities_list = []
		for post_entities in post_entities_blobs:
			brand_name = post_entities.name.split('/')[0]
			ipe = InstagramPostEntities(isTraining = isTraining, isClassification = isOperational)
			ipe.deserialize(post_entities.content)
			print("extracting ipe data for brand", brand_name, "from resource", post_entities.name)
			post_entities_list.append(ipe)
		return post_entities_list

	def retrieve_unproccessed_training_post_entities(self, brand_name):
		return self.storage_manager.download_brand_training_input_post_entities(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_post_entities(self, brand_name):
		return self.storage_manager.download_brand_operational_input_post_entities(brand_name, processing_status_filter="Unprocessed")

class R2D2:
	def __init__(self, storage_manager):
		self.storage_manager = storage_manager

	def reset(self):
		self.current_index = 0
		self.cache = []

	def set_image_paths(self, image_paths, batch_size = 10):
		self.image_paths = image_paths
		self.batch_size = batch_size
		self.reset()
		self.batch_download()

	def is_cache_empty(self):
		return (len(self.cache) == 0)

	def get_image_with_path(self, full_blob_name):
		if(self.is_cache_empty() == True):
			self.batch_download()
		return self.get_blob_from_cache(full_blob_name)
		# print "downloading image from path: " + full_blob_name
		# return self.download_data(full_blob_name)

	def get_blob_from_cache(self, full_blob_name):
		blob = None
		for index in range(len(self.cache)):
			if(self.cache[index].name == full_blob_name):
				print "blob with path: " + full_blob_name + " found in cache"
				blob = self.cache[index].content
				self.cache.pop(index)
				break
		if(blob == None):
			blob = self.download_data(full_blob_name)
			print "blob with path: " + full_blob_name + " NOT found in cache"
		return blob

	def download_data(self, full_blob_name):
		return self.storage_manager.download_input_data(full_blob_name)

	def batch_download(self):
		if(self.is_cache_empty() == False):
			return
		indices = [(self.current_index + i) for i in range(self.batch_size)]
		paths = [self.image_paths[i] for i in indices if (i < len(self.image_paths))]
		print "downloading next batch to cache..."
		self.current_index += len(paths)
		if(len(paths) != 0):
			self.cache.extend(self.storage_manager.parallel_input_image_download(paths))
