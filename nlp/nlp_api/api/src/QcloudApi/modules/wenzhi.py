#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import Base
from pprint import pprint

class Wenzhi(Base):
    requestHost = 'wenzhi.api.qcloud.com'
'''
action = 'TextKeywords'
config = {
    'Region': 'bj',
    'secretId': 'AKIDRnyynd3n6UvRl3GJApIarFZivCRf6gU7',
    'secretKey': 'eGE3gYKwOgokYL7nIbG7wdBVhiYCi4Pj',
    'method': 'get'
    }
params = {
    "title" : "Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330",
    "content" : "Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330"
 }
service = Wenzhi(config)
result=service.call(action, params)
re={"u'tags'":result}
pprint(re)

'''