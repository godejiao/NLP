# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from api.baidu_api import BaiduNLP
from api.tencent_api import TencentNLP
from api.boson_api import BosonNLPAPI,BOKEYLIST
from api.ltp_api import LtpNLP
from api.snow_api import SnowNLPAPI

from nlp_api.forms import SearchForm, SearchKeyWordsFrom
import requests


class NLP (object):
    def __init__(self) :
        self._nlp_dict = {"tencent" : TencentNLP, "baidu" : BaiduNLP, "boson" : BosonNLPAPI, "ltp" : LtpNLP,'snow':SnowNLPAPI}

    def get_nlp(self, mode = str("boson"),idkey='') :
        return self._nlp_dict[mode](idkey)


# nlp=NLP()
# nlp_class = nlp.get_nlp(1)

# 分词和词性标注
@csrf_exempt
def lexicalAnalysis(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text', None).encode('utf-8')
            engine = request.POST.get('engine', None)
            type = request.POST.get('type', None)
            space_mode = int(request.POST.get('space_mode',int(0)))
            oo_level = int(request.POST.get('level',int(3)))
            t2s = int(request.POST.get('t2s',int(0)))
            special_char_conv = int(request.POST.get('special_char_conv',int(0)))
            message = str()
            if text and engine and type:
                nlp = NLP()
                if engine == 'tencent' :
                    data = nlp.get_nlp(engine).lexicalAnalysis(text, type)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'baidu' :
                    data = nlp.get_nlp(engine).lexicalAnalysis(text)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage :
                        try :
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).wordSeg(text,space_mode,oo_level,t2s,special_char_conv)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message :
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0
                elif engine == 'ltp' :
                    # seg=nlp.get_nlp(engine).wordSeg(text)
                    # pos=nlp.get_nlp(engine).wordPos(text)
                    result['data'] = u''  # {'seg':seg,'pos':pos}
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                elif engine == 'snow':
                    text = text.decode('utf-8')
                    result['data'] = ''
                    result['status'] = 4
                    result['message'] = u''
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'
            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else:
        result['status'] = 1
        result['message'] = u'请求失败'
    return HttpResponse(json.dumps(result))

# 命名实体识别
@csrf_exempt
def lexical(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text',None).encode('utf-8')
            engine = request.POST.get('engine',None)
            type = request.POST.get('type',None)
            sensitivity = request.POST.get('sensitivity',None)
            message = str()
            if text and engine and type:
                nlp = NLP()
                if engine == 'tencent' :
                    data = nlp.get_nlp("tencent").lexicalAnalysis(text, type)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'baidu' :
                    data = nlp.get_nlp("baidu").lexicalAnalysis(text)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage :
                        try :
                            print BOKEYLIST[0]
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).lexicalAnalysis(text,sensitivity = sensitivity)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message :
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0
                elif engine == 'ltp' :
                    # data=nlp.get_nlp("ltp").lexicalAnalysis(text)
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                elif engine == 'snow' :
                    text = text.decode('utf-8')
                    # data=nlp.get_nlp(engine).lexicalAnalysis(text)
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                else:
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'
            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else :
        result['message'] = u'请求失败'
        result['status'] = 1
    return HttpResponse(json.dumps(result))



