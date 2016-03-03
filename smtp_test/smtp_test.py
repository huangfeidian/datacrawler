# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import requests
smtp163=smtplib.SMTP();
smtp163.connect("smtp.163.com","25");
from_addr="boysenberryeater@163.com";
passwd="python314159"
to_addr="pineberryeater@163.com";
smtp163.login(from_addr,passwd);
response=requests.get("http://www.baidu.com");
attachment1=MIMEText(response.text,"base64","utf-8");
attachment1["Content-Type"]="application/octet-stream";
attachment1["Content-Disposition"]="attachment; filename=\"baidutext.xml\"" 
attachment2=MIMEText(response.content,"base64","utf-8");
attachment2["Content-Type"]="application/octet-stream";
attachment2["Content-Disposition"]="attachment; filename=\"baiducontent.xml\"" 
msg=MIMEMultipart();
msg["From"]=from_addr;
msg["To"]=to_addr;
msg["Subject"]="request attachment test ";
msg.attach(MIMEText("test only"));
msg.attach(attachment1);
msg.attach(attachment2);
smtp163.sendmail(from_addr,to_addr,msg.as_string());
smtp163.close()