import json

class Record:
	def __init__(self, uniqueID, downloaded, deadAsOf = None, quality = None):
		self.uniqueID = uniqueID
		self.deadAsOf = deadAsOf
		self.downloaded = downloaded
		self.quality = quality

	def ToDict(self):
		d = {}
		d['uniqueID'] = self.uniqueID
		if self.deadAsOf is not None:
			d['deadAsOf'] = self.deadAsOf
		d['downloaded'] = self.downloaded
		if self.quality is not None:
			d['quality'] = self.quality
		return d

class DownloadRecords:
	def __init__(self, json = None):
		self.records = []
		if json is not None:
			pass

	def Serialize(self):
		records = []
		for record in self.records:
			records.append(record.ToDict())
		d = {}
		d['records'] = records
		return json.dumps(d)

	def GetRecord(self, uniqueID):
		for record in self.records:
			if record.uniqueID == uniqueID:
				return record
		return None

	def HasRecord(self, uniqueID):
		if self.GetRecord(uniqueID) is not None:
			return True
		else:
			return False

	def AddRecord(self): # more params
		# TODO
		pass

	def MarkDownloaded(self, uniqueID, quality):
		self.GetRecord(uniqueID).quality = quality

	def MarkDead(self, uniqueID):
		# self.GetRecord(uniqueID).deadAsOf = [some sort of timestamp]
		# TODO
		pass

class VideoInfo:
	def __init__(self, json = None):
		if json is not None:
			pass
		else:
			self.name = ''
			self.uploader = ''
			self.desc = ''
			self.myName = ''
			self.myDesc = ''

	def SetMetadata(self, name, uploader, description, myName = '', myDesc = ''):
		self.name = name
		self.uploader = uploader
		self.desc = description
		self.myName = myName
		self.myDesc = myDesc

	def Serialize(self):
		d = {}
		d['name'] = self.name
		d['uploader'] = self.uploader
		d['desc'] = self.desc
		d['myName'] = self.myName
		d['myDesc'] = self.myDesc
		return json.dumps(d)