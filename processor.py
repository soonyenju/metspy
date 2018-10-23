from pathlib import Path
import pickle
import pandas as pd
# import pymongo

class Dumper(object):
	"""docstring for Dumper"""
	def __init__(self, records, path = "./records", template_path = "./static/record_template.pkl"):
		super(Dumper, self).__init__()
		self.records = records
		self.saveparpath = Path(path)
		self.template_path = template_path

	def init_template(self):
		record_template = {
			"time"    : [],
			"cur_pm25": [],
			"cur_pm10": [],
			"cur_o3"  : [],
			"cur_no2" : [],
			"cur_so2" : [],
			"cur_co"  : [],
			"cur_t"   : [],
			"cur_p"   : [],
			"cur_h"   : [],
			"cur_r"   : [],
			"cur_w"   : []
		}
		with open(self.template_path, "wb+") as f:
			pickle.dump(record_template, f)

	def dump(self):
		with open(self.template_path, "rb+") as f:
			record_template = pickle.load(f)
		for label, record in self.records.items():
			label = label.split("/")
			code_name = "_".join(label[-3:-1])
			savepath = self.saveparpath.joinpath(code_name + ".csv")#.as_posix()
			self.detect_template(record_template, record)
			for key in record_template.keys():
				if key in record.keys():
					record_template[key].append(record[key])
				else:
					record_template[key].append("-")
			if savepath.exists():
				df = pd.read_csv(savepath.as_posix())
				df_new = pd.DataFrame.from_dict(record_template, orient="columns")
				df = pd.concat([df, df_new]).set_index("time")
			else:
				df = pd.DataFrame.from_dict(record_template, orient="columns").set_index("time")

			df.to_csv(savepath.as_posix())

	def detect_template(self, record_template, record):
		# record_template = deepcopy(template)
		for key in record_template.keys():
			record_template[key] = []
		for key in record.keys():
			if key not in record_template.keys():
				record_template[key] = []
				with open(self.template_path, "wb+") as f:
					pickle.dump(record_template, f)
		