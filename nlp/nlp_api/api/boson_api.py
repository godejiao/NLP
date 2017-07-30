# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bosonnlp import BosonNLP
import datetime
BOKEYLIST = ['IKBIoANy.14545.A7GCYBnT9jIB',
             '5k4jMDos.16728.rCYPDpgFKl0j',
             'hKYYl2oa.16727.as96AqKfu_Wv',
             'KzCvp7Ik.16729.vNbR3f4IgKjD',
             'QPuUO2Hr.16819.jQvFFtl-h-dC',
             ]

class BosonNLPAPI:
    def __init__(self,bosonkey='IKBIoANy.14545.A7GCYBnT9jIB'):
        # self.bonlp = BosonNLP('IKBIoANy.14545.A7GCYBnT9jIB')
        self.bonlp = BosonNLP(bosonkey)
    #情感分析
    def textSentiment(self,s,model = 'general'):
        result={}
        data=self.bonlp.sentiment(s,model = model)
        # for i in range(len(data)) :
        #     result['the %s sentence' % (i + 1)] = {'positive' : data[i][0], 'negative' : data[i][1]}
        result['positive']=data[0][0]
        result['negative']=data[0][1]
        return result
    #命名实体识别
    def lexicalAnalysis(self,s,sensitivity=None):
        result=self.bonlp.ner(s,sensitivity = sensitivity)
        # :param
        # sensitivity : 准确率与召回率之间的平衡，
        # 设置成
        # 1
        # 能找到更多的实体，设置成
        # 5
        # 能以更高的精度寻找实体。
        # :type
        # sensitivity : int
        # 默认为
        # 3
        return result
    #依存文法分析
    def textDependency(self,s):
        result = self.bonlp.depparser(s)
        return result
    #关键词提取
    def textKeywords(self,s,top_k=10):
        result = self.bonlp.extract_keywords(s, top_k=top_k)
        return result
    #新闻分类
    def textClassify(self,s):
        resultlist=self.bonlp.classify(s)
        classifys={0:'体育',1:'教育',2:'财经',3:'社会',4:'娱乐',5:'军事',6:'国内',7:'科技',8:'互联网',9:'房产',10:'国际',11:'女人',12:'汽车',13:'游戏'}
        return(classifys[resultlist[0]])
    #语义联想
    def lexicalSynonym(self,term):
        result=self.bonlp.suggest(term, top_k=10)
        return result
    #分词与词性标注
    def wordSeg(self,s,space_mode= 0,oo_level = 3,t2s = 0, special_char_conv = 0):
        result = self.bonlp.tag(contents = s,space_mode = space_mode,oov_level = oo_level,t2s = t2s,special_char_conv = special_char_conv)

        # def tag(self, contents, space_mode = 0, oov_level = 3, t2s = 0, special_char_conv = 0) :
        # """BosonNLP `分词与词性标注 <http://docs.bosonnlp.com/tag.html>`_ 封装。
        #
        #        :param contents: 需要做分词与词性标注的文本或者文本序列。
        #        :type contents: string or sequence of string
        #
        #        :param space_mode: 空格保留选项
        #        :type space_mode: int（整型）, 0-3有效
        #
        #        :param oov_level: 枚举强度选项
        #        :type oov_level:  int（整型）, 0-4有效
        #
        #        :param t2s: 繁简转换选项，繁转简或不转换
        #        :type t2s:  int（整型）, 0-1有效
        #
        #        :param special_char_conv: 特殊字符转化选项，针对回车、Tab等特殊字符转化或者不转化
        #        :type special_char_conv:  int（整型）, 0-1有效
        #
        #        :returns: 接口返回的结果列表。
        #
        #        :raises: :py:exc:`~bosonnlp.HTTPError` 如果 API 请求发生错误。
        #
        #        调用参数及返回值详细说明见：http://docs.bosonnlp.com/tag.html
        #
        #        调用示例：
        #
        #        >>> import os
        #        >>> nlp = BosonNLP(os.environ['BOSON_API_TOKEN'])
        #
        #        >>> result = nlp.tag('成都商报记者 姚永忠')
        #        >>> _json_dumps(result)
        #        '[{"tag": ["ns", "n", "n", "nr"], "word": ["成都", "商报", "记者", "姚永忠"]}]'
        #
        #        >>> format_tag_result = lambda tagged: ' '.join('%s/%s' % x for x in zip(tagged['word'], tagged['tag']))
        #        >>> result = nlp.tag("成都商报记者 姚永忠")
        #        >>> format_tag_result(result[0])
        #        '成都/ns 商报/n 记者/n 姚永忠/nr'
        #
        #        >>> result = nlp.tag("成都商报记者 姚永忠", space_mode=2)
        #        >>> format_tag_result(result[0])
        #        '成都/ns 商报/n 记者/n  /w 姚永忠/nr'
        #
        #        >>> result = nlp.tag(['亚投行意向创始成员国确定为57个', '“流量贵”频被吐槽'], oov_level=0)
        #        >>> format_tag_result(result[0])
        #        '亚/ns 投/v 行/n 意向/n 创始/vi 成员国/n 确定/v 为/v 57/m 个/q'
        #
        #        >>> format_tag_result(result[1])
        #        '“/wyz 流量/n 贵/a ”/wyy 频/d 被/pbei 吐槽/v'
        #        """
        return result
    #文本摘要
    def textSummary(self,s,title = '',limit=0.3):
        result = self.bonlp.summary(title = title,content = s,word_limit = limit)
        return result

