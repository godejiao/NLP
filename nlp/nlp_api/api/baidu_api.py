# encoding: utf-8
from __future__ import print_function
from aip import AipNlp
from pprint import pprint
#APP_ID='9519234'
#API_KEY='CIwEvSR9m9hEWnQp2GK7LGKI'
#SECRET_KEY='s4hA4YTO1SjqIkRzTCT5uHSa715BKHFL'
#aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
class BaiduNLP:
    def __init__(self,baidu_key = {}):
        self.APP_ID='9519234'
        self.API_KEY='CIwEvSR9m9hEWnQp2GK7LGKI'
        self.SECRET_KEY='s4hA4YTO1SjqIkRzTCT5uHSa715BKHFL'
        self.baiduNlp=AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    # '''----------评论观点抽取,默认7教育-----------'''
    # def commenttag(self,words,type=7):
    #     comment=self.baiduNlp.commentTag(words,type)#返回处理
    #     commentTags=comment[u'tags']#得到评论观点，可能有多条评论观点
    #     length=len(commentTags)#得到有几个评论观点
    #     validComment = []
    #     for i in range(length):
    #         temp=commentTags[i]
    #         abstract=self.__deleteUnvalid(temp[u'abstract'])
    #         tempComement={u'abstract':abstract,u'adj':temp[u'adj'],u'fea':temp[u'fea'],u'type':temp[u'type']}
    #         validComment.append(tempComement)
    #     return validComment

    '''---------词法分析--------'''
    def lexicalAnalysis(self,text):
        return self.baiduNlp.lexer(text)

    '''---------依句法分析-------'''
    def textDependency(self,text):
        return self.baiduNlp.depParser(text)

    '''---------词向量表示-------'''
    def wordEmbedding(self,word):
        return self.baiduNlp.wordEmbedding(word)

    '''----------dnn语言模型-----------'''
    def dnnlm(self,words):
        return self.baiduNlp.dnnlm(words)

    '''----------词义相似度------------'''
    def wordSimEmbedding(self,word1,word2):
        return self.baiduNlp.wordSimEmbedding(word1,word2)

    '''----------短文相似度------------'''
    def simnet(self,text1,text2,):
        return self.baiduNlp.simnet(text1,text2)

    '''----------评论观点抽取------------'''
    def commentTag(self,text,type):
        return self.baiduNlp.commentTag(text,options={'type':type})

    '''----------情感分析------------'''
    def textSentiment(self,text):
        result = {}
        data = self.baiduNlp.sentimentClassify(text)
        positive = data['items'][0]['positive_prob']
        negative = data['items'][0]['negative_prob']
        result['positive'] = positive
        result['negative'] = negative
        return result


# aip=BaiduNLP()
# text=u"今天是个好日子，很适合出去游玩"
# text_list=[]
# a=u"我连上了飞机到了附近的搜房送到了分手的浪费就到了房间，速度发货款收到回复的回复可单独发几个房间，地方和东方红松"
# text_list.append(text)
# text_list.append(a)
# text_list.append(u"看电话覅是电话费等放款速度快的合法的历史考核方式和帕克；看过的介绍费老师；了；案例及方式方法可")
# result=[]
# for tx in text_list:
#     temp=aip.lexer(tx)
#     result.append(json.dumps(temp).decode("unicode_escape"))
#
# for res in result:
#     print (res)
#
# c=aip.wordseg(text)
# c=json.dumps(c).decode("unicode_escape")
# print(c)
#
# d=aip.textDependency(text)
# d=json.dumps(d).decode("unicode_escape")
# print(d)
#
# e=aip.wordEmbedding("李白")
# e=json.dumps(e).decode("unicode_escape")
# print (e)
#
# f=aip.dnnlm("床前明月光")
# f=json.dumps(f).decode("unicode_escape")
# print (f)

# g=aip.wordSimEmbedding("北京","上海")
# g=json.dumps(g).decode("unicode_escape")
# print (g)

#
# h=aip.commentTag("酒店设备齐全、干净卫生",1)
# h=json.dumps(h).decode("unicode_escape")
# print(h)

# i=aip.testSentiment("百度是一家伟大的公司")
# i=json.dumps(i).decode("unicode_escape")
# print (i)



