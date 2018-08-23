import sys
import re

class TxtReader():
    def __init__(self, url='夏祭り.txt'):

        self._readfile(url)

        self.time_start, self.time_end = self._get_time_section()
        self.content_start = self.time_end + 1

        # following is public to other class
        self.timeaxis_lst = []  #毫秒时间轴列表, [msec]
        self.block_amount = len(self.timeaxis_lst)  # 共有多少句话
        self.original_lst = []
        self.analyzer_lst = []
        self.translate_lst = []
        self.time2block_dict = {}    # {time(str) :  block(lst[original, analysis, translate])}

        self._get_timeaxis()
        self._get_time_block_dict()

    def _readfile(self, url):
        self.url = url
        try:
            f = open(self.url, 'r', encoding='utf-8')
            self.txt = f.readlines()   # type -> list
            f.close()
        except Exception as e:
            print(e)

    def _get_time_section(self):     # TODO \r\n 不同平台的问题
        time_start = self.txt.index('time_start\n')
        time_end = self.txt.index('time_end\n')
        return time_start + 1, time_end

    # [00:07.29]  TODO can use lambda or map as one function
    def _timestr_to_msec(self, str):
        msec = int(str[1:3]) * 60000 + int(float(str[4:9]) * 1000)
        return msec

    def _get_timeaxis(self):
        for i in self.txt[self.time_start:self.time_end]:
            self.timeaxis_lst.append(self._timestr_to_msec(i))

    def _get_time_block_dict(self):     # from 0
        index = self.content_start
        for i in range(0, self.block_amount):
            index = self._one_block_finder(i, index)

    def _one_block_finder(self, sentence_num, start_index):  # use static to avoid search from beginning every time
        block = []
        while not self.txt[start_index].startswith('{}.'.format(sentence_num + 1)):  # check until "sentence_num."
            start_index += 1

        #might use zip() function to generate block dict TODO
        #add original to block
        self.original_lst.append(self.txt[start_index])
        block.append(self.txt[start_index])
        start_index += 1

        #add analyzer to block
        self.analyzer_lst.append(self.txt[start_index])
        block.append(self.txt[start_index])
        start_index += 1

        #add translate to block
        self.translate_lst.append(self.txt[start_index])
        block.append(self.txt[start_index])
        start_index += 1

        self.time2block_dict.setdefault(self.timeaxis_lst[sentence_num], block)
        return start_index

    # 输入string， 寻找（）中的平假名注音以及前面的汉字，返回二者集合的字典 {xx:xx, yy:yy, zz:zz}
    def find_kanji_hiragana(self, st):
        hiragana = re.findall('[(,（](.*?)[),）]', st)  # find (XX) XX in st, get list
        kanji = re.findall('(\S*?)[(,（]', st)
        print(type(hiragana))
        if not len(kanji) == len(hiragana):
            print('cannot pair kanji and hiragana')
        else:
            pronounce = dict(zip(kanji, hiragana))
            return pronounce



a = TxtReader()
print(a.find_kanji_hiragana('遠い（とおい长音）：遥远。 夢（ゆめ）：梦想。 中（なか）：中。'))