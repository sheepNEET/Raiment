import os

import video
import bookmark
import data
import config

# load bookmarks from file
bookmarkBar = bookmark.GetTopFolder()
markedFolders = bookmarkBar.GetMarkedFolders()

# try to load records list from file
records = data.DownloadRecords.LoadOrCreate()

bookmarks = [link for marked in markedFolders for link in marked.childBookmarks]
for link in bookmarks:
	# time to stop downloading?
	if config.ShouldAbort():
		print('\nAborted')
		break

	# skip if not known video site
	vid = video.VideoFromURL(link.url)
	if vid.type == 'unsupported':
		continue

	# add to record list if not already there
	uniqueID = video.UniqueIDfromURL(link.url)
	if uniqueID is None:
		raise Exception('Unexpected None for uniqueID')
	if not records.HasRecord(uniqueID):
		records.AddRecord(uniqueID, downloaded=False)
		records.SaveToFile()

	# skip if already downloaded
	if records.GetRecord(uniqueID).downloaded:
		if records.GetRecord(uniqueID).VideoFileExists():
			continue
		else:
			print('Redownloading previously downloaded video (video was deleted?)')

	# mark dead if not alive
	if records.GetRecord(uniqueID).deadAsOf is not None:
		continue
	if not vid.IsAlive():
		records.MarkDead(uniqueID)
		records.SaveToFile()
		print('Skipping one (newly discovered dead)')
		continue

	# skip if Youtube video over 15 minutes
	if vid.type == 'youtube':
		wasTooLong = records.GetRecord(uniqueID).wasTooLong
		if wasTooLong is not None:
			if wasTooLong > config.GetMaxYoutubeLength():
				continue
			else:
				records.UnmarkTooLong(uniqueID)
		if vid.GetLength() > config.GetMaxYoutubeLength():
			records.MarkTooLong(uniqueID, vid.GetLength())
			print('Skipping "{0}" (too long)'.format(uniqueID))
			continue

	# download the video
	print('\nNow downloading "' + uniqueID + '"')
	quality = vid.DownloadVideo()
	if quality is None:
		print('Failed to download ' + uniqueID)
		continue

	# put metadata to file, download thumbnail to file
	info = data.VideoInfo(uniqueID, *vid.TextInfo())
	info.SaveToFile()
	vid.DownloadThumbnail()

	# set downloaded = True in record list
	records.MarkDownloaded(uniqueID, quality)

	# save record list to file
	records.SaveToFile()
	print('Downloaded "' + uniqueID + '"')