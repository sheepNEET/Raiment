import video
import bookmark

bookmarkBar = bookmark.GetTopFolder('data/asd.bak')

markedFolders = bookmarkBar.GetMarkedFolders()

def Process(folder):
	q = 0
	supportedCount = 0
	for link in folder.childBookmarks:
		vid = video.VideoFromUrl(link.url)
		if vid.type != 'unknown':
			supportedCount += 1
			aliveStr = 'ALIVE'
			if not vid.IsAlive():
				aliveStr = 'DEAD'
			print(link.url, ' --- ', aliveStr)
		else:
			print(link.url, ' --- ', '***UNSUPPORTED***')
		q += 1
		if q > 50:
			break
	print(supportedCount)

Process(markedFolders[0])