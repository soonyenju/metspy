from metspy.initializer import Text2pkl
from metspy.spyder import Spyder
from metspy.processor import Dumper
from datetime import *
from pathlib import Path


class Dispatcher(object):
	"""docstring for Dispatcher"""
	def __init__(self, start_hour):
		super(Dispatcher, self).__init__()
		self.start_hour = start_hour
		static_path = Path("./static")
		record_path = Path("./records")
		userurl_path = Path("./static/user_url.txt")
		if not static_path.exists():
			static_path.mkdir()
		if not record_path.exists():
			record_path.mkdir()
		if not userurl_path.exists():
			userurl_path.write_text("")

	def cust_run(self, cust_path):
		"""
		user define user_url.txt
		"""
		t2p = Text2pkl(out_path = cust_path)
		urls_path = cust_path
		self.monitor(self.runTask, urls_path = urls_path, hour = self.start_hour)

	def deft_run(self, country_name = None):
		"""
		default worldwide scraping
		"""
		self.monitor(self.runTask, hour = self.start_hour, country_name = country_name)

	def monitor(self, func, urls_path = "./static/urls.pkl", hour = "0", country_name = None):
		# watch per hour
		period = timedelta(days = 0, hours = 1, minutes = 0, seconds = 0)
		run_time = datetime.strftime(datetime.now(), "%Y-%m-%d:")
		run_time = datetime.strptime(run_time + hour, "%Y-%m-%d:%H")
		now = datetime.now()
		print("start run at " + datetime.strftime(run_time, "%Y-%m-%d %H:%M"))
		while True:
			if datetime.strftime(now, "%Y-%m-%d:%H") == datetime.strftime(run_time, "%Y-%m-%d:%H"):
				func(urls_path, country_name = country_name)
				run_time = run_time + period
				print("next run at " + datetime.strftime(run_time, "%Y-%m-%d %H:%M"))

	def runTask(self, urls_path, country_name = None):
		spyder = Spyder(urls_path) 
		if country_name:
			records = spyder.run(country_name = country_name)
		else:
			records = spyder.run()
		dumper = Dumper(records)
		if not Path(dumper.template_path).exists():
			dumper.init_template()
		dumper.dump()

if __name__ == '__main__':
	main()