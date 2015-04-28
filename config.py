# All file path-related stuff is in here

def ShouldAbort():
	f = open(ABORT_FILE_PATH, 'r')
	abort = len(f.read()) > 0
	f.close()
	return abort

def GetNicoCredentials():
	f = open(NICO_LOGIN_FILE_PATH)
	user, pw = f.read().strip().split(' ')
	f.close()
	return user, pw

def GetVideoFolder():
	return STORAGE_FOLDER_PATH + 'video/'

def GetThumbnailFolder():
	return STORAGE_FOLDER_PATH + 'thumbnail/'

def GetInfoFolder():
	return STORAGE_FOLDER_PATH + 'video-info/'

def GetDownloadRecordPath():
	return RECORD_LIST_FILE_PATH

f = open('data/StorageFolderPath.txt', 'r')
STORAGE_FOLDER_PATH = f.read()
f.close()

ABORT_FILE_PATH = 'data/Abort.txt'

NICO_LOGIN_FILE_PATH = 'data/creds.txt'

RECORD_LIST_FILE_PATH = 'data/DownloadRecords.txt'