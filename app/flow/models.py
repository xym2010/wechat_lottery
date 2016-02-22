#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#
from app import db


class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), index=True, unique=True)  # 用户openid
    province = db.Column(db.String(512))  # 省份
    headimgurl = db.Column(db.String(512))  # 头像url
    city = db.Column(db.String(512))  # 城市
    country = db.Column(db.String(512))  # 国家
    sex = db.Column(db.Integer)  # 性别
    nickname = db.Column(db.String(512))  # 昵称
    create_time = db.Column(db.DateTime)  # 创建时间
    uid = db.Column(db.String(36), index=True, unique=True)  # 用户标识
    mobile = db.Column(db.String(11), index=True)  # 手机


class ApplyFlowRecord(db.Model):
    __tablename__ = 'apply_flow_record'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), index=True, unique=True)  # 用户标识
    flow_id = db.Column(db.Integer)  # 流量对应id，没有的话为0
    status = db.Column(db.Integer)  # 状态
    create_time = db.Column(db.DateTime)  # 创建时间


class FlowLib(db.Model):
    __tablename__ = 'flow_lib'
    id = db.Column(db.Integer, primary_key=True)
    flow = db.Column(db.Integer)  # 流量
    status = db.Column(db.Integer)  # 状态 0 未领取, 1领取
