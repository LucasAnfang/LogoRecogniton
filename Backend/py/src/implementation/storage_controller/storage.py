import azure
from azure.storage import *
from azure.storage.blob import BlockBlobService
from datetime import datetime
import os, mimetypes
from azure.cosmosdb.table import TableService, Entity


class AzureStorage():

    def __init__(self, container=None):
        self.AZURE_STORAGE_ACCOUNT = 'logodetectionstorage'
        self.AZURE_STORAGE_KEY  = 'jPJyzct+8WD1lKU5M+ZwDflWUGRu+YBpH8n/3Z6qR7WD7uc3HV2U1rtiQKesLRq2tU3jtXIe26RklAYdKzoydA=='
        self.table_service = TableService(account_name=self.AZURE_STORAGE_ACCOUNT, account_key=self.AZURE_STORAGE_KEY)
        self.blob_service = BlockBlobService(account_name=self. AZURE_STORAGE_ACCOUNT, account_key=self.AZURE_STORAGE_KEY)
        self.container = "input"
        self.table_list = [] #everything in the table for this logo
        self.logo = ""

    def query(self, tableName, partitionKey, rowKey):
        task = self.table_service.get_entity(tableName, partitionKey, rowKey)
        return task

    def retrieve_table(self, tableName):
        #tasks = table_service.query_entities(tableName, filter="PartitionKey eq 'tasksSeattle'", select='description')
        try:
            tasks = self.table_service.query_entities(tableName)
        except:
            return None
        self.logo = tableName
        for task in tasks:
            self.table_list.append(task)
        self.table_list = sorted(self.table_list, key=lambda k: k['has_logo'], reverse=True) 
        return self.table_list
    
    def download_blob(self, path, logoName):
        #download pic into logoName file
        path = "images/" + logoName 

        self.blob_service.get_blob_to_path(self.container, path, "test.jpeg")

    def exists(self, name):
        try:
            self.blob_service.get_blob_properties(self.container, name)
            return True
        except:
            return False

