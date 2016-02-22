#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#

import hashlib
import time
import xml.etree.cElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def smart_str(s):
    from urllib import unquote
    return unquote(unicode(s).encode('UTF-8'))


def check_sign(token, sign, timestamp, nonce):
    """
        验证消息真实性
        @see http://mp.weixin.qq.com/wiki/index.php?title=%E9%AA%8C%E8%AF%81%E6%B6%88%E6%81%AF%E7%9C%9F%E5%AE%9E%E6%80%A7
    """
    if not sign or not timestamp or not nonce:
        return False

    params = [token, str(timestamp), nonce]
    params.sort()
    params_str = ''.join(params)
    server_sign = sha1(params_str)

    valid = False
    if server_sign == sign:
        valid = True
    return valid


def sha1(str):
    sha1 = hashlib.sha1()
    sha1.update(str)
    return sha1.hexdigest()


def md5(str):
    md5 = hashlib.md5()
    md5.update(str)
    return md5.hexdigest()


def parse_msg_xml(msg_xml):
    """
        微信文本消息
        @see http://mp.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E6%8E%A5%E5%8F%A3%E6%8C%87%E5%8D%97
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[key sklr100]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """
    root_elem = ET.fromstring(msg_xml)
    msg = {}
    if root_elem.tag == 'xml':
        for child in root_elem:
            msg[child.tag] = smart_str(child.text)
    return msg


def get_reply_xml(msg, reply_content):
    ext_tpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    ext_tpl = ext_tpl % (
        msg['FromUserName'],
        msg['ToUserName'],
        str(int(time.time())),
        'text',
        reply_content
    )
    return ext_tpl


def get_news_reply_xml(msg, items):
    """
        转换成图文消息的xml
    """
    ext_tpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><ArticleCount>%d</ArticleCount><Articles>%s</Articles><FuncFlag>0</FuncFlag></xml>"

    item_xml_tpl = '<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>'
    item_xml_list = []
    for item in items:
        item_xml = item_xml_tpl % (item['title'], item['description'], item['pic_url'], item['url'])
        item_xml_list.append(item_xml)

    items_xml = ''.join(item_xml_list)

    ext_tpl = ext_tpl % (
        msg['FromUserName'],
        msg['ToUserName'],
        str(int(time.time())),
        'news',
        len(items),
        items_xml
    )
    return ext_tpl
