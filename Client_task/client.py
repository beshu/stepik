class Client:

	def __init__(self, host, port, timeout=None):
		self.host = host
		self.port = port
		self.timeout = timeout

	def put(self, metric_name, metric_value, timestamp):
		pass

	def get(self):
		pass

class ClientError:
	pass