# if __name__ == "__main__":
    # nl=BosonNLP()
    # s=['对于该小孩是不是郑尚金的孩子，目前已做亲子鉴定，结果还没出来，'
    #  '纪检部门仍在调查之中。成都商报记者 姚永忠']
    # #调用情感分析接口
    # print(nl.testSentiment(s))
    # #命名实体识别
    # resultlex=nl.lexicalAnalysis(s)
    # words = resultlex['word']
    # entities = resultlex['entity']
    # for entity in entities:
    #     print(''.join(words[entity[0]:entity[1]]), entity[2])
    # #依存文法分析
    # resultdep=nl.textDependency(s)
    # print(' '.join(resultdep[0]['word']))
    # print(' '.join(resultdep[0]['tag']))
    # print(resultdep[0]['head'])
    # print(' '.join(resultdep[0]['role']))
    #
    # #新闻字段
    # xinwen=['俄否决安理会谴责叙军战机空袭阿勒颇平民',
    #  '邓紫棋谈男友林宥嘉：我觉得我比他唱得好',
    #  'Facebook收购印度初创公司']
    # #新闻分类
    # resultclass=nl.textClassify(xinwen)
    #
    # guanjian='对于该小孩是不是郑尚金的孩子，目前已做亲子鉴定，结果还没出来,纪检部门仍在调查之中。成都商报记者 姚永忠'
    # resultkey=nl.testKeywords(guanjian)
    # for weight, word in resultkey:
    #         print(weight, word)
    # term='元宝'
    # #语义联想
    # resultsyn=nl.lexicalSynonym(term)
    # for score, word in resultsyn:
    #         print(score, word)
    # #分词
    # resultfenci=nl.fenci(s)
    # for d in resultfenci:
    #         print(' '.join(['%s/%s' % it for it in zip(d['word'], d['tag'])]))
    #
    # content = (
    # '腾讯科技讯（刘亚澜）10月22日消息，前优酷土豆技术副总裁黄冬已于日前正式加盟芒果TV，出任CTO一职。资料显示，黄冬历任土豆网技术副总裁、优酷土豆集团产品技术副总裁等职务，曾主持设计、运营过优酷土豆多个大型高容量产品和系统。此番加入芒果TV或与芒果TV计划自主研发智能硬件OS有关。今年3月，芒果TV对外公布其全平台日均独立用户突破3000万，日均VV突破1亿，但挥之不去的是业内对其技术能力能否匹配发展速度的质疑，亟须招揽技术人才提升整体技术能力。芒果TV是国内互联网电视七大牌照方之一，之前采取的是“封闭模式”与硬件厂商预装合作，而现在是“开放下载”+“厂商预装”。黄冬在加盟土豆网之前曾是国内FreeBSD（开源OS）社区发起者之一，是研究并使用开源OS的技术专家，离开优酷土豆集团后其加盟果壳电子，涉足智能硬件行业，将开源OS与硬件结合，创办魔豆智能路由器。未来黄冬可能会整合其在开源OS、智能硬件上的经验，结合芒果的牌照及资源优势，在智能硬件或OS领域发力。公开信息显示，芒果TV在今年6月对外宣布完成A轮5亿人民币融资，估值70亿。')
    # #新闻摘要
    # #print(content[0])
    # #print(isinstance(content[0], unicode))
    # resultsub=nl.newssubstract(content)
    # #print(isinstance(resultsub, unicode))#判断编码是否是unicode编码
    # #print(isinstance(resultsub, basestr))
    # #f=chardet.detect(resultsub)
    # #print(f)
    # print (resultsub)
    # #chardet.detect(nl.newssubstract(content))