#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#
from flask import Blueprint

flow = Blueprint('flow', __name__)

from . import views
