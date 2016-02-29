class weibo_user:
	def __init__(self):
		self.home=None;
		self.fan_number=0;
		self.fan_set=set();
		self.nick=None;
		self.fo_number=0;
		self.fo_set=set();
	def set_fo(self,in_fo_set):
		self.fo_set=in_fo_set;
		self.fo_number=len(self.fo_set);
	def set_fan(self,in_fan_set):
		self.fan_set=in_fan_set;
		self.fan_number=len(self.fan_set);
	def set_home(self,in_home):
		self.home=in_home;
	def set_nick(self,in_nick):
		self.nick=in_nick;
	def to_dict(self):
		result=dict();
		result["home"]=self.home;
		result["nick"]=self.nick;
		result["fo_num"]=self.fo_number;
		result["fan_num"]=self.fan_number;
		result["fo_list"]=list(self.fo_set);
		result["fan_list"]=list(self.fan_set);
		return result;


