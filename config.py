import socket

class Config(object):
	"""
	Basic configuration, like socket default timeout, headers
	"""
	def __init__(self, timeout = 20):
		super(Config, self).__init__()
		self.timeout = timeout
		socket.setdefaulttimeout(self.timeout)  # set socket layer timeout as 20s
		self.header = {'User-Agent': 'Mozilla/5.0'}