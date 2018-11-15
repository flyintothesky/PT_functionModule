"""
文本分词
"""
import os, re
import jieba
from jieba import analyse
dictpath = os.path.split(os.path.realpath(__file__))[0]+"/dicts"
jieba.set_dictionary(dictpath + "/synonym.txt")
jieba.load_userdict(dictpath +"/custom_words.txt") #加载自定义词典  


# 创建停用词列表
def stopwordslist():
    """
              使用结巴分词，去除停用词
    :param content: 默认停用词
    :return: 停用词
    """
    stopwords = [line.strip() for line in open(dictpath +"/stop_words.txt",encoding='UTF-8').readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    """'
             对文档中的每一行进行中文分词,去掉停用词
    """
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

def abs_pos(words):
    """
             词性标注
             保留制定词性的词
    """
    allow_pos = ('ns', 'n', 'v', 'nv')
    word_tags = analyse.extract_tags(words, topK=5, withWeight=False, allowPOS=allow_pos)
#     for t in tags:
#         print(t) 
    return word_tags

def cut_data(iter_text):
    """
              分词，不去停用词
    :param iter_text: 元组或者列表形式的文本
    """
    assert isinstance(iter_text, (list, tuple))

    # 处理从文本读入的数据
    if isinstance(iter_text, list):
        return [cut_word(each) for each in iter_text]

    # 处理从数据库读入数据
    return [cut_word(each[0]) for each in iter_text]


def cut_word(content, cut_all=False):
    """
              使用结巴分词，默认使用不完全分词
    :param content: 字符串
    :param cut_all: 默认精确分词
    :return: 以空格分割的字符串
    """
    seg_list = list(jieba.cut(content, cut_all=cut_all))
    return seg_list


if __name__ == '__main__':
    """ 
              此处为功能测试 
    """
    text = "总行人员通过任务分配导入功能，导入任务分配数据到客户风险报送系统，分行进行报送"
    line_seg = seg_depart(text)
    print("[停用词+自定义词分词]: ", line_seg)
    line_seg1 = abs_pos(line_seg)
    print("[词性]: ", line_seg1)