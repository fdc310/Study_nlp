import pandas as pd
# from textblob import TextBlob
from snownlp import SnowNLP
from docx import Document
import random
import os

def read_data(filepath):
    """
    读取文件数据
    :return: 数据
    """
    # 读取文件中格式化数据
    data = pd.read_csv(filepath, sep='|', names=["add", "yuyan", "text"])
    print(data[:5])
    return data

def qingxi_qinggan(data,filename = None):


    # 提取出文案数据，直接筛除短文本无用数据d
    long_texts = [text for text in data["text"] if not isinstance(text, float) and len(text) > 80]
    # 进行文案情感评分
    sl_data = [SnowNLP(text).sentiments for text in long_texts]
    # print(sl_data)
    # 将文本和评分组合在一起
    text_sl = [[i.replace(',', '，'), j] for i, j in zip(long_texts, sl_data)]
    # 高情感评分
    gao_data = []
    # 低情感评分
    di_data = []
    for i in range(len(text_sl)):
        if text_sl[i][1] > 0.35:
            gao_data.append(text_sl[i])
        else:
            di_data.append(text_sl[i])

    print(len(gao_data), len(di_data))
    gaonum = 35
    if len(gao_data) < gaonum:
        gaonum = len(gao_data)
    # 随机抽取数据
    sha_gao = random.sample(gao_data, gaonum)
    # num = 20
    # if len(di_data) < num:
    #     num = len(di_data)
    # sha_di = random.sample(di_data, num)
    # print(sha_di)
    # print(data['add'][0])
    if not filename:
        filename = data['add'][0]
    if not os.path.isfile(f"newdata/{filename}知识库.csv"):
        with open(f"newdata/{filename}知识库.csv", "a", encoding='utf-8-sig') as f:
            for i in long_texts:
                f.write(f"{i}\n")
    if not os.path.isfile(f"newdata/{filename}.docx"):
        doc = Document()
        for i in gao_data:
            doc.add_paragraph(i[0])
        doc.save(f"newdata/{filename}.docx")

    # if not os.path.isfile(f"newdata/{filename}.csv"):
    #     with open(f"newdata/{filename}.csv", "a", encoding='utf-8-sig') as f:
    #         for i in range(gaonum):
    #             if i < gaonum:
    #                 f.write(f"{sha_gao[i][0]}")
    #             if i < num:
    #                 f.write(f",{sha_di[i][0]}\n")
    #             else:
    #                 f.write(f"{sha_gao[i][0]}\n")



if __name__ == '__main__':
    basepath = os.getcwd()
    filedir = os.path.join(basepath, 'dengdai')
    filenames = os.listdir(filedir)
    for filename in filenames:
        data = read_data(os.path.join(filedir,filename))
        qingxi_qinggan(data, filename)
    print(basepath)




    # data = read_data()





    # for text in long_texts:
    #     sl = SnowNLP(text)
    #     print(sl.sentiments)
    #     # print(sl.sentiment.polarity)
    #     break

