import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
import jieba
def load_data():
    """
    读取数据/停用词
    :return: 数据，停用词

    """
    # 读取数据
    data = pd.read_csv("test.txt", sep="/t", names=["Cless", "Title", "Content"])
    print(data.head())
    # 读取停用词
    stop_words = pd.read_csv("stopwords.txt", names=["stopwords"], encoding="utf-8")
    stop_words = stop_words["stopwords"].values.tolist()
    print(stop_words)
    return data, stop_words

def main():
    '''
    主函数
    '''

    # 获取数据
    data, stopwords = load_data()
    # 分词
    segs = data['Content'].apply(lambda x:' '.join(jieba.cut(x)))
    # ti-idf构建
    tf_idf = TfidfVectorizer(stop_words=stopwords, max_features=1000,lowercase=False)
    # 拟合
    tf_idf.fit(segs)
    # 转换
    X = tf_idf.transform(segs)
    # 分割数据
    X_train,X_test, y_train, y_test = train_test_split(X, data["Class"], random_state=0)
    print(X_train[:2])
    print(y_train[:2])
    # 实例化朴素贝叶斯
    classifier = MultinomialNB()
    # 拟合
    classifier.fit(X_train, y_train)
    # 计算分数
    acc = classification_report(y_test,classifier.predict(X_test))
    print(f"准确率：{acc}")


if __name__ == '__main__':
    main()