# 关键词提取
@csrf_exempt
def textKeywords(request) :
    result = {}
    if request.method == "POST" :
        text = request.POST.get('text',None).encode('utf-8')#str
        engine = request.POST.get('engine',None).encode('utf-8')
        title = request.POST.get('title',None).encode('utf-8')
        channel = request.POST.get('channel',None)
        type = request.POST.get('type',None)
        top_k = request.POST.get('top_k',int(10))
        message = str()
        try :
            if text and engine and title and channel and type :
                nlp = NLP()
                if engine == 'tencent' :
                    data = nlp.get_nlp("tencent").textKeywords(title, text, channel)
                    result['data'] = str(data).encode('utf-8')
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'baidu' :

                    data = nlp.get_nlp("baidu").commentTag(text, int(type))
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                # elif engine == 'boson' :
                #     try:
                #         data = nlp.get_nlp("boson",BOKEYLIST[0]).textKeywords(text,top_k)
                #         result['data'] = data
                #     except Exception,e:
                #         message = str(e)
                #     limitmessage = 'HTTPError: 429 count limit exceeded'
                #     if message  == limitmessage :
                #         BOKEYLIST.append(BOKEYLIST.pop(0))
                #         data = nlp.get_nlp("boson", BOKEYLIST[0]).textKeywords(text,top_k)
                #         result['data'] = data
                #         result['status'] = 0
                #         result['message'] = u'获取成功'
                #
                # elif engine == 'boson2':
                #     try:
                #         data = nlp.get_nlp('boson',BOKEYLIST[0]).textKeywords(text,top_k)
                #         result['data'] = data
                #         print BOKEYLIST[0]
                #     finally:
                #         print BOKEYLIST[0]
                #         BOKEYLIST.append(BOKEYLIST.pop(0))
                #         data = nlp.get_nlp('boson',BOKEYLIST[0]).textKeywords(text,top_k)
                #         result['data'] = data
                #     result['message'] = u'获取成功'
                #     result['status'] = 0
                # elif engine == 'boson3':
                #     headers = {'X-Token' : BOKEYLIST[0]}
                #     RATE_LIMIT_URL = 'http://api.bosonnlp.com/application/rate_limit_status.json'
                #     limit_result = requests.get(RATE_LIMIT_URL, headers = headers).json()
                #     count_limit_remaining = limit_result['limits']['keywords']['count-limit-remaining']
                #
                #     if count_limit_remaining < 20 :
                #         BOKEYLIST.append(BOKEYLIST.pop(0))
                #
                #     data = nlp.get_nlp("boson", BOKEYLIST[0]).textKeywords(text,int(top_k))
                #
                #     result['data'] = data
                #     result['message'] = u'获取成功'
                #     result['status'] = 0

                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage:
                        try :
                            print BOKEYLIST[0]
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).textKeywords(text, top_k)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message:
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0

                elif engine == 'ltp' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4

                elif engine == 'snow':
                    text = text.decode('utf-8')
                    data = nlp.get_nlp(engine).textKeywords(text,int(top_k))
                    # data = [(b,a) for a, b in data]
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'
            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)+message
            result['status'] = 2
    else :
        result['message'] = u'请求失败'
        result['status'] = 1
    return HttpResponse(json.dumps(result))

# 情感分析
@csrf_exempt
def textSentiment(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text', None).encode('utf-8')
            engine = request.POST.get('engine', None)
            type = request.POST.get('type', None)
            model = request.POST.get('model','general')
            message = str()
            if text and engine and type:
                nlp = NLP()
                if engine == 'tencent' :
                    data = nlp.get_nlp("tencent").textSentiment(text, type)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'baidu' :
                    data = nlp.get_nlp("baidu").textSentiment(text)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage :
                        try :
                            print BOKEYLIST[0]
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).textSentiment(text,model)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message :
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0
                elif engine == 'ltp' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                elif engine == 'snow':
                    text = text.decode('utf-8')
                    result['data'] = nlp.get_nlp('snow').textSentiment(text)
                    result['status'] = 0
                    result['message'] = u'获取成功'
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'
            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else:
        result['status'] = 1
        result['message'] = u'请求失败'
    return HttpResponse(json.dumps(result))

# 文本分类
@csrf_exempt
def textClassify(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text', None).encode('utf-8')
            engine = request.POST.get('engine', None)
            message = str()
            if text and engine :
                nlp = NLP()
                if engine == 'tencent' :
                    data = nlp.get_nlp(engine).textClassify(text)
                    result['data'] = data
                    result['message'] = u'获取成功'
                    result['status'] = 0
                elif engine == 'baidu' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage :
                        try :
                            print BOKEYLIST[0]
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).textClassify(text)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message :
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0
                elif engine == 'ltp' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 4
                elif engine == "snow":
                    text = text.decode('utf-8')
                    result['data'] = ''
                    result['status'] =4
                    result['message'] = u''
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'
            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else:
        result['status'] = 1
        result['message'] = u'请求失败'
    return HttpResponse(json.dumps(result))


