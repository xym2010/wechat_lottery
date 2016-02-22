#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# Last modified: 2016-02-06 23:06:17

from flask import current_app, request, Response

from app.wechat import wechat
from app.wechat.service import check_sign, smart_str,\
    parse_msg_xml, get_reply_xml, get_news_reply_xml
from app import csrf
import sys
reload(sys)
sys.setdefaultencoding('utf8')


@csrf.exempt
@wechat.route('/test/', methods=['GET', 'POST'])
def test():
    return "test success"

@csrf.exempt
@wechat.route('/wechat/', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', None)
    timestamp = request.args.get('timestamp', None)
    nonce = request.args.get('nonce', None)
    echostr = request.args.get('echostr', None)
    current_app.logger.info("signature=%s timestamp=%s nonce=%s echostr=%s"
                            % (signature, timestamp, nonce, echostr))

    if request.method == 'POST':
        resp = ''
        if not check_sign(
                current_app.config['TOKEN'],
                signature,
                timestamp,
                nonce):
            return Response(resp, content_type='text/plain')

        raw_str = smart_str(request.data)
        msg = parse_msg_xml(raw_str)
        current_app.logger.info(str(msg))
        reply = None
        msg_type = msg.get('MsgType', None)
        open_id = msg.get('FromUserName', None)
        if msg_type == 'event':
            event = msg.get('Event', '')
            event_key = msg.get('EventKey', '')
            resp_content = "找不到你要的答案"
            if event == 'subscribe':
                # 关注
                resp_content = "感谢你的关注!\n 回复'抽奖'可以获得一次抽奖机会哦"
            elif event == 'unsubscribe':
                # 取消关注
                pass
            elif event == 'CLICK':
                # event_key
                if event_key == "KEY_GET_GAME":
                    reply = get_reply_by_content(msg, "抽奖", open_id)

            if not reply:
                reply = get_reply_xml(msg, resp_content)

        elif msg_type == 'text':
            # 文字信息
            content = msg.get('Content', None)
            resp_content = "无效回复"
            if content:
                content = content.strip()
                # auto_reply = load_auto_reply(game_id, content, deleted=0)
                # if not auto_reply:
                # # 如果不能处理用户指令，则回复默认回复
                #     tips_qs = load_auto_reply(game_id, 'sys:reply', deleted=2)
                #     if tips_qs:
                #         auto_reply = tips_qs
                reply = get_reply_by_content(msg, content, open_id)

            if resp_content and not reply:
                reply = get_reply_xml(msg, resp_content)

        if not reply:
            return Response("")

        return Response(reply, content_type='application/xml')

    elif request.method == 'GET':
        # 接受微信验证请求
        resp = ''
        if check_sign(current_app.config['TOKEN'], signature, timestamp, nonce):
            resp = echostr
            return Response(resp, content_type='text/plain')

    return Response("")


def get_reply_by_content(msg, content, open_id):
    current_app.logger.info("content = %s  open_id = %s" % (content, open_id))
    reply = None
    if content == '抽奖':
        url = "http://xxx.com/xxx"
        # 验证链接格式：url?uid=xxx
        # 获取唯一标志
        item = {
            'title': '测试测试',
            'description': "test",
            'pic_url': "http://xxx.png",
            'url': url
        }
        items = []
        items.append(item)
        reply = get_news_reply_xml(msg, items)

    return reply
