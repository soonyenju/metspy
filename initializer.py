# coding: utf-8
from bs4 import BeautifulSoup
from pathlib import Path
from metspy.config import Config
import requests
import socket
import pickle

class Urlinit(Config):
	"""
	If there are no station urls .pkl exist, run this code to initialize it.
	"""
	# def __init__(self, timeout = 20):
	# 	super(Urlinit, self).__init__()
	# 	self.timeout = timeout
	# 	socket.setdefaulttimeout(self.timeout)  # set socket layer timeout as 20s
	# 	self.header = {'User-Agent': 'Mozilla/5.0'}
	def __init__(self):
		super(Urlinit, self).__init__()
		self.init_urls = ["http://aqicn.org/map/world/",
					"http://aqicn.org/map/world/cn/",
					"http://aqicn.org/map/world/cn/#@g/5.1993/8.6133/2z"]

	def run(self):
		for init_url in self.init_urls:
			"""
			Record url of each country and its provinces/major cities.
			"""
			try:
				res = requests.get(init_url, headers=self.header)
				html = res.text
				soup = BeautifulSoup(html, features='lxml')
				# print(type(soup))
				countries = soup.find_all("span", {"class": "country"})
				countries_url = {}
				for country in countries:
					# print(country)
					# print(dir(country))
					country_name = country.findChild().get_text().strip()
					country_href = country.findChild(name="a").get("href")
					countries_url[country_name] = {
						"province": {},
						"_country_url": country_href
						}
					provinces = country.find_all("a")
					for province in provinces:
						province_name = province.get_text().strip()
						province_href = province.get("href")
						if province_name != country_name: countries_url[country_name]["province"][province_name] = province_href
				break
			except Exception as e:
				print(e)
				continue

		with open("static/countries_url.pkl", "wb+") as f:
			pickle.dump(countries_url, f)

		urls = {}
		for country_name, country_item in countries_url.items():
			"""
			Record url of stations based on the countries_url dict saved previously.
			"""
			urls[country_name] = []
			# print(country_name, country_item["province"])
			print(country_name)
			for province_name, province_href in country_item["province"].items():
				# print(province_name.casefold(), province_href)
				res = requests.get(province_href, headers=self.header)
				html = res.text
				soup = BeautifulSoup(html, features='lxml')
				stations = soup.find_all("a")
				for station in stations:
					try:
						# if "aqicn.org/city/" + province_name.casefold() in station.get("href"):
						if "aqicn.org/city/" in station.get("href"):
							# print((station.get("href")))
							urls[country_name].append(station.get("href"))
					except Exception as e:
						# print(e)
						continue
			# print(urls)
			# exit(0)
		with open("static/urls.pkl", "wb+") as f:
			pickle.dump(urls, f)

class Urloader(object):
	"""
	If the urls exist, load them.
	"""
	def __init__(self, path = Path.cwd().joinpath("static/urls.pkl")):
		super(Urloader, self).__init__()
		self.path = path
		with open(self.path, "rb+") as f:
			self.urls = pickle.load(f)

class Text2pkl(object):
	"""
	docstring for Text2pkl
	"""
	def __init__(self, path = "./static/user_url.txt", label = "User_define", out_path = "./static/urls.pkl"):
		super(Text2pkl, self).__init__()
		self.path = path
		self.out_path = out_path
		with open(self.path, "rb") as f:
			urls = [line.strip().decode() for line in f.readlines()]
		self.user_def = {label: urls}
		self.dump()

	def dump(self):
		with open(self.out_path, "wb+") as f:
			pickle.dump(self.user_def, f)				