import os
import sys

import shutil
import requests

# TODO: Fix The class below to fit yours while looking at the one above (test it in a seperate file)
# Look at this https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
class R2D2:
	'''
		base_url: base url of the endpoint (Ex: http://localhost:2000)
		targets: routes to hit off the base url
		mode: what is the content and download method
	'''
	def __init__(self, base_url, targets, batch_size = 10, mode = 'image_download'):	
		if(mode == 'image_download'):
			self.image_download_enabled = True

		self.batch_size = batch_size
		self.base_url = base_url
		self.targets = targets
		self.reset()

	def reset(self):
		self.current_index = 0
		self.cache = []

	def start(self):
		self.batch_download()

	def set_output():


	def _is_cache_empty(self):
		return (len(self.cache) == 0)

	def _space_in_cache(self):
		return (len(self.cache) < self.batch_size)

	def get_artifact_with_url(self, url):
		if(self._is_cache_empty() == True):
			self.batch_download()
		return self.get_artifact_from_cache(url)

	def get_artifact_from_cache(self, url):
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
		return self.input_controller.download_data(full_blob_name)

	def batch_download(self):
		if(self.is_cache_empty() == False):
			return
		indices = [(self.current_index + i) for i in range(self.batch_size)]
		paths = [self.image_paths[i] for i in indices if (i < len(self.image_paths))]
		print "downloading next batch to cache..."
		self.current_index += len(paths)
		if(len(paths) != 0):
			self.cache.extend(self.parallel_download(paths))
	
	def parallel_download(self, urls):
		if(full_blob_names == None):
			return None
		threads = []
		results = []
		for full_blob_name in full_blob_names:
			result =  None
			t = threading.Thread(target=self._download_blob_helper, args=(self.base_url, base_dir, image_path, result))
			results.append(result)
			threads.append(t)
			t.start()
		[t.join() for t in threads]
		blobs = [r for r in results if r != None]
		return blobs

	'''
		base_url: http://localhost:2000
		base_dir: /datasets
		image_path: images/21mwvg4/patagonia/27891041_513296255732070_8569826624566984704_n.jpg
		result: result passed in to store result, in this case file path on local machine

	'''
	def _download_image_helper(self, base_url, base_dir, image_path, result):
		url = base_url + '/' + image_path
		result_path = base_dir + '/' + image_path
		response = requests.get(url, stream = True)
		with open(result_path, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
		result = result_path

def main():
	base_url = "http://localhost:2000"
	image_paths = ["images/21mwvg4/patagonia/27891041_513296255732070_8569826624566984704_n.jpg"]
	print("Hi!")

if __name__ == '__main__':
  main()

  #krk rocket 5

