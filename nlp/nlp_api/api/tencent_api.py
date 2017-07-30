#!/usr/bin/python
# -*- coding: utf-8 -*-
#from __future__ import print_function
from pprint import pprint
from src.QcloudApi.modules.wenzhi import Wenzhi
from decimal import *
class TencentNLP:
    def __init__(self,tencent_key = {}):
        self.config = {
            'Region': 'bj',
            'secretId': 'AKIDRnyynd3n6UvRl3GJApIarFZivCRf6gU7',
            'secretKey': 'eGE3gYKwOgokYL7nIbG7wdBVhiYCi4Pj',
            'method': 'post'
        }
        self.tencentNlp=Wenzhi(self.config)

    '''--------分词&命名实体识别--------'''
    def lexicalAnalysis(self,text,type=0):
        action = 'LexicalAnalysis'
        params = {
            "text": text,
            "type": type,
            "code": 0x00200000
        }
        resultStr=self.tencentNlp.call(action, params)
        resultStr=resultStr.replace("[null]","\"\"")
        result=eval(resultStr)
        tokens=result["tokens"]
        length=len(tokens)
        validComment=[]
        validTokens=[]
        for i in range(length):
            token=tokens[i]
            pos=token["pos"]
            wlen=token["wlen"]
            word=token["word"].decode("unicode_escape")
            wtype=token["wtype"].decode("unicode_escape")
            wtype_pos=token["wtype_pos"]
            temp={'pos': pos,
             'wlen': wlen,
             'word': word,
             'wtype': wtype,
             'wtype_pos': wtype_pos}
            validTokens.append(temp)
        if length==0:
            validComment.append({'tokens':"null"})
        else:
            validComment.append({'tokens':validTokens})
        combtokens=result['combtokens']
        lengthOfCombTokens=len(combtokens)
        validCombTokens=[]
        for k in range(lengthOfCombTokens):
            combtoken=combtokens[k]
            cls=combtoken["cls"].decode('unicode_escape')
            pos=combtoken["pos"]
            wlem=combtoken["wlen"]
            word=combtoken["word"].decode('unicode_escape')
            temp={"cls":cls,"pos":pos,"wlen":wlen,"word":word}
            validCombTokens.append(temp)
        if lengthOfCombTokens==0:
            validComment.append({'combtokens':"null"})
        else:
            validComment.append({'combtokens':validCombTokens})
        return validComment

    '''-----------情感分析--------------'''
    def textSentiment(self,content,type=4):
        action = 'TextSentiment'
        params = {
            "content": content,
            "type":type
        }
        result=eval(self.tencentNlp.call(action, params))
        if result['message']=='':
            positive_ori=float(result['positive'])
            positive=float(Decimal.from_float(positive_ori).quantize(Decimal('0.0000000000000000')))
            negative_ori=1-positive
            negative=round(negative_ori,16)
            validComment={"positive":positive,"negative":negative}
            return validComment
        else:
            message=result['message'].decode('unicode_escape')
            return {"message": message}

    '''-----------关键词提取------------'''
    def textKeywords(self,title,content,channle='CHnews_news_cul'):
        action = 'TextKeywords'
        params = {
             "title" : title,
             "content" : content
        }
        resultStr=self.tencentNlp.call(action, params)
        if (resultStr.find("\"keywords\":[null]"))==-1:
            result = eval(self.tencentNlp.call(action, params))
            if result['code'] == 0:
                commentTags = result['keywords']
                length=len(commentTags)
                validComment=[]
                for i in range(length):
                    keyword=commentTags[i]['keyword'].decode('unicode_escape')
                    score_ori=commentTags[i]['score']
                    score = float(Decimal.from_float(score_ori).quantize(Decimal('0.0000')))
                    type = commentTags[i]['type']
                    tempComement={'keyword':keyword,'score':score,'type':type}
                    validComment.append(tempComement)
            return validComment
        else:
            return -1

    '''-----------同义词------------'''
    def  lexicalSynonym(self,text):
        action = 'LexicalSynonym'
        params={
             "text":text
        }
        resultStr = self.tencentNlp.call(action, params)
        if (resultStr.find("\"syns\":null")) == -1:
            #result=self.tencentNlp.call(action, params)
            resultStr=resultStr.replace("\"query\":null,","")
            result=eval(resultStr)
            # pprint(result)
            syns=result['syns']
            length=len(syns)
            validComment=[]
            for i in range(length):
                validSyns=[]
                synonymList=syns[i]
                word_ori=synonymList['word_ori']["text"].decode('unicode_escape')
                wordSynonyms=synonymList["word_syns"]
                lengthOfWordSyns=len(wordSynonyms)
                validSyns.append({"word_ori":word_ori})
                for j in range(lengthOfWordSyns):
                    synonym = wordSynonyms[j]['text'].decode('unicode_escape')
                    conf_ori=wordSynonyms[j]['conf']
                    conf=float(Decimal.from_float(conf_ori).quantize(Decimal('0.0000')))
                    temp={'text':synonym,'conf':conf}
                    validSyns.append(temp)
                validComment.append(validSyns)
            return  validComment
        else:
            return -1

    '''-----------文本分类------------'''
    def textClassify(self,content,title='',secd_nav='',url=''):
        action = 'TextClassify'
        params = {
            "title" : title,
            "content" : content,
            "secd_nav" : secd_nav,
            "url" : url
        }
        result=eval(self.tencentNlp.call(action, params))
        comment=result['classes']
        length=len(comment)
        validComment=[]
        conf_sum=0
        for i in range(length):
            _class=comment[i]['class'].decode('unicode_escape')
            _class_num=comment[i]['class_num']
            conf_ori=comment[i]['conf']
            conf = float(Decimal.from_float(conf_ori).quantize(Decimal('0.0000')))
            temp={'class':_class,'class_num':_class_num,'conf':conf}
            validComment.append(temp)
            conf_sum+=conf
        if conf_sum!=1:
            conf_sum-=validComment[length-1]["conf"]
            validComment[length-1]["conf"]=round((1-conf_sum),4)
        return validComment

    '''-----------词语纠错------------'''
    def lexicalCheck(self,text):
        action = 'LexicalCheck'
        params = {
            "text": text
        }
        result=eval(self.tencentNlp.call(action, params))
        text=result['text'].decode('unicode_escape')
        conf_ori=result['conf']
        conf = float(Decimal.from_float(conf_ori).quantize(Decimal('0.0000')))
        validComment=[{'text':text,'conf':conf}]
        return validComment

    '''-----------网页转码------------'''
    def contentTranscode(self,url,to_html):
        action = 'ContentTranscode'
        params = {
            "url": url,
            "to_html": to_html
        }
        return self.tencentNlp.call(action, params)

    '''-----------句法分析------------'''
    def textDependency(self,content):
        action = 'TextDependency'
        params = {
            "content": content
        }
        result=eval(self.tencentNlp.call(action, params))
        return self.tencentNlp.call(action, params)

    '''-----------敏感信息识别------------'''
    def textSensitivity(self,content,type):
        action = 'TextSensitivity'
        params = {
            "content": content,
            "type":type
        }
        result=eval(self.tencentNlp.call(action, params))
        if result['message'] == '':
            sensitive_ori=result['sensitive']
            sensitive=float(Decimal.from_float(sensitive_ori).quantize(Decimal('0.00')))
            nonsensitive_ori=1-sensitive
            nonsensitive=round(nonsensitive_ori,2)
            validComment={"code":result["code"],"codeDesc":result["codeDesc"],"nonsensitive":nonsensitive,"sensitive":sensitive}
            return validComment
        else:
            message = result['message'].decode('unicode_escape')
            return {"message": message}

