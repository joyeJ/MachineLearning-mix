#! /usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------
# @version: py2.7
# @author: Joye
# @file: jieba-test1.py
# @time: 2017-4-14
# ---------------------

import jieba

def word_split(text):
    """ 
    Split a text in words. Returns a list of tuple that contains 
    (word, location) location is the starting byte position of the word. 
    """
    word_list = []
    windex = 0
    word_primitive = jieba.cut(text, cut_all=True)
    for word in word_primitive:
        if len(word) > 0:
            word_list.append((windex, word))
            windex += 1
    return word_list


def inverted_index(text):
    """ 
    Create an Inverted-Index of the specified text document. 
        {word:[locations]} 
    """
    inverted = {}
    for index, word in word_split(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)
    return inverted


def inverted_index_add(inverted, doc_id, doc_index):
    """ 
    Add Invertd-Index doc_index of the document doc_id to the  
    Multi-Document Inverted-Index (inverted),  
    using doc_id as document identifier. 
        {word:{doc_id:[locations]}} 
    """
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted


def search_a_word(inverted, word):
    """ 
    search one word 
    """
    word = word.decode('utf-8')
    if word not in inverted:
        return None
    else:
        word_index = inverted[word]
    return word_index


def search_words(inverted, wordList):
    """ 
    search more than one word 
    """
    wordDic = []
    docRight = []
    for word in wordList:
        if isinstance(word, str):
            word = word.decode('utf-8')
        if word not in inverted:
            return None
        else:
            element = inverted[word].keys()
            element.sort()
            wordDic.append(element)
    numbers = len(wordDic)
    inerIndex = [0 for i in range(numbers)]
    docIndex = [wordDic[i][0] for i in range(numbers)]
    flag = True
    while flag:
        if min(docIndex) == max(docIndex):
            docRight.append(min(docIndex))
            inerIndex = [inerIndex[i] + 1 for i in range(numbers)]
            for i in range(numbers):
                if inerIndex[i] >= len(wordDic[i]):
                    flag = False
                    return docRight
            docIndex = [wordDic[i][inerIndex[i]] for i in range(numbers)]
        else:
            minIndex = min(docIndex)
            minPosition = docIndex.index(minIndex)
            inerIndex[minPosition] += 1
            if inerIndex[minPosition] >= len(wordDic[minPosition]):
                flag = False
                return docRight
            docIndex = [wordDic[i][inerIndex[i]] for i in range(numbers)]


def search_phrase(inverted, phrase):
    """ 
    search phrase 
    """
    docRight = {}
    temp = word_split(phrase)
    wordList = [temp[i][1] for i in range(len(temp))]
    docPossible = search_words(inverted, wordList)
    for doc in docPossible:
        wordIndex = []
        indexRight = []
        for word in wordList:
            wordIndex.append(inverted[word][doc])
        numbers = len(wordList)
        inerIndex = [0 for i in range(numbers)]
        words = [wordIndex[i][0] for i in range(numbers)]
        flag = True
        while flag:
            if words[-1] - words[0] == numbers - 1:
                indexRight.append(words[0])
                inerIndex = [inerIndex[i] + 1 for i in range(numbers)]
                for i in range(numbers):
                    if inerIndex[i] >= len(wordIndex[i]):
                        flag = False
                        docRight[doc] = indexRight
                        break
                if flag:
                    words = [wordIndex[i][inerIndex[i]] for i in range(numbers)]
            else:
                minIndex = min(words)
                minPosition = words.index(minIndex)
                inerIndex[minPosition] += 1
                if inerIndex[minPosition] >= len(wordIndex[minPosition]):
                    flag = False
                    break
                if flag:
                    words = [wordIndex[i][inerIndex[i]] for i in range(numbers)]
    return docRight


