# coding:utf-8
# gensim需要先训练的，用它自带的数据集进行训练


from nltk import download
from analysis import Analysis, SentimentAnalysis2
from nltk.stem.wordnet import WordNetLemmatizer
import string
from gensim.models import LdaModel
from gensim import corpora
from nltk.corpus import stopwords


## download的资源写在这里
# download("stopwords")
# download("wordnet")
# download("omw-1.4")

# 总体来一个，不用每天都搞了
# 去重推文其积极的话题
def simpleDataCleaning(day, sentiment):
    df = Analysis().sentimentScore()
    # df = SentimentAnalysis2().sentiment()
    # df = df[df['day'].apply(lambda x: x == day)]     # 时间
    df = df[df['class'].apply(lambda x: x == sentiment)]   # 情感态度
    doc_original = list(df['tweets'])

# 简单的去掉一些关键词
    doc_complete = list(map(
    lambda x: (x.replace("rt", "").replace("RT", "").
                replace("shell", "").replace("Shell", "").replace("@Shell", "").
                replace("yes","").replace("no","").
               replace("don't","").replace("it's","").replace("tank","").
               replace('exxonmobil','').replace("chevron","").replace("hamidmirpak","").
               replace("dcislamabad","").replace("cdathecapital", ""))
                , doc_original))
    return doc_complete
# print(simpleDataCleaning())

# 参数设置
stop = set(stopwords.words('english'))  # 去重停用词
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
day = "May 04"
sentiment = -1

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized
    # return stop_free

doc_clean = [clean(doc).split() for doc in simpleDataCleaning(day, sentiment)]


# print(doc_clean)
# 创建语料的词语词典，每个单独的词语都会被赋予一个索引
dictionary = corpora.Dictionary(doc_clean)
#
# 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# 使用 gensim 来创建 LDA 模型对象
Lda = LdaModel

# 在 DT 矩阵上运行和训练 LDA 模型
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
# 输出结果
# print(ldamodel.print_topics(num_topics=3, num_words=5))
# num_topic是生成的主题，而num_words是生成主题的排序
# print(ldamodel.print_topics(num_topics=3, num_words=5))
res = []
for topic in ldamodel.print_topics(num_topics=10, num_words=3):
    i = str(topic[1]).split(" + ")
    for s in i:
        res.append(s)
# res = res.sort(reverse=False)
# example，排序
# a = ['0.034*"need"', '0.023*"exxonmobil"', '0.012*"chevron"', '0.024*"oil"', '0.024*"tak"', '0.012*"carbon"', '0.019*"get"', '0.019*"exxonmobil"', '0.010*"predefined"', '0.024*"it’s"', '0.024*"247"', '0.024*"12"', '0.031*"forget"', '0.021*"russian"', '0.021*"exxonmobil"', '0.027*"like"', '0.027*"coffee"', '0.027*"thank"', '0.021*"bpamerica"', '0.021*"quality"', '0.011*"product"', '0.030*"exxonmobil"', '0.020*"bpamerica"', '0.020*"people"', '0.012*"chevron"', '0.012*"bpplc"', '0.012*"kwasikwaeng"', '0.034*"price"', '0.018*"thedopebohemian"', '0.018*"totalenergiesug"']
res.sort(reverse=True)
print(res)


# print(res)


