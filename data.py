import json
import time
import os

import config

def Timestamp():
	return int(time.time())

def OptionalInDict(d, name):
	if name in d:
		return d[name]
	else:
		return None

class Record:
	def __init__(self, uniqueID, downloaded, deadAsOf = None, quality = None, wasTooLong = None):
		self.uniqueID = uniqueID
		self.deadAsOf = deadAsOf
		self.downloaded = downloaded
		self.quality = quality
		self.wasTooLong = wasTooLong

	def ToDict(self):
		d = {}
		d['uniqueID'] = self.uniqueID
		if self.deadAsOf is not None:
			d['deadAsOf'] = self.deadAsOf
		d['downloaded'] = self.downloaded
		if self.quality is not None:
			d['quality'] = self.quality
		if self.wasTooLong is not None:
			d['wasTooLong'] = self.wasTooLong
		return d

	@staticmethod
	def FromDict(d):
		uniqueID = d['uniqueID']
		downloaded = d['downloaded']
		deadAsOf = OptionalInDict(d, 'deadAsOf')
		quality = OptionalInDict(d, 'quality')
		wasTooLong = OptionalInDict(d, 'wasTooLong')
		return Record(uniqueID, downloaded, deadAsOf, quality, wasTooLong)

	def VideoFileExists(self):
		toFolder = config.GetVideoFolder()
		path = toFolder + self.uniqueID
		def ExistsWithExt(ext):
			if os.path.exists(path + ext):
				if os.path.getsize(path + ext) > 0:
					return True
			return False
		return ExistsWithExt('.mp4') or ExistsWithExt('.flv') or ExistsWithExt('.swf')

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
			jsonPath = config.GetDownloadRecordPath()
		if os.path.isfile(jsonPath):
			f = open(jsonPath, 'rb')
			buf = f.read()
			buf = buf.decode('utf8')
			records = DownloadRecords(buf)
		else:
			records = DownloadRecords()
		records.SetSavePath(jsonPath)
		return records

	def SaveToFile(self):
		path = self.savePath
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

	def AddRecord(self, uniqueID, downloaded, deadAsOf = None, quality = None, wasTooLong = None):
		self.records.append(Record(uniqueID, downloaded, deadAsOf, quality, wasTooLong))

	def MarkDownloaded(self, uniqueID, quality):
		record = self.GetRecord(uniqueID)
		record.downloaded = True
		record.quality = quality

	def MarkDead(self, uniqueID):
		record = self.GetRecord(uniqueID)
		if record.deadAsOf is None:
			record.deadAsOf = Timestamp()

	def MarkTooLong(self, uniqueID, lengthInSeconds):
		record = self.GetRecord(uniqueID)
		record.wasTooLong = lengthInSeconds

	def UnmarkTooLong(self, uniqueID):
		record = self.GetRecord(uniqueID)
		record.wasTooLong = None

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
		toFolder = config.GetInfoFolder()

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