import os
import urllib.request
import time
import http

import nicovideo as nicolib
import pafy

CREDENTIALS_FILE = 'data/creds.txt'
VIDEO_FOLDER_FILE = 'data/video_folder.txt'
THUMB_FOLDER_FILE = 'data/thumb_folder.txt'

def DownloadFromURL(url, outputPath):
	response = urllib.request.urlopen(url)
	f = open(outputPath, 'wb')
	f.write(response.read())
	f.close()

def __IsYoutube(url):
	if (-1) != url.find('youtube.com/watch'):
		return True
	else:
		return False

def __IsNicovideo(url):
	if (-1) != url.find('nicovideo.jp/watch/'):
		return True
	else:
		return False

def UniqueIDfromURL(url):
	if (-1) != url.find('youtube.com/watch'):
		url = url[url.find('youtube.com/watch')+17:]
		pos = url.find('?v=')
		if pos != (-1):
			return 'youtube ' + url[pos+3:pos+3+11]
		pos = url.find('&v=')
		if pos != (-1):
			return 'youtube ' + url[pos+3:pos+3+11]
		raise Exception('Failed to get unique ID for Youtube video')
	elif (-1) != url.find('nicovideo.jp/watch/'):
		url = url[url.find('nicovideo.jp/watch/')+19:]
		pos = url.find('?')
		if pos != (-1):
			return 'nico ' + url[:pos]
		else:
			return 'nico ' + url
	else:
		return None

class UnsupportedVideo:
	def __init__(self, url):
		self.url = url
		self.type = 'unsupported'
	def IsAlive(self):
		return False

class YoutubeVideo:
	def __init__(self, url):
		self.url = url
		self.vid = None
		self.type = 'youtube'
		self.uniqueID = UniqueIDfromURL(self.url)

	def Initialize(self, attempt = 0):
		if self.vid is not None:
			return True
		try:
			self.vid = pafy.new(self.url)
		except OSError:
			return False
		except (ValueError, KeyError):
			time.sleep(2)
			if attempt < 5:
				print('Retrying Youtube video (attempt {0})'.format(attempt+1))
				self.Initialize(attempt + 1)
			else:
				raise Exception('Failed to open Youtube video')
		return True

	def IsAlive(self):
		if not self.Initialize():
			return False
		return True

	def UniqueID(self):
		return self.uniqueID

	def DownloadThumbnail(self):
		if not self.Initialize():
			raise Exception()
		url = self.vid.bigthumbhd
		if url == '':
			url = self.vid.bigthumb
		if url == '':
			url = self.vid.thumb

		f = open(THUMB_FOLDER_FILE, 'r')
		toFolder = f.read()
		f.close()
		path = toFolder + self.UniqueID() + '.jpg'

		DownloadFromURL(url, path)

	def TextInfo(self):
		if not self.Initialize():
			raise Exception()
		return (self.vid.title, self.vid.username, self.vid.description)

	def DownloadVideo(self):
		f = open(VIDEO_FOLDER_FILE, 'r')
		toFolder = f.read()
		f.close()
		path = toFolder + self.UniqueID()

		if not self.Initialize():
			raise Exception()

		stream = self.vid.getbest(preftype='mp4')
		quality = str(stream.dimensions[1]) + 'p'

		if os.path.exists(path + '.mp4'):
			if os.path.getsize(path + '.mp4') > 0:
				raise Exception('Youtube downloader: File already exists '+ self.vid.videoid)
		if os.path.exists(path + '.flv'):
			if os.path.getsize(path + '.flv') > 0:
				raise Exception('Youtube downloader: File already exists '+ self.vid.videoid)

		stream.download(path + '.' + stream.extension)

		return quality

	def IsAcceptableLength(self):
		if self.vid.length > (60 * 15):
			return False
		else:
			return True

class NicoVideo:
	def __init__(self, url):
		self.url = url
		self.vid = None
		self.type = 'nico'
		self.uniqueID = UniqueIDfromURL(self.url)

	def Initialize(self):
		if self.vid is not None:
			return True
		pos = self.url.find('nicovideo.jp/watch/')
		sm = self.url[pos+19:]
		try:
			self.vid = nicolib.Video(sm)
		except nicolib.DeletedError:
			return False
		return True

	def IsAlive(self):
		if not self.Initialize():
			return False
		return True

	def UniqueID(self):
		return self.uniqueID

	def DownloadThumbnail(self):
		if not self.Initialize():
			raise Exception()
		url = self.vid.thumbnail_url

		f = open(THUMB_FOLDER_FILE, 'r')
		toFolder = f.read()
		f.close()
		path = toFolder + self.UniqueID() + '.jpg'

		DownloadFromURL(url, path)

	def TextInfo(self):
		if not self.Initialize():
			raise Exception()
		return (self.vid.title, self.vid.user_id, self.vid.description)

	def DownloadVideo(self):
		f = open(VIDEO_FOLDER_FILE, 'r')
		toFolder = f.read()
		path = toFolder + self.UniqueID()
		f.close()

		if not self.Initialize():
			raise Exception()

		nico = nicolib.Nicovideo()
		f = open(CREDENTIALS_FILE, 'r')
		user, pw = f.read().split(' ')
		nico.login(user, pw)
		f.close()

		if os.path.exists(path + '.mp4'):
			if os.path.getsize(path + '.mp4') > 0:
				raise Exception('Nico downloader: File already exists '+ self.vid.video_id)
		if os.path.exists(path + '.flv'):
			if os.path.getsize(path + '.flv') > 0:
				raise Exception('Nico downloader: File already exists '+ self.vid.video_id)

		for tries in range(5):
			try:
				nico.getvideo(self.vid.video_id, path)
				break
			except http.client.IncompleteRead:
				if os.path.exists(path + '.mp4'):
					os.remove(path + '.mp4')
				if os.path.exists(path + '.flv'):
					os.remove(path + '.flv')
			if tries == 5:
				raise Exception('Failed to download video ' + self.UniqueID())

		quality = 'best'
		return quality

	def IsAcceptableLength(self):
		return True # all videos guaranteed <100MB anyways

def VideoFromURL(url):
	if __IsYoutube(url):
		return YoutubeVideo(url)
	elif __IsNicovideo(url):
		return NicoVideo(url)
	else:
		return UnsupportedVideo(url)