# -*- coding: utf-8 -*-
from crawler_mgr import crawler_mgr;
crawler_instance=crawler_mgr();
crawler_instance.set_proxy("proxies.json");
crawler_instance.set_cookie("cookies.json");
crawler_instance.set_email("email_config.json")
crawler_instance.set_worker_list("worker_name_list.json");

crawler_instance.run();