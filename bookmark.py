import json

# Make a bookmark with name = MARK_STRING and url = [anything]
# in each folder you want to download
MARK_STRING = 'DOWNLOADMARK*****'

class Bookmark:
	def __init__(self, urlDict):
		self.url = urlDict['url']
		self.name = urlDict['name']
		self.id = urlDict['id']

class Folder:
	def __init__(self, folderDict):
		self.name = folderDict['name']
		self.id = folderDict['id']
		self.childBookmarks = []
		self.childFolders = []
		self.marked = False
		childList = folderDict['children']
		for child in childList:
			if child['type'] == 'url':
				if child['name'] == MARK_STRING:
					self.marked = True
				else:
					self.childBookmarks.append(Bookmark(child))
			elif child['type'] == 'folder':
				self.childFolders.append(Folder(child))

	def PrintHierarchy(self, layerNum = 0):
		indent = '\t' * layerNum
		print(indent + self.name)
		for folder in self.childFolders:
			folder.PrintHierarchy(layerNum + 1)

	def GetMarkedFolders(self):
		folders = []
		for child in self.childFolders:
			folders += child.GetMarkedFolders()
		if self.marked:
			folders.append(self)
		return folders

# input: json file containing your bookmark info
# usually r"C:\Users\[username]\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
def GetTopFolder(jsonPath):
	f = open(jsonPath, 'rb')
	buf = f.read()
	buf = buf.decode('utf8')
	j = json.loads(buf)
	return Folder(j['roots']['bookmark_bar'])