import nicovideo as nicolib
import pafy

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

class UnsupportedVideo:
	def __init__(self, url):
		self.url = url
		self.type = 'unknown'
	def IsAlive(self):
		return False

class YoutubeVideo:
	def __init__(self, url):
		self.url = url
		self.vid = None
		self.type = 'youtube'

	def Initialize(self):
		if self.vid is not None:
			return True
		try:
			self.vid = pafy.new(self.url)
		except OSError:
			return False
		return True

	def IsAlive(self):
		if not self.Initialize():
			return False
		return True

	def UniqueID(self):
		if not self.Initialize():
			raise Exception()
		return 'youtube ' + self.vid.videoid

	def DownloadThumbnail(self):
		if not self.Initialize():
			raise Exception()
		url = self.vid.bigthumb
		if url == '':
			url = self.vid.thumb
		# TODO

	def TextInfo(self):
		if not self.Initialize():
			raise Exception()
		return (self.vid.title, self.username, self.vid.description)

class NicoVideo:
	def __init__(self, url):
		self.url = url
		self.vid = None
		self.type = 'nico'

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
		if not self.Initialize():
			raise Exception()
		return 'nico ' + self.vid.video_id

	def DownloadThumbnail(self):
		if not self.Initialize():
			raise Exception()
		url = self.vid.thumbnail_url
		# TODO

	def TextInfo(self):
		if not self.Initialize():
			raise Exception()
		return (self.vid.title, self.user_id, self.vid.description)

def VideoFromUrl(url):
	if __IsYoutube(url):
		return YoutubeVideo(url)
	elif __IsNicovideo(url):
		return NicoVideo(url)
	else:
		return UnsupportedVideo(url)