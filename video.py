from nicovideo import Nicovideo
import nicovideo
import pafy

def IsYoutube(url):
	if (-1) != url.find('youtube.com/watch'):
		return True
	else:
		return False

def IsNicovideo(url):
	if (-1) != url.find('nicovideo.jp/watch/'):
		return True
	else:
		return False

def IsAliveYoutube(url):
	try:
		vid = pafy.new(url)
	except(OSError):
		return False
	return True

def IsAliveNico(url):
	pos = url.find('nicovideo.jp/watch/')
	url = url[pos+19:]
	nico = Nicovideo()
	try:
		nico.append(url)
	except(nicovideo.DeletedError):
		return False
	return True

class Video:
	UNKNOWN = 0
	YT = 1
	NICO = 2
	def __init__(self, url):
		self.url = url
		if IsYoutube(self.url):
			self.type = Video.YT
		elif IsNicovideo(self.url):
			self.type = Video.NICO
		else:
			self.type = Video.UNKNOWN

		self.__IsAlive = {Video.YT : IsAliveYoutube, Video.NICO : IsAliveNico, Video.UNKNOWN : lambda x:False}[self.type]
		self.isAlive = None

	def IsAlive(self):
		if self.isAlive is None:
			self.isAlive = self.__IsAlive(self.url)
		return self.isAlive