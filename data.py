import json
import time
import os

VIDEO_INFO_FOLDER_FILE = 'data/videoinfo_folder.txt'
RECORD_LIST_FILE = 'data/DownloadRecords.txt'

def Timestamp():
	return int(time.time())

def OptionalInDict(d, name):
	if name in d:
		return d[name]
	else:
		return None

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

	@staticmethod
	def FromDict(d):
		uniqueID = d['uniqueID']
		downloaded = d['downloaded']
		deadAsOf = OptionalInDict(d, 'deadAsOf')
		quality = OptionalInDict(d, 'quality')
		return Record(uniqueID, downloaded, deadAsOf, quality)

class DownloadRecords:
	def __init__(self, jsonStr = None):
		self.records = []
		if jsonStr is not None:
			d = json.loads(jsonStr)
			records = d['records']
			for record in records:
				newRecord = Record.FromDict(record)
				self.records.append(newRecord)
		self.savePath = None

	def Serialize(self):
		records = []
		for record in self.records:
			records.append(record.ToDict())
		d = {}
		d['records'] = records
		return json.dumps(d, indent=4)

	@staticmethod
	def LoadOrCreate(jsonPath = None):
		if jsonPath is None:
			jsonPath = RECORD_LIST_FILE
		if os.path.isfile(jsonPath):
			f = open(jsonPath, 'rb')
			buf = f.read()
			buf = buf.decode('utf8')
			records = DownloadRecords(buf)
		else:
			records = DownloadRecords()
		records.SetSavePath(RECORD_LIST_FILE)
		return records

	def SaveToFile(self):
		path = RECORD_LIST_FILE
		f = open(path, 'wb')
		buf = self.Serialize()
		bytes = buf.encode('utf8')
		f.write(bytes)
		f.close()

	def SetSavePath(self, path):
		self.savePath = path

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

	def AddRecord(self, uniqueID, downloaded, deadAsOf = None, quality = None):
		self.records.append(Record(uniqueID, downloaded, deadAsOf, quality))

	def MarkDownloaded(self, uniqueID, quality):
		record = self.GetRecord(uniqueID)
		record.downloaded = True
		record.quality = quality

	def MarkDead(self, uniqueID):
		record = self.GetRecord(uniqueID)
		if record.deadAsOf is None:
			record.deadAsOf = Timestamp()

class VideoInfo:
	def __init__(self, uniqueID, name = '', uploader = '', description = '', myName = '', myDesc = ''):
		self.uniqueID = uniqueID
		self.name = name
		self.uploader = uploader
		self.desc = description
		self.myName = myName
		self.myDesc = myDesc

	@staticmethod
	def FromJson(uniqueID, jsonStr):
		d = json.loads(jsonStr)
		return VideoInfo(uniqueID, d['name'], d['uploader'], d['desc'], d['myName'], d['myDesc'])

	def SaveToFile(self):
		f = open(VIDEO_INFO_FOLDER_FILE, 'r')
		toFolder = f.read()
		f.close()

		path = toFolder + self.uniqueID + '.txt'
		f = open(path, 'wb')
		buf = self.Serialize()
		bytes = buf.encode('utf8')
		f.write(bytes)
		f.close()

	def Serialize(self):
		d = {}
		d['name'] = self.name
		d['uploader'] = self.uploader
		d['desc'] = self.desc
		d['myName'] = self.myName
		d['myDesc'] = self.myDesc
		return json.dumps(d, ensure_ascii=False, indent=4)