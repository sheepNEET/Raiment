def GetVideoFolder():
	return STORAGE_FOLDER_PATH + 'video/'

def GetThumbnailFolder():
	return STORAGE_FOLDER_PATH + 'thumbnail/'

def GetInfoFolder():
	return STORAGE_FOLDER_PATH + 'video-info/'

f = open('data/StorageFolderPath.txt', 'r')
STORAGE_FOLDER_PATH = f.read()
f.close()