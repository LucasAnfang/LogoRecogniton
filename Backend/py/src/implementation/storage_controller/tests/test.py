import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from src.storage_controller.NetworkedFileSystem.storage_manager import LogoStorageConnector
from src.storage_controller.Entities.input_log_entries import InputLogEntries

logs = InputLogEntries("fu.txt")
print logs.filename
path_one = 'path_one'
path_two = 'path_two'
print 'adding path one (not processed) : {}'.format(logs.update(path_one, False))
print 'get logs: {}'.format(logs.get_logs())
print 'get processed logs: {}'.format(logs.get_logs(isProcessed = True))
print 'update path one to processed: {}'.format(logs.update(path_one, True))
print 'get processed logs: {}'.format(logs.get_logs(isProcessed = True))
print 'get logs: {}'.format(logs.get_logs())
print 'adding path two (not processed) : {}'.format(logs.update(path_two, False))
print 'get unprocessed logs: {}'.format(logs.get_logs(isProcessed = False))
print 'get logs: {}'.format(logs.get_logs())
print 'get processed paths: {}'.format(logs.get_paths_from_log(isProcessed = True))
print 'get unprocessed paths: {}'.format(logs.get_paths_from_log(isProcessed = False))
print 'get paths: {}'.format(logs.get_paths_from_log())

indices_test = False
upload_demo = False
log_demo = False
download_demo = False
lsc = LogoStorageConnector()
if(indices_test == True):
	image_paths = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

	current_index = 0
	temp_current_index = current_index
	indices = [(current_index + i) for i in range(5)]
	paths = [image_paths[i] for i in indices]
	print paths
	current_index += 5

	for index in range(len(paths)):
		if(paths[index] == "2"):
			print("found 2")
			paths.pop(index)
			break
	print paths

	indices = [(current_index + i) for i in range(5)]
	paths = [image_paths[i] for i in indices]
	print paths

	current_index += 5

	indices = [(current_index + i) for i in range(5)]
	paths = [image_paths[i] for i in indices]
	print paths

	current_index += 5

	indices = [(current_index + i) for i in range(5)]
	paths = [image_paths[i] for i in indices if (i < len(image_paths))]
	print paths
#"Puma", "Lego", "Nike", "Adidas",
brand_names = ["patagonia"]

if(upload_demo == True):
	print("Demo for upload to various directories for", brand_names)
	for brand_name in brand_names:
		print("\nUploading ", brand_name, " Training Data [UNPROCESSED]")
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

		print("\nUploading ", brand_name, " Operational Data [UNPROCESSED]")
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

		print("\nUploading ", brand_name, " Training Data [PROCESSED]")
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_1", isProcessed = True))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_2", isProcessed = True))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_3", isProcessed = True))

		print("\nUploading ", brand_name, " Operational Data [PROCESSED]")
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_1", isProcessed = True))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_2", isProcessed = True))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_3", isProcessed = True))

print("These are the current brands being supprted or sleighted to be processed")
vds = lsc.get_container_directories("input")
for entity in vds:
	print('[',entity,']')

if(log_demo == True):
	print("Demo for analyzing logs for multiple brands and their existing directories", brand_names)
	for brand_name in brand_names:
		path = brand_name + "/training"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "patagonia/training", "Unprocessed")
		for entity in unprocessed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "patagonia/training", "Processed")
		for entity in processed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")

		path = brand_name + "/operational"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "patagonia/operational", "Unprocessed")
		for entity in unprocessed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "patagonia/operational", "Processed")
		for entity in processed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")


if(download_demo == True):
	print("Demo for downloading data for multiple brands unprocessed input/operational data", brand_names)
	for brand_name in brand_names:
		# blobs = lsc.download_brand_training_input_data(brand_name, processing_status_filter="Unprocessed")
		# for blob in blobs:
		# 	print("  blob name:",blob.name)
		# 	print("    blob content:",blob.content)
		blobs = lsc.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")
		for blob in blobs:
			print("  blob name:",blob.name)
			if(blob.content != None):
				print("    blob content:",len(blob.content))
			else:
				print("    could not download blob contents")
