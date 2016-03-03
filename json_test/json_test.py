import codecs
import json


def main():
	input_file=codecs.open("weibo_test.json","r","utf-8");
	total_data_list=input_file.readlines();
	output_file=codecs.open("weibo_out.json","w","utf-8");
	for i in total_data_list:
		output_file.write(i.decode("unicode-escape")+"\n");

	#json_value=json.loads(total_data_list[0]);
	#print json_value;
main()
