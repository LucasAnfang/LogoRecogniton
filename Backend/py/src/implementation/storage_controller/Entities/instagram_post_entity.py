import json
import pickle
import os
from PIL import Image
import base64
DIMENSIONS = 'dimensions'
CAPTION = 'caption'
OWNER_ID = 'owner_id'
TAGS = 'tags'
TIME = 'taken_at_timestamp'
LOCATION = 'location'
LOGO_NAME = 'logo_name'
HAS_LOGO = 'has_logo'
ACCURACY = 'accuracy'
PICTURE = 'picture'
PICTURE_ID = 'picture_id'
""" NEW """
IMAGE_PATH = 'image_path'
IMAGE_CONTEXT = 'image_context'
TYPE = 'processing_type'
TYPE_TRAINING = 'training'
TYPE_CLASSIFICATION = 'classification'

class InstagramPostEntities:
	def __init__(self, isTraining = False, isClassification = False):
		self.posts = []
		self.isTraining = isTraining
		self.isClassification = isClassification
		if(self.isTraining == self.isClassification):
			raise ValueError('InstagramPostEntities must be either for classification or training')

	def append(self, post = None, brand_name = None):
		ig_post_entity = {}
		if(self.isClassification == True):
			if(post == None):
				raise ValueError('No post supplied')
			if "id" in post:
				ig_post_entity[PICTURE_ID] = post['id']
			if "dimensions" in post:
				ig_post_entity[DIMENSIONS] = post['dimensions']
			if "edge_media_to_caption" in post:
				ig_post_entity[CAPTION] = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
			if "owner" in post:
				ig_post_entity[OWNER_ID] = post["owner"]["id"]
			if "tags" in post:
				ig_post_entity[TAGS] = post["tags"]
			if "taken_at_timestamp" in post:
				ig_post_entity[TIME] = post["taken_at_timestamp"]
			if "location" in post and post['location'] is not None:
				if "name" in post["location"]:
					ig_post_entity[LOCATION] = post["location"]["name"]
			else:
				ig_post_entity[LOCATION] = None
			ig_post_entity[LOGO_NAME] = brand_name
			ig_post_entity[HAS_LOGO] = None
			ig_post_entity[IMAGE_CONTEXT] = None
			ig_post_entity[ACCURACY] = None
			ig_post_entity[PICTURE] = post['picture']
		if(self.isTraining == True):
			if(post == None):
				raise ValueError('No post supplied')
			if PICTURE in post:
				ig_post_entity[PICTURE] = post[PICTURE]
			ig_post_entity[PICTURE_ID] = post[PICTURE_ID]
			ig_post_entity['picture_id_with_extension'] = post['picture_id_with_extension']
			ig_post_entity[HAS_LOGO] = post[HAS_LOGO]
		self.posts.append(ig_post_entity)

	def extend(self, post_list):
		# print("Extending the list with elements", post_list)
		if post_list is not None:
			self.posts.extend(post_list)

	def archiveImageDirectory(self, directory, has_logo = True):
		if(self.isTraining == False):
			raise ValueError('You can only archive if this class is said to be for training')
		for image_name in os.listdir(directory):
			picture = self.openImage('{}/{}'.format(directory,image_name))
			if picture is None:
				continue
			post = {}
			post[PICTURE] = picture
			post[PICTURE_ID] = image_name.split('.')[0]
			post[HAS_LOGO] = has_logo
			self.append(post = post)

	def archiveImageDirectoryPaths(self, directory, has_logo = True):
		if(self.isTraining == False):
			raise ValueError('You can only archive if this class is said to be for training')
		for image_name in os.listdir(directory):
			if image_name == '.DS_Store':
				continue
			image_name
			post = {}
			post[PICTURE_ID] = image_name.split('.')[0]
			post['picture_id_with_extension'] = image_name
			post[HAS_LOGO] = has_logo
			self.append(post = post)

	def openImage(self, fileName):
		try:
			picture = Image.open(fileName)
			return picture
		except IOError:
			return None

	def serializeImage(self, picture):
		return {
			'pixels': base64.encodestring(picture.tobytes()),
			'size': picture.size,
			'mode': picture.mode,
		}

	def deserializeImage(self, serialized_image):
		return Image.frombytes(serialized_image['mode'], serialized_image['size'], base64.decodestring(serialized_image['pixels']))

	def size(self):
		return len(self.posts)

	def getImageAtIndex(self, index):
		""" return deserialized image """
		return self.deserializeImage(self.posts[index][PICTURE])

	def setImageContextAtIndex(self, index, image_context):
		if(self.isClassification == False):
			raise ValueError('You can only setImageContextAtIndex if you operational')
		self.posts[index][IMAGE_CONTEXT] = image_context

	def setHasLogoAtIndex(self, index, has_logo):
		if(self.isClassification == False):
			raise ValueError('You can only setHasLogoAtIndex if you operational')
		self.posts[index][HAS_LOGO] = has_logo

	def setAccuracyAtIndex(self, index, accuracy):
		if(self.isClassification == False):
			raise ValueError('You can only setAccuracyAtIndex if you operational')
		self.posts[index][ACCURACY] = accuracy

	def serialize(self):
		return json.dumps(self.posts, indent=4, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.posts = json.loads(serialized_entity)