# 句法分析
@csrf_exempt
def textDependency(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text', None).encode('utf-8')
            engine = request.POST.get('engine', None)
            message = str()
            if text and engine :
                nlp = NLP()
                if engine == 'tencent' :
                    # data=nlp.get_nlp(engine).textDependency(text)
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 1
                elif engine == 'baidu' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 0
                elif engine == 'boson' :
                    message = limitmessage = 'HTTPError: 429 count limit exceeded'
                    while message == limitmessage :
                        try :
                            print BOKEYLIST[0]
                            data = nlp.get_nlp("boson", BOKEYLIST[0]).textDependency(text)
                            result['data'] = data
                            result['status'] = 0
                            result['message'] = u'获取成功'
                            message = ''
                        except Exception, e :
                            message = str(e)
                            if message == limitmessage :
                                BOKEYLIST.append(BOKEYLIST.pop(0))
                            elif message :
                                result['message'] = message
                                result['status'] = 6
                                result['data'] = 0
                elif engine == 'ltp' :
                    # data=nlp.get_nlp(engine).textDependency(text)
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 1
                elif engine == "snow" :
                    text = text.decode('utf-8')
                    result['data'] = ''
                    result['status'] = 4
                    result['message'] = u''
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'

            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else :
        result['status'] = 1
        result['message'] = u'请求失败'
    return HttpResponse(json.dumps(result))


# 文本摘要
@csrf_exempt
def textSummary(request) :
    result = {}
    if request.method == "POST" :
        try :
            text = request.POST.get('text', None).encode('utf-8')#str
            engine = request.POST.get('engine', None)
            limit_of_boson = float(request.POST.get('limit_of_boson',float(0.3)))
            limit_of_snow = int(request.POST.get('limit_of_snow',int(5)))
            message = str()
            if text and engine :
                nlp = NLP()
                if engine == 'tencent' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 1
                elif engine == 'baidu' :
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 0
                elif engine == 'boson' :
                    if limit_of_boson <= 1.0 and limit_of_boson > 0.0:
                        message = limitmessage = 'HTTPError: 429 count limit exceeded'
                        text = text.decode('utf-8')
                        while message == limitmessage :
                            try :
                                data = nlp.get_nlp("boson", BOKEYLIST[0]).textSummary(s = text, limit = limit_of_boson)
                                result['data'] = data
                                result['status'] = 0
                                result['message'] = u'获取成功'
                                message = ''
                            except Exception, e :
                                message = str(e)
                                if message == limitmessage :
                                    BOKEYLIST.append(BOKEYLIST.pop(0))
                                elif message :
                                    result['message'] = message
                                    result['status'] = 6
                                    result['data'] = 0
                    else:
                        result['status'] = 7
                        result['message'] = u'limit不符合要求'
                        result['data'] = ''
                elif engine == 'ltp' :
                    # data=nlp.get_nlp(engine).textDependency(text)
                    result['data'] = u''
                    result['message'] = u'暂未开通'
                    result['status'] = 1
                elif engine == "snow" :
                    text = text.decode('utf-8')
                    data = nlp.get_nlp(engine).textSummary(text,limit_of_snow)
                    result['data'] = data
                    result['status'] = 0
                    result['message'] = u'获取成功'
                else :
                    result['data'] = ''
                    result['status'] = 5
                    result['message'] = u'引擎请求错误'

            else :
                result['data'] = ''
                result['message'] = u'获取失败'
                result['status'] = 3
        except Exception, e :
            result['data'] = ""
            result['message'] = str(e)
            result['status'] = 2
    else :
        result['status'] = 1
        result['message'] = u'请求失败'
    return HttpResponse(json.dumps(result))