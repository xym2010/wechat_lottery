#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#

from flask import current_app, render_template, redirect, flash, request,\
    url_for, abort, make_response
from app.flow import flow
from app.flow.models import UserInfo
from app import db, csrf
from app.wechat.wechat_api import get_access_token_by_code,\
    get_userinfo, auth_url
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from datetime import datetime

import uuid
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
cookies_dump_time = 24 * 60 * 60
PHONE_PATTERN = re.compile(r'^1[0-9]{10}$')


@csrf.exempt
@flow.route('/flow/index/')
def flow_index():
    chn = request.args.get('chn', None)
    if current_app.config['OPEN_COUNT'] and chn:
        current_app.logger.info(
            'chn:%s, ip:%s, actions:index' % (chn, request.remote_addr)
        )

    cookie_key = request.cookies.get(current_app.config['COOKIE_NAME'])
    cookie_data = cookies_loads(cookie_key)
    uid = None
    if cookie_data:
        uid = cookie_data.get('uid', None)
        if uid:
            user_info = UserInfo.query.filter(UserInfo.uid == uid).first()
            if user_info:
                return redirect(
                    url_for('flow.click_get_flow', uid=uid, _external=True)
                )

    url = auth_url(
        current_app.config['APPID'],
        url_for('flow.flow_auth', _external=True),
        chn
    )
    return redirect(url)


@csrf.exempt
@flow.route('/flow/index/auth/')
def flow_auth():
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    chn = state
    if current_app.config['OPEN_COUNT'] and chn:
        current_app.logger.info('chn:%s, ip:%s, actions:auth' % (
            chn,
            request.remote_addr
        ))

    if not code:
        return "请授权"

    token_msg = get_access_token_by_code(
        current_app.config['APPID'],
        current_app.config['WECHAT_SECRET'],
        code
    )
    # current_app.logger.info(str(token_msg))
    if 'e' in token_msg:
        current_app.logger.info(token_msg['e'])
        return '服务器连接错误'

    if 'errmsg' in token_msg:
        current_app.logger.info(token_msg['errmsg'])
        return token_msg['errmsg']

    access_token = token_msg['access_token']
    openid = token_msg['openid']
    expires_in  = token_msg['expires_in']
    refresh_token = token_msg['refresh_token']
    scope = token_msg['scope']
    user_info = UserInfo.query.filter(UserInfo.openid == openid).first()
    uid = None
    if user_info:
        uid = user_info.uid
    else:
        userinfo_msg = get_userinfo(access_token, openid)
        if 'e' in userinfo_msg:
            current_app.logger.info(userinfo_msg['e'])
            return '服务器连接错误'

        if 'errmsg' in token_msg:
            current_app.logger.info(userinfo_msg['errmsg'])
            return userinfo_msg['errmsg']

        uid = str(uuid.uuid1()).replace('-', '')
        user_info = UserInfo()
        user_info.openid = userinfo_msg['openid']
        user_info.province = userinfo_msg['province']
        user_info.headimgurl = userinfo_msg['headimgurl']
        user_info.city = userinfo_msg['city']
        user_info.country = userinfo_msg['country']
        user_info.sex = userinfo_msg['sex']
        user_info.nickname = userinfo_msg['nickname']
        user_info.create_time = datetime.now()
        user_info.uid = uid
        user_info.mobile = 'o'
        db.session.add(user_info)
        db.session.commit()
    # current_app.logger.info(str(userinfo_msg))

    if uid:
        cookie_data = cookies_dumps({'uid': uid}, cookies_dump_time)
        response = make_response(redirect(url_for('flow.click_get_flow', uid=uid, _external=True)))
        response.set_cookie(
            current_app.config['COOKIE_NAME'],
            value=cookie_data,
            max_age=cookies_dump_time
        )
        return response
    else:
        return "授权失败，请重试!"


@csrf.exempt
@flow.route('/flow/index/click_get_flow/')
def click_get_flow():
    uid = request.args.get('uid')
    if uid:
        user_info = UserInfo.query.filter(UserInfo.uid == uid).first()
        if user_info:
            pass
        else:
            return '非授权用户'
    else:
        return '参数错误'

    return render_template('index_1.html', uid=uid)


@flow.route('/flow/index/mobile/', methods=['GET', 'POST'])
def get_mobile():
    if request.method == 'GET':
        uid = request.args.get('uid')
        if uid:
            user_info = UserInfo.query.filter(UserInfo.uid == uid).first()
            if user_info:
                if user_info.mobile == 'o':
                    return render_template('index_2.html', uid=uid)
                else:
                    flow = get_flow_ans(user_info.uid)
                    return render_template('index_3.html', flow=flow)
            else:
                abort(404)
        else:
            abort(404)
    elif request.method == 'POST':
        uid = request.form.get('uid')
        mobile = request.form.get('mobile')
        user = UserInfo.query.filter(UserInfo.uid == uid).first()
        if user:
            if user.mobile != 'o':
                # flash('已经填写过了手机')
                flow = get_flow_ans(user.uid)
                return render_template('index_3.html', flow=flow)
            else:
                if check_mobile(mobile):
                    user.mobile = mobile
                    db.session.add(user)
                    db.session.commit()
                    flow = get_flow_ans(user.uid)
                    return render_template('index_3.html', flow=flow)
                else:
                    flash("手机格式错误")
        else:
            return flash("非授权用户")

        return render_template('index_2.html', uid=uid)


def cookies_dumps(data, expires_in):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
    return s.dumps(data)


def cookies_loads(cookie):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(cookie)
        return data
    except:
        return None


def check_mobile(mobile):
    if mobile and PHONE_PATTERN.match(mobile):
        return True
    return False


def get_flow_ans(uid):
    # flow = get_rand_flow()
    return flow
