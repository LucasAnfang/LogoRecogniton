from log_entries_base import LogEntriesBase

class InputLogEntries(LogEntriesBase):
    """ Keys """
    """ PATH is coming from parent class """
    PATH = 'path'
    PROCESSING_STATUS = 'Processing_Status'
    PROCESSED = 'Processed'
    UNPROCESSED = 'Unprocessed'

    def __init__(self, filename = 'log.txt', log_entries = None):
        LogEntriesBase.__init__(self, filename, log_entries)

    def get_logs(self, isProcessed = None):
        if(isProcessed == None):
            filter = None
        else:
            processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
            filter = { InputLogEntries.PROCESSING_STATUS : processing_status }
        return LogEntriesBase.get_logs(self, filter = filter)

    def update(self, path, isProcessed):
        processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
        entry = { LogEntriesBase.PATH : path, InputLogEntries.PROCESSING_STATUS : processing_status }
        LogEntriesBase.update(self, entry)

    def get_paths_from_log(self, isProcessed = None):
        return [log_entry[LogEntriesBase.PATH] for log_entry in self.get_logs(isProcessed = isProcessed)]
