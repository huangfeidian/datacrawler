# -*- coding: utf-8 -*-
from json import *
from datetime import datetime
class weibo:
	def __init__(self):
		self.datetime=None;
		self.timetext=None;
		self.id=None;
		self.text=None;
		slef.author=None;
	def __init__(self,dict_data):
		if(isinstance(dict_data["datetime"],datetime)):
			#这个dict里存的是datetime
			self.datetime=dict_data["datetime"];
			self.timetext=datetime.strftime(self.datetime,"%Y-%m-%d %H:%M:%S:");
		else:
			#这个dict里存的是string
			self.timetext=dict_data["datetime"];
			self.datetime=datetime.strptime(dict_data["datetime"],"%Y-%m-%d %H:%M:%S:");
		self.id=dict_data["id"];
		self.text=dict_data["text"];
		self.author=dict_data["author"];
	def get_json_dict(self):
		result={};
		result["datetime"]=self.timetext;
		result["id"]=self.id;
		result["text"]=self.text;
		result["author"]=self.author;
		return result;


