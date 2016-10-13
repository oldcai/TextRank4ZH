#-*- encoding:utf-8 -*-
"""
@author:   letian
@homepage: http://www.letiantian.me
@github:   https://github.com/someus/
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import util
from .Segmentation import Segmentation


class TextRank4Sentence(object):
    
    def __init__(
            self, stop_words_file=None,
            allow_speech_tags=util.allow_speech_tags,
            delimiters=util.sentence_delimiters,
            api_url='http://localhost:11200'):
        """
        Keyword arguments:
        stop_words_file  --  str，停止词文件路径，若不是str则是使用默认停止词文件
        delimiters       --  默认值是`?!;？！。；…\n`，用来将文本拆分为句子。
        
        Object Var:
        self.sentences               --  由句子组成的列表。
        self.words_no_filter         --  对sentences中每个句子分词而得到的两级列表。
        self.words_no_stop_words     --  去掉words_no_filter中的停止词而得到的两级列表。
        self.words_all_filters       --  保留words_no_stop_words中指定词性的单词而得到的两级列表。
        """
        self.seg = Segmentation(stop_words_file=stop_words_file,
                                allow_speech_tags=allow_speech_tags,
                                delimiters=delimiters,
                                api_url=api_url)
        
    def get_key_sentences(
            self, text, lower=False,
            sim_func=util.get_similarity,
            pagerank_config=None,
            filters='all_filters',
            num=6, sentence_min_len=6,
    ):
        """
        Keyword arguments:
        text                 --  文本内容，字符串。
        lower                --  是否将文本转换为小写。默认为False。
        source               --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来生成句子之间的相似度。
                                 默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。
        sim_func             --  指定计算句子相似度的函数。
        """

        sentences, filtered_words = self.seg.segment(text=text, lower=lower, filters=filters)

        key_sentences = util.sort_sentences(
            sentences=sentences,
            words=filtered_words,
            sim_func=sim_func,
            pagerank_config=pagerank_config or {'alpha': 0.85},
        )

        result = []
        count = 0
        for item in key_sentences:
            if count >= num:
                break
            if len(item['sentence']) >= sentence_min_len:
                result.append(item)
                count += 1
        result.sort(key=lambda x: x['index'])
        return result
    

if __name__ == '__main__':
    pass
