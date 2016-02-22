#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 xym
#

"""
微信的一些api方法
"""

import urllib
import urllib2
import json

import requests
import collections


GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'

CREATE_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/menu/create'

DELETE_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delete'

GET_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/menu/get'

CREATE_CHN_QRCODE_URL = 'https://api.weixin.qq.com/cgi-bin/qrcode/create'


def post_json(url, data_map):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(req, json.dumps(data_map, ensure_ascii=False))
    return resp.read()


def get(url, data=None, user_agent=None):
    if data:
        encode_params = urllib.urlencode(data)
        url = url + "?" + encode_params

    request = urllib2.Request(url)
    if user_agent:
        request.add_header('User-Agent', user_agent)

    resp = urllib2.urlopen(request)
    return resp.read()


def get_access_token(app_id, app_secret):
    """
        获取凭证
        @see http://mp.weixin.qq.com/wiki/index.php?title=%E9%80%9A%E7%94%A8%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3
    """
    data = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret,
    }
    resp = get(GET_ACCESS_TOKEN_URL, data)
    return resp


def create_menu(menu_map, access_token):
    """
        创建菜单
    """

    url = CREATE_MENU_URL + '?access_token=%s' % access_token
    # resp = urllib2.urlopen(url, menu_json_str.encode('utf-8'))
    resp = post_json(url, menu_map)
    return resp


def delete_menu(access_token):
    """
        删除菜单，建议现考虑是否直接关闭开发者模式
    """
    url = DELETE_MENU_URL + '?access_token=%s' % access_token
    resp = post_json(url, None)
    return resp


def get_current_menu(access_token):
    """
        获取当前菜单配置
    """
    data = {
        'access_token': access_token,
    }
    resp = get(GET_MENU_URL, data)
    return resp


def create_chn_qrcode(scene_str, access_token):
    """
        创建渠道永久二维码, 需要订阅号才能使用
        scene_str: 渠道标识字符串
        @see http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html
    """
    url = CREATE_CHN_QRCODE_URL + '?access_token=%s' % access_token
    data = {
        "action_name": "QR_LIMIT_STR_SCENE",
        "action_info": {
            "scene": {
                "scene_str": scene_str
            }
        }
    }
    resp = post_json(url, data)
    return resp


def auth_url(appid, redirect_uri, state):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize"
    data = collections.OrderedDict()
    data['appid'] = appid
    data['redirect_uri'] = redirect_uri
    data['response_type'] = 'code'
    data['scope'] = 'snsapi_userinfo'
    data['state'] = state
    ans = "%s?%s%s" % (url, urllib.urlencode(data), "#wechat_redirect")
    return ans

def get_access_token_by_code(appid, secret, code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {
        'appid': appid,
        'secret': secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        return {'e': e.message}


def get_userinfo(access_token, openid):
    url = "https://api.weixin.qq.com/sns/userinfo"
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN',
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        return {'e': e.message}
