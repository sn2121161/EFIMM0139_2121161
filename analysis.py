# coding:utf-8
# 对推文进行整理

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download
from matplotlib import pyplot as plt
import warnings
import seaborn as sns
import numpy as np

warnings.filterwarnings("ignore")
# download("vader_lexicon")

class Analysis():
    def __init__(self):
        self.general = 'D:\\上课资料库\\social media and web analysis\\结课论文\\'
        self.paths = [
                 self.general + 'dataset(backups)_1.xlsx',
                 self.general + 'dataset_2.xlsx',
                 self.general + 'dataset_3.xlsx',
                 self.general + 'dataset_4.xlsx',
                 self.general + 'dataset_5.xlsx']

    def combine(self):
        df_shell = pd.DataFrame()
        for path in self.paths:
            # print(df)
            df_shell = df_shell.append( pd.read_excel(path), ignore_index=True)
        return df_shell

# 去重留推文得到的
    def duplicate(self):
        # float has no attribution "encode" 因为nan值也被转码成了float，因此，要删除这些空值
        df = pd.DataFrame(self.combine()[2].drop_duplicates()).dropna(how = "any")
        df.columns = ['tweets']
        df.astype(str)
        return df.reset_index()

    def sentimentScore(self):
        df_tweets = self.duplicate()
        scorer = SentimentIntensityAnalyzer()

        def predict_sentiment(text_string):
            return (scorer.polarity_scores(text_string)['compound'])

        df_tweets['sentiment'] = df_tweets['tweets'].apply(predict_sentiment)
        df_tweets['class'] = df_tweets['sentiment'].apply(lambda s: 1 if s > 0 else -1 if s < 0 else 0)
        return df_tweets

    def desc(self):
        df_tweets = self.sentimentScore()
        return df_tweets.describe()

    def drawPic(self):
        df_tweets = self.sentimentScore()
        # plt.figure(figsize = (12, 8))

        ## 分析情感分布
        # plt.scatter(x = [_ for _ in range(len(df_tweets['sentiment']))], y = df_tweets['sentiment'], c="b")
        # plt.title("sentiment distribution", fontsize=18)
        # plt.xlabel("number of tweets", fontsize=14)
        # plt.ylabel("sentiment score", fontsize=14)

        # 分类
        # df_class = df_tweets.groupby('class')['sentiment'].agg(['count']).reset_index()
        # plt.bar(df_class['class'], df_class['count'], color=("r","g","b"))
        # sns.pairplot(df_tweets[['sentiment','class']])
        # plt.show()

        ##distplot
        plt.style.use("ggplot")
        sns.distplot(df_tweets['sentiment'])
        plt.title("Histogram and kernel density estimation graph", fontsize=16)
        plt.xlabel("sentiment", fontsize=13)
        plt.ylabel("frequency",fontsize=13)
        plt.show()



# 按照时间顺序来
class SentimentAnalysis2():
    def __init__(self):
        ana = Analysis()
        self.df_shell = ana.combine()

    def addTime(self):
        df_time = self.df_shell[[1,2]]
        df_time.columns = ['time', 'tweets']
        df_time['day'] = df_time['time'].apply(lambda x: x[4:10])  # 精确到每小时 4:13，精确到天 4:10
        df_time = df_time[['day', 'tweets']].drop_duplicates().dropna()
        return df_time

    def sentiment(self):
        df_tweets = self.addTime()
        scorer = SentimentIntensityAnalyzer()

        def predict_sentiment(text_string):
            return (scorer.polarity_scores(text_string)['compound'])

        df_tweets['sentiment'] = df_tweets['tweets'].apply(predict_sentiment)
        df_tweets['class'] = df_tweets['sentiment'].apply(lambda s: 1 if s > 0 else -1 if s < 0 else 0)
        return df_tweets

    def group(self):
        df_day = self.sentiment()
        df_group = df_day.groupby('day')['sentiment'].agg(['mean']).reset_index()
        df_group = df_group.sort_values(by=['day'], ascending=True)
        df_count = df_day.groupby('day')['sentiment'].agg(['count']).reset_index()
        return df_group, df_count

    def picture(self):
        # 趋势线函数拟合
        df_group, df_count = self.group()
        x = [_ for _ in range(len(df_group['day']))]
        p = np.poly1d(np.polyfit(x, df_group['mean'], 4))
        plt.style.use("ggplot")
        fig, ax = plt.subplots()  # 创建子图

        ax.plot(x, p(x), 'b--', label = "Trendline")
        # plt.style.use("ggplot")
        ax.plot(df_group['day'], df_group['mean'])
        # plt.bar(df_count['day'], df_count['count'])
        ax.set_title("Trends in people's average sentiment over 10 days(daily basis)" ,fontsize=16)
        ax.set_xlabel("days", fontsize=13)
        ax.set_ylabel("average sentiment score", fontsize=13)

        plt.xticks(rotation = 270, fontsize = 10)
        ax.legend()

        plt.show()

    def detect(self):
        df_54 = self.sentiment()
        df_54.to_excel("D:\\上课资料库\\social media and web analysis\\结课论文\\detect.xlsx")


def main():
    # ana = Analysis()
    # print(ana.drawPic())
    # print(ana.desc())
    ana2 = SentimentAnalysis2()
    # print(ana2.addTime())
    # print(ana2.sentiment())
    # print(ana2.group())
    print(ana2.picture())
    # print(ana2.detect())



if __name__ == "__main__":
    main()