if __name__ == '__main__':
    doc1 = """ 
中文分词指的是将一个汉字序列切分成一个一个单独的词。分词就是将连续的字序列按照一定的规范 
重新组合成词序列的过程。我们知道，在英文的行文中，单词之间是以空格作为自然分界符的，而中文 
只是字、句和段能通过明显的分界符来简单划界，唯独词没有一个形式上的分界符，虽然英文也同样 
存在短语的划分问题，不过在词这一层上，中文比之英文要复杂的多、困难的多。 
"""

    doc2 = """ 
存在中文分词技术，是由于中文在基本文法上有其特殊性，具体表现在： 
与英文为代表的拉丁语系语言相比，英文以空格作为天然的分隔符，而中文由于继承自古代汉语的传统， 
词语之间没有分隔。　古代汉语中除了连绵词和人名地名等，词通常就是单个汉字，所以当时没有分词 
书写的必要。而现代汉语中双字或多字词居多，一个字不再等同于一个词。 
在中文里，“词”和“词组”边界模糊 
现代汉语的基本表达单元虽然为“词”，且以双字或者多字词居多，但由于人们认识水平的不同，对词和 
短语的边界很难去区分。 
例如：“对随地吐痰者给予处罚”，“随地吐痰者”本身是一个词还是一个短语，不同的人会有不同的标准， 
同样的“海上”“酒厂”等等，即使是同一个人也可能做出不同判断，如果汉语真的要分词书写，必然会出现 
混乱，难度很大。 
中文分词的方法其实不局限于中文应用，也被应用到英文处理，如手写识别，单词之间的空格就不很清楚， 
中文分词方法可以帮助判别英文单词的边界。 
"""

    doc3 = """ 
作用 
中文分词是文本挖掘的基础，对于输入的一段中文，成功的进行中文分词，可以达到电脑自动识别语句含义的效果。 
中文分词技术属于自然语言处理技术范畴，对于一句话，人可以通过自己的知识来明白哪些是词，哪些不是词， 
但如何让计算机也能理解？其处理过程就是分词算法。 
影响 
中文分词对于搜索引擎来说，最重要的并不是找到所有结果，因为在上百亿的网页中找到所有结果没有太多的意义， 
没有人能看得完，最重要的是把最相关的结果排在最前面，这也称为相关度排序。中文分词的准确与否，常常直接 
影响到对搜索结果的相关度排序。从定性分析来说，搜索引擎的分词算法不同，词库的不同都会影响页面的返回结果 
"""

    doc4 = """ 
这种方法又叫做机械分词方法，它是按照一定的策略将待分析的汉字串与一个“充分大的”机器词典中的词条进行配， 
若在词典中找到某个字符串，则匹配成功（识别出一个词）。按照扫描方向的不同，串匹配分词方法可以分为正向 
匹配和逆向匹配；按照不同长度优先匹配的情况，可以分为最大（最长）匹配和最小（最短）匹配；常用的几种 
机械分词方法如下： 
正向最大匹配法（由左到右的方向）； 
逆向最大匹配法（由右到左的方向）； 
最少切分（使每一句中切出的词数最小）； 
双向最大匹配法（进行由左到右、由右到左两次扫描） 
还可以将上述各种方法相互组合，例如，可以将正向最大匹配方法和逆向最大匹配方法结合起来构成双向匹配法。 
由于汉语单字成词的特点，正向最小匹配和逆向最小匹配一般很少使用。一般说来，逆向匹配的切分精度略高于 
正向匹配，遇到的歧义现象也较少。统计结果表明，单纯使用正向最大匹配的错误率为，单纯使用逆向 
最大匹配的错误率为。但这种精度还远远不能满足实际的需要。实际使用的分词系统，都是把机械分词 
作为一种初分手段，还需通过利用各种其它的语言信息来进一步提高切分的准确率。 
一种方法是改进扫描方式，称为特征扫描或标志切分，优先在待分析字符串中识别和切分出一些带有明显特征 
的词，以这些词作为断点，可将原字符串分为较小的串再来进机械分词，从而减少匹配的错误率。另一种方法 
是将分词和词类标注结合起来，利用丰富的词类信息对分词决策提供帮助，并且在标注过程中又反过来对分词 
结果进行检验、调整，从而极大地提高切分的准确率。 
对于机械分词方法，可以建立一个一般的模型，在这方面有专业的学术论文，这里不做详细论述。 
"""

    doc5 = """ 
从形式上看，词是稳定的字的组合，因此在上下文中，相邻的字同时出现的次数越多，就越有可能构成一个词。 
因此字与字相邻共现的频率或概率能够较好的反映成词的可信度。可以对语料中相邻共现的各个字的组合的频度 
进行统计，计算它们的互现信息。定义两个字的互现信息，计算两个汉字的相邻共现概率。互现信息体现了 
汉字之间结合关系的紧密程度。当紧密程度高于某一个阈值时，便可认为此字组可能构成了一个词。这种方法 
只需对语料中的字组频度进行统计，不需要切分词典，因而又叫做无词典分词法或统计取词方法。但这种方法 
也有一定的局限性，会经常抽出一些共现频度高、但并不是词的常用字组，例如“这一”、“之一”、“有的”、 
“我的”、“许多的”等，并且对常用词的识别精度差，时空开销大。实际应用的统计分词系统都要使用一部基本 
的分词词典（常用词词典）进行串匹配分词，同时使用统计方法识别一些新的词，即将串频统计和串匹配结合起来， 
既发挥匹配分词切分速度快、效率高的特点，又利用了无词典分词结合上下文识别生词、自动消除歧义的优点。 
另外一类是基于统计机器学习的方法。首先给出大量已经分词的文本，利用统计机器学习模型学习词语切分的规律 
（称为训练），从而实现对未知文本的切分。我们知道，汉语中各个字单独作词语的能力是不同的，此外有的字常 
常作为前缀出现，有的字却常常作为后缀（“者”“性”），结合两个字相临时是否成词的信息，这样就得到了许多 
与分词有关的知识。这种方法就是充分利用汉语组词的规律来分词。这种方法的最大缺点是需要有大量预先分好词 
的语料作支撑，而且训练过程中时空开销极大。 
到底哪种分词算法的准确度更高，目前并无定论。对于任何一个成熟的分词系统来说，不可能单独依靠某一种算法 
来实现，都需要综合不同的算法。例如，海量科技的分词算法就采用“复方分词法”，所谓复方，就是像中西医结合 
般综合运用机械方法和知识方法。对于成熟的中文分词系统，需要多种算法综合处理问题。  
"""

    # Build Inverted-Index for documents
    inverted = {}
    documents = {'doc1': doc1, 'doc2': doc2, 'doc3': doc3, 'doc4': doc4, 'doc5': doc5}
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

        # Search one word
    aWord = "分词"
    result_a_word = search_a_word(inverted, aWord)
    if result_a_word:
        result_a_word_docs = result_a_word.keys()
        print "'%s' is appeared at" % (aWord)
        for result_a_word_doc in result_a_word_docs:
            result_a_word_index = result_a_word[result_a_word_doc]
            for index in result_a_word_index:
                print (str(index) + ' '),
            print "of " + result_a_word_doc
        print ""
    else:
        print "No matches!\r\n"

        # Search more than one word
    words = ["汉语", "切分"]
    result_words = search_words(inverted, words)
    if result_words:
        print ("["),
        for i in range(len(words)):
            print ("%s " % (words[i])),
        print ("] are appeared at the "),
        for result_words_doc in result_words:
            print (result_words_doc + ' '),
        print "\r\n"
    else:
        print "No matches!\r\n"

        # Search phrase
    phrase = "正向最大"
    result_phrase = search_phrase(inverted, phrase)
    if result_phrase:
        result_phrase_docs = result_phrase.keys()
        print "'%s' is appeared at the " % (phrase)
        for result_phrase_doc in result_phrase_docs:
            result_phrase_index = result_phrase[result_phrase_doc]
            for index in result_phrase_index:
                print (str(index) + ' '),
            print "of " + result_phrase_doc
        print ""
    else:
        print "No matches!\r\n"