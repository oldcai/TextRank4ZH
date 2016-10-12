#-*- encoding:utf-8 -*-
"""
@author:   letian
@homepage: http://www.letiantian.me
@github:   https://github.com/someus/
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from pyltp import SentenceSplitter, Segmentor, Postagger

import codecs
import os

from . import util

segmentor = postagger = None


def get_segmentor(model_path='ltp_data'):
    global segmentor
    if segmentor:
        return segmentor
    else:
        segmentor = Segmentor()
        segmentor.load('%s/cws.model' % model_path)
        return segmentor


def get_postagger(model_path='ltp_data'):
    global postagger
    if postagger:
        return postagger
    else:
        postagger = Postagger()
        postagger.load('%s/pos.model' % model_path)
        return postagger


def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')


class WordSegmentation(object):
    """ 分词 """
    
    def __init__(self, stop_words_file=None, allow_speech_tags=util.allow_speech_tags, model_path='ltp_data'):
        """
        Keyword arguments:
        stop_words_file    -- 保存停止词的文件路径，utf8编码，每行一个停止词。若不是str类型，则使用默认的停止词
        allow_speech_tags  -- 词性列表，用于过滤
        """     
        
        allow_speech_tags = [util.as_text(item) for item in allow_speech_tags]

        self.default_speech_tag_filter = allow_speech_tags
        self.stop_words = set()
        self.stop_words_file = get_default_stop_words_file()
        self.segmentor = get_segmentor(model_path)
        self.postagger = get_postagger(model_path)
        if type(stop_words_file) is str:
            self.stop_words_file = stop_words_file
        for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
            self.stop_words.add(word.strip())
    
    def segment(self, text, lower = True, use_stop_words = True, use_speech_tags_filter = False):
        """对一段文本进行分词，返回list类型的分词结果

        Keyword arguments:
        lower                  -- 是否将单词小写（针对英文）
        use_stop_words         -- 若为True，则利用停止词集合来过滤（去掉停止词）
        use_speech_tags_filter -- 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。    
        """
        text = util.as_text(text)
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)
        words_with_tag = zip(words, postags)
        
        if use_speech_tags_filter == True:
            words_with_tag = [(w, t) for w, t in words_with_tag if t in self.default_speech_tag_filter]

        # 去除特殊符号
        word_list = [w.strip() for (w, t) in words_with_tag if t != 'x']
        word_list = [word for word in word_list if len(word) > 0]
        
        if lower:
            word_list = [word.lower() for word in word_list]

        if use_stop_words:
            word_list = [word.strip() for word in word_list if word.strip() not in self.stop_words]

        return word_list
        
    def segment_sentences(self, sentences, lower=True, use_stop_words=True, use_speech_tags_filter=False):
        """将列表sequences中的每个元素/句子转换为由单词构成的列表。
        
        sequences -- 列表，每个元素是一个句子（字符串类型）
        """
        
        res = []
        for sentence in sentences:
            res.append(self.segment(text=sentence, 
                                    lower=lower, 
                                    use_stop_words=use_stop_words, 
                                    use_speech_tags_filter=use_speech_tags_filter))
        return res


class SentenceSegmentation(object):
    """ 分句 """
    
    def __init__(self, delimiters=util.sentence_delimiters):
        """
        Keyword arguments:
        delimiters -- 可迭代对象，用来拆分句子
        """
        self.delimiters = set([util.as_text(item) for item in delimiters])
    
    def segment(self, text):
        res = SentenceSplitter.split(util.as_text(text))
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res 


class Segmentation(object):
    
    def __init__(
            self, stop_words_file=None,
            allow_speech_tags=util.allow_speech_tags,
            delimiters=util.sentence_delimiters,
            model_path='ltp_data'
    ):
        """
        Keyword arguments:
        stop_words_file -- 停止词文件
        delimiters      -- 用来拆分句子的符号集合
        """
        self.ws = WordSegmentation(
            stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags, model_path=model_path
        )
        self.ss = SentenceSegmentation(delimiters=delimiters)
        self.filter_options = {
            'no_filter': {
                'use_stop_words': False,
                'use_speech_tags_filter': False
            },
            'no_stop_words': {
                'use_stop_words': True,
                'use_speech_tags_filter': False
            },
            'all_filters': {
                'use_stop_words': True,
                'use_speech_tags_filter': True
            },
        }

    def segment(self, text, lower=False, filters='no_stop_words'):
        text = util.as_text(text)
        sentences = self.ss.segment(text)
        filtered_words = self.ws.segment_sentences(
            sentences=sentences,
            lower=lower,
            **self.filter_options.get(filters)
        )

        return sentences, filtered_words


if __name__ == '__main__':
    pass
