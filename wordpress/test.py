from wordpress import wordpress
def test():
    log=wordpress();
    log.set_blog("http://weibocrawler.azurewebsites.net/","weibocrawler","1031Aa1010");
    log.login();
    title="hello test";
    text_body="hello world";
    log.post(title,text_body);

if __name__=="__main__":
    test();