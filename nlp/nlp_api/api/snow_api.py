# -*- encoding: utf-8 -*-
from snownlp import SnowNLP
from snownlp import seg
from snownlp import tag
from snownlp import normal
from snownlp.summary import textrank,words_merge


class MyKeywordTextRank(textrank.KeywordTextRank):
    #
    # def __init__(self, docs):
    #     self.docs = docs
    #     self.words = {}
    #     self.vertex = {}
    #     self.d = 0.85
    #     self.max_iter = 200
    #     self.min_diff = 0.001
    #     self.top = []

    def solve(self):
        for doc in self.docs:
            que = []
            for word in doc:
                if word not in self.words:
                    self.words[word] = set()
                    self.vertex[word] = 1.0
                que.append(word)
                if len(que) > 5:
                    que.pop(0)
                for w1 in que:
                    for w2 in que:
                        if w1 == w2:
                            continue
                        self.words[w1].add(w2)
                        self.words[w2].add(w1)
        for _ in range(self.max_iter):
            m = {}
            max_diff = 0
            tmp = filter(lambda x: len(self.words[x[0]]) > 0,
                         self.vertex.items())
            tmp = sorted(tmp, key=lambda x: x[1] / len(self.words[x[0]]))
            for k, v in tmp:
                for j in self.words[k]:
                    if k == j:
                        continue
                    if j not in m:
                        m[j] = 1 - self.d
                    m[j] += (self.d / len(self.words[k]) * self.vertex[k])
            for k in self.vertex:
                if k in m and k in self.vertex:
                    if abs(m[k] - self.vertex[k]) > max_diff:
                        max_diff = abs(m[k] - self.vertex[k])
            self.vertex = m
            if max_diff <= self.min_diff:
                break
        self.top = list(self.vertex.items())
        self.top = sorted(self.top, key=lambda x: x[1], reverse=True)
        # return self.top

    def top_index(self, limit):
        return list(map(lambda x: x, self.top))[:limit]

class MySnowNLP(SnowNLP):
    def keywords(self, limit=5, merge=False):
        doc = []
        sents = self.sentences
        for sent in sents :
            words = seg.seg(sent)
            words = normal.filter_stop(words)
            doc.append(words)
        rank = MyKeywordTextRank(doc)
        result = rank.solve()

        ret = []
        for w in rank.top_index(limit) :
            ret.append(w)
        # top = rank.top(10)
        if merge :
            wm = words_merge.SimpleMerge(self.doc, ret)
            return wm.merge()
        return ret


class SnowNLPAPI:
    def __init__(self,snow_key=''):
        self.snow_key = snow_key
    def textKeywords(self,text,top_k = 10):
        # nlp = MysnowNLP(text)
        return MySnowNLP(text).keywords(top_k)

    def textSentiment(self,text):
        result = {}
        result['positive'] = SnowNLP(text).sentiments
        result['negative'] = 1 - SnowNLP(text).sentiments
        return result

    def textSummary(self,text,limit=5):
        return SnowNLP(text).summary(limit=limit)