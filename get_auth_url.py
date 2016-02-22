#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 xym
#

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from app.wechat.wechat_api import auth_url

app_id = 'xxxx'

if __name__ == "__main__":
    print auth_url(app_id, "http://wechat.xxx.com/flow/index/", "test")
