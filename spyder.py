# coding: utf-8
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import urllib, requests
import socket
import time, pickle
from metspy.config import Config
from metspy.initializer import Urlinit, Urloader

class Spyder(Config):
	"""
	Create a new spider
	"""
	def __init__(self, obj_path = "./static/urls.pkl"):
		super(Spyder, self).__init__()
		self.obj_path = obj_path

	def run(self, country_name = None):
		records = {}
		if not Path(self.obj_path).exists():
			init = Urlinit()
			init.run()
		else:
			loader = Urloader(self.obj_path)
			urls = loader.urls
		if country_name:
			for url in urls[country_name]:
				print(url)
				record = self.curt_scrape(url)
				records[url] = record

		else:
			for country, country_urls in urls.items():
				print(country)
				for url in country_urls:
					print(url)
					record = self.curt_scrape(url)
					records[url] = record
		return records

	def curt_scrape(self, url):
		record = {}
		request = urllib.request.Request(url, headers=self.header)
		try:
			response = urllib.request.urlopen(request)
			html = response.read().decode("utf-8")
			soup = BeautifulSoup(html, features="lxml")
			vals = soup.find_all("td", {"class": "tdcur"})
			for val in vals:
				record[val.get("id")] = val.get_text()
			now = datetime.now().strftime("%Y-%m-%d:%H")
			record["time"] = now
			response.close()
		except urllib.error.URLError as e:
			print(e.reason)

		time.sleep(1) # sleep time, it's for anti-anti-scraping
		return record