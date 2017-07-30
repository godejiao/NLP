# -*- coding:utf-8 -*-
import urllib

LTPKEYLIST = [
    '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN',
]


class LtpNLP(object) :
    def __init__(self, ltp_key = '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN') :
        self._url_get_base = "http://api.ltp-cloud.com/analysis/"
        self.__api_key = ltp_key

    # 词性标注
    def wordPos(self, s) :
        args = {
            'api_key' : self.__api_key,
            'text' : s,
            'pattern' : 'pos',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        content = result.read().strip()
        return content

    # 分词
    def wordSeg(self, s) :
        args = {
            'api_key' : self.__api_key,
            'text' : s,
            'pattern' : 'srl',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        print result
        content = result.read().strip()
        return content

    # 命名实体识别
    def lexicalAnalysis(self, s) :
        args = {
            'api_key' : self.__api_key,  # '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN',
            'text' : s,
            'pattern' : 'ner',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        content = result.read().strip()
        return content

    # 语义依存分析
    def textDependency(self, s) :
        args = {
            'api_key' : self.__api_key,  # '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN',
            'text' : s,
            'pattern' : 'sdp',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        content = result.read().strip()
        return content

    # 依存句法分析
    def wordDependency(self, s) :
        args = {
            'api_key' : self.__api_key,  # '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN',
            'text' : s,
            'pattern' : 'dp',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        content = result.read().strip()
        return content

    # 语义角色标注
    def wordmark(self, s) :
        args = {
            'api_key' : self.__api_key,  # '89X001705x6XrXnRNYJzxnIFJvhw1MVsDRuJgahN',
            'text' : s,
            'pattern' : 'srl',
            'format' : 'plain'
        }
        result = urllib.urlopen(self._url_get_base, urllib.urlencode(args))  # POST method
        content = result.read().strip()
        return content


if __name__ == '__main__' :
    nlp = LtpNLP()
    s = '北京欢迎你'
    # print("词性标注结果")
    # print(nlp.cixing(s))
    # print("分词")
    # print(nlp.fenci(s))
    # print("命名实体识别")
    # print(nlp.lexicalAnalysis(s))
    # print("依存句法分析")
    # print(nlp.textDependency(s))
    print("语义依存分析")
    print(nlp.wordDependency(s))
    print("语义角色标注")
    print(nlp.wordmark(s).encode('UTF-8'))