import codecs
import json


def main():
	input_file=codecs.open("weibo_test.json","r","utf-8");
	total_data_list=input_file.readlines();
	print total_data_list;

	json_value=json.loads(total_data_list[0]);
	print json_value;
main()