# aip=TencentNLP();
# analysis=aip.lexicalAnalysis("Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数",1)
# pprint(analysis)

#keywords1=aip.testKeywords("Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330","Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330")
#keywords=aip.testKeywords("外套","Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330")
#pprint(keywords)

# sentiment=aip.testSentiment("林哲铭真蠢")
# sentiment2=aip.testSentiment("真好")
# sentiment3=aip.testSentiment("sss")
# pprint(sentiment)
# pprint(sentiment2)
# pprint(sentiment3)


# classfiy=aip.textClassify("腾讯入股京东")
# classfiy2=aip.textClassify("木烧烤")
# pprint(classfiy)
# pprint(classfiy2)
#print classfiy2.decode('unicode_escape')

#transcode=aip.contentTranscode("www.163.com",1)
#dependency=aip.textDependency("双万兆服务器就是好，只是内存小点")

#result={analysis,keywords,sentiment,synonym,classfiy}
#print result


# s=synonym1.decode('unicode_escape')

# synonym=aip.lexicalSynonym("周杰伦结婚")
# synonym1=aip.lexicalSynonym("大家都爱人民币")
# synonym2=aip.lexicalSynonym("人民币")
# pprint(synonym)
# pprint(synonym1)
# pprint(synonym2)
#print s

# check=aip.lexicalCheck("睡交吃饭")
# check1=aip.lexicalCheck("王把蛋真的是个累追")
# pprint(check)
# print(check1)
# #print  check1.decode('unicode_escape')

# sensitivity=aip.textSensitivity("六四事件是一个历史问题",2)
# sensitivity2=aip.textSensitivity("",2)
# sensitivity3=aip.textSensitivity("今天是个好日",2)
# pprint(sensitivity)
# pprint(sensitivity2)
# pprint(sensitivity3)
#print  sensitivity3.decode('unicode_escape')

