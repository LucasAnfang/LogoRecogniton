import json
class LogEntriesBase:
	PATH = 'path'
	def __init__(self, filename = 'log.txt', _log_entries = None):
		self.reset_logs(_log_entries = _log_entries)
		self.filename = 'log.txt'

	def append(self, entry):
		if LogEntriesBase.PATH in entry:
			self.log_entries.append(entry)
		else:
			raise ValueError('Logs entries must have a path')

	def update(self, entry):
		if LogEntriesBase.PATH in entry:
			if(len([log_entry for log_entry in self.log_entries if log_entry[LogEntriesBase.PATH] == entry[LogEntriesBase.PATH]]) == 0):
				self.append(entry)
			else:
				entries = [log_entry for log_entry in self.log_entries if log_entry[LogEntriesBase.PATH] == entry[LogEntriesBase.PATH]]
				entries[0].update(entry)
		else:
			raise ValueError('Logs entries must have a path')

	def get_logs(self, filter = None):
		if(filter == None):
			return self.log_entries
		return [log_entry for log_entry in self.log_entries if filter.viewitems() <= log_entry.viewitems()]

	def reset_logs(self, _log_entries = None):
		self.log_entries = []
		if(_log_entries != None):
			for entry in _log_entries:
				self.append(entry)

	def serialize(self):
		return json.dumps(self.log_entries, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.log_entries = json.loads(serialized_entity)
