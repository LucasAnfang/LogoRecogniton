import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../..'))
import time
import uuid
from datetime import datetime
import uuid
import datetime
import json
from src.implementation.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from src.implementation.storage_controller.NetworkedFileSystem.nfs_controller_config import NFS_Controller_Config
from io import BytesIO
from io import BytesIO
import zlib
import threading
import base64
from PIL import Image
from azure.storage import CloudStorageAccount
from azure.common import (
    AzureHttpError,
    AzureConflictHttpError,
    AzureMissingResourceHttpError,
)
from azure.storage import (
    Logging,
    Metrics,
    CorsRule,
)
from azure.storage.table import (
    Entity,
    TableBatch,
    EdmType,
    EntityProperty,
    TablePayloadFormat,
)
DIMENSIONS = 'dimensions'
CAPTION = 'caption'
OWNER_ID = 'owner_id'
TAGS = 'tags'
TIME = 'time'
LOCATION = 'location'
LOGO_NAME = 'logo_name'
HAS_LOGO = 'has_logo'
PICTURE = 'picture'
PICTURE_ID = 'picture_id'
""" NEW """
IMAGE_PATH = 'image_path'
IMAGE_CONTEXT = 'image_context'
TYPE = 'processing_type'
TYPE_TRAINING = 'training'
TYPE_CLASSIFICATION = 'classification'
ACCURACY = 'accuracy'

class TableStorageConnector:
	def __init__(self, config):
		self.config = config
		self.account = CloudStorageAccount(account_name=config.storage_account_name, account_key=config.storage_account_key)
		self.service = self.account.create_table_service()

	#only successful table creations (name is unique, not None, and does not contain illegal characters) returns the original table_name
	def create_table(self, table_name):
		if(table_name == None):
			return None;
		success = self.service.create_table(table_name)
		if(success == False):
			return None
		return table_name

	#only successful table deletions (table exists) returns the original table_name
	def delete_table(self, table_name):
		if(table_name == None):
			return None;
		success = self.service.delete_table(table_name)
		if(success == False):
			return None
		return table_name

	#only returns true if name is not None and the table exists
	def exists(self, table_name):
		if(table_name == None):
			return False;
		return self.service.exists(table_name)

	# All operations in the same batch must have the same partition key but different row keys
	# Batches can hold from 1 to 100 entities
	# Batches are atomic. All operations completed simulatenously. If one operation fails, they all fail.
	# Insert, update, merge, insert or merge, insert or replace, and delete entity operations are supported
	def _batch_upload(self, table_name, post_entities):
		# Context manager style
		if(len(post_entities) == 0):
			return
		if(len(post_entities) > 100):
			raise ValueError("batch cannot be over 100 entries")

		# Context manager style
		# with self.service.batch(table_name) as batch:
		# 	for entity in post_entities:
		# 		batch.insert_entity(entity)

		# Commit style
		batch = TableBatch()
		for entity in post_entities:
			if(entity == None):
				print "entity none"
				break
			batch.insert_entity(entity)
		self.service.commit_batch(table_name, batch)

	def upload_instagram_post_entities(self, brand_name, IPE):
		print "Batch upload called for brand: " + brand_name
		table_name = brand_name
		if not(self.exists(table_name)):
			table_name = self.create_table(table_name)
			print (table_name ," table created...")
		current_index = 0
		while(True):
			pk = self.get_pk()
			indices = [(current_index + i) for i in range(100)]
			instagram_post_entities = [IPE.posts[i] for i in indices if (i < len(IPE.posts))]
			if(len(instagram_post_entities) == 0):
				break;
			current_index += len(instagram_post_entities)
			batch = [self.create_entity(post, pk = pk, rk = self.get_rk()) for post in instagram_post_entities]
			# print batch
			self._batch_upload(table_name, batch)
			print "uploading batch with pk " + pk
		print "batch upload completed"

	def get_pk(self):
		return 'pk{}'.format(str(uuid.uuid4()).replace('-', ''))

	def get_rk(self):
		return 'rk{}'.format(str(uuid.uuid4()).replace('-', ''))

	def create_entity(self, instagram_post_entity, pk = None, rk = None):
		entity = {}

		if(pk != None):
			entity['PartitionKey'] = pk
		else:
			entity['PartitionKey'] = self.get_pk()

		if(rk != None):
			entity['RowKey'] = rk
		else:
			entity['RowKey'] = self.get_pk()

		if(PICTURE_ID in instagram_post_entity and instagram_post_entity[PICTURE_ID] != None):
			entity[PICTURE_ID] = EntityProperty(EdmType.INT64, instagram_post_entity[PICTURE_ID])

		if(OWNER_ID in instagram_post_entity and instagram_post_entity[OWNER_ID] != None):
			entity[OWNER_ID] = EntityProperty(EdmType.INT64, instagram_post_entity[OWNER_ID])

		if(LOGO_NAME in instagram_post_entity and instagram_post_entity[LOGO_NAME] != None):
			entity[LOGO_NAME] = EntityProperty(EdmType.STRING, instagram_post_entity[LOGO_NAME])

		#This is a unix epoch timestamp (we will do conversion from utc to epoch for search)
		if(TIME in instagram_post_entity and instagram_post_entity[TIME] != None):
			entity[TIME] = EntityProperty(EdmType.INT64, instagram_post_entity[TIME])

		if(CAPTION in instagram_post_entity and instagram_post_entity[CAPTION] != None):
			entity[CAPTION] = EntityProperty(EdmType.STRING, instagram_post_entity[CAPTION])

		if(TAGS in instagram_post_entity and instagram_post_entity[TAGS] != None):
			entity[TAGS] = EntityProperty(EdmType.STRING, self.serialize_entity_attribute_value(instagram_post_entity[TAGS]))

		if(HAS_LOGO in instagram_post_entity and instagram_post_entity[HAS_LOGO] != None):
			entity[HAS_LOGO] = EntityProperty(EdmType.BOOLEAN, instagram_post_entity[HAS_LOGO])

		if(ACCURACY in instagram_post_entity and instagram_post_entity[ACCURACY] != None):
			entity[ACCURACY] = EntityProperty(EdmType.DOUBLE, instagram_post_entity[ACCURACY])

		if(IMAGE_CONTEXT in instagram_post_entity and instagram_post_entity[IMAGE_CONTEXT] != None):
			entity[IMAGE_CONTEXT] = EntityProperty(EdmType.STRING, self.serialize_entity_attribute_value(instagram_post_entity[IMAGE_CONTEXT]))

		if(IMAGE_PATH in instagram_post_entity and instagram_post_entity[IMAGE_PATH] != None):
			entity[IMAGE_PATH] = EntityProperty(EdmType.STRING, instagram_post_entity[IMAGE_PATH])

		if(DIMENSIONS in instagram_post_entity and instagram_post_entity[DIMENSIONS] != None):
			entity[DIMENSIONS] = EntityProperty(EdmType.STRING, self.serialize_entity_attribute_value(instagram_post_entity[DIMENSIONS]))
		return entity


	def serialize_entity_attribute_value(self, attribute_value):
		if(attribute_value == None):
			return ""
		return json.dumps(attribute_value, indent=4, ensure_ascii=False)

	def get_all_entries(self, table_name):
		 return list(self.service.query_entities(table_name))
