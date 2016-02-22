#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 xym
#

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from app.wechat.wechat_api import get_access_token, create_menu, create_chn_qrcode
# from utils.youmi.devUserHelper import load_income

app_id = 'wx0b54143998697725'

app_secret = '88a22b0f9781f58aa28973207989c8a8'

btn_def = {
    "button": [
       {
            "name": "小马Club",
            "sub_button": [
                {
                    "type": "view",
                    "name": "小马商城",
                    "url": "http://wx.ponyrunning.com/web/ecshop/mobile/",
                },
                {
                    "type": "view",
                    "name": "小马聚会",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe6e1cc3fc75b5741&redirect_uri=http%3A%2F%2Fwx.ponyrunning.com%2Fweb%2Findex.php%3Fc%3DActivity%26a%3Dactivity_list&response_type=code&scope=snsapi_base&state=188&connect_redirect=1#wechat_redirect",
                },
                {
                    "type": "view",
                    "name": "小马热点",
                    "url": "http://eqxiu.com/s/ud7UILSt",
                },
                {
                    "type": "view",
                    "name": "小马社区",
                    "url": "http://xiaoqu.qq.com/mobile/barindex.html?ticket=&srctype=61&isappinstalled=0&g_f=5757&sid=&_wv=5123&_bid=128&#bid=266904&from=groupmessage",
                },
            ]
        },
        {
            "type": "view",
            "name": "小马上门",
            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe6e1cc3fc75b5741&redirect_uri=http%3A%2F%2Fwx.ponyrunning.com%2Fweb%2Findex.php&response_type=code&scope=snsapi_base&state=188&connect_redirect=1#wechat_redirect",
        },
        {
            "name": "Hi小马",
            "sub_button": [
                {
                    "type": "view",
                    "name": "帮助",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA5MzE2NzI0Mg==&mid=208262200&idx=1&sn=8dfd3e75d3dc22cb4ab4569c5714a268&scene=18#wechat_redirect",
                },
                {
                    "type": "view",
                    "name": "小马招募",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA5MzE2NzI0Mg==&mid=208301402&idx=1&sn=a33f9aa053f68ee7374e950fb0821d6f&scene=18#wechat_redirect",
                },
                {
                    "type": "view",
                    "name": "关于小马",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA5MzE2NzI0Mg==&mid=208277484&idx=1&sn=a7c92d99320b80ac36410ab415747a95&scene=18#wechat_redirect",
                },
                {
                    "type": "view",
                    "name": "打印照片",
                    "url": "http://lomoservices.lomopai.cn/ImageUpload.html?ghid=gh_ff2a629f0df1&uid=gh_ff2a629f0df1oknght6IU7tyEynsu1RuWd1ngCVo&lomoid=2458",
                },
                {
                    "type": "view",
                    "name": "在线客服",
                    "url": "http://downt.ntalker.com/t2d/chat.php?siteid=kf_9691&settingid=kf_9691_1448246542843&baseuri=http%3A%2F%2Fdl.ntalker.com%2Fjs%2Fxn6%2F&mobile=1&lan=&ref=weixin",
                },

            ]
        }
    ]
}


def send_create_menu():
    token_json = get_access_token(app_id, app_secret)
    token_dict = json.loads(token_json)
    print token_dict
    access_token = token_dict.get("access_token", None)

    # cur_menu_json_str = get_current_menu(access_token)
    # print cur_menu_json_str

    # print delete_menu(access_token)
    print create_menu(btn_def, access_token)


def send_create_chn_qrcode():

    print "创建渠道二维码"
    token_json = get_access_token(app_id, app_secret)
    token_dict = json.loads(token_json)
    print token_dict
    access_token = token_dict.get("access_token", None)

    chn_id_str = "weiyao1508"
    resp = create_chn_qrcode(chn_id_str, access_token)

    print resp
    resp_data = json.loads(resp)

    ticket = resp_data.get("ticket")

    qrcode_download_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ticket

    print qrcode_download_url

# 需要创建菜单，请打开下列代码
send_create_menu()

# 创建渠道二维码
# send_create_chn_qrcode()


"""
def test_load_income():
    uid = 6768,
    start_date = datetime.strptime('2013-10-01', '%Y-%m-%d')
    end_date = datetime.strptime('2013-10-07', '%Y-%m-%d')
    app_ids = None
    load_income(uid, start_date, end_date)
"""
