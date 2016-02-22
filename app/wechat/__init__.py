#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#
from flask import Blueprint

wechat = Blueprint('wechat', __name__)

from . import views
