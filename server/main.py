from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, StaticFileHandler
import tornado.web
import os
import random
random.seed()

import config

LISTEN_PORT = 8888
FILES_PATH = './files'

print('Serving from ' + config.GetVideoFolder())

videos = os.listdir(config.GetVideoFolder())
videos = list(filter(lambda x: True if x[-4:] == '.mp4' else False, videos))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/(.*\.mp4)", VideoHandler, {'path' : config.GetVideoFolder()}),
            (r"/(.*)", StaticFileHandler, {'path' : FILES_PATH})
        ]
        settings = {"template_path": FILES_PATH}
        tornado.web.Application.__init__(self, handlers, **settings)

class VideoHandler(StaticFileHandler):
	@classmethod
	def get_content(self, abspath, start=None, end=None):
		with open('data/log.txt', 'a') as f:
			f.write('Requested video ' + abspath + '\n')
		return super().get_content(abspath, start, end)

class MainHandler(RequestHandler):
	def get(self):
		self.render("index.html", VIDEO_FILENAME = random.choice(videos))
		# self.render("index.html", VIDEO_FILENAME = test)

class WebHandler(RequestHandler):
    def get(self, filename):
        self.render(filename)

def main():
    application = Application()
    application.listen(LISTEN_PORT)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()