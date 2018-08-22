# 爬取网易歌词。需要复制歌曲链接
# -*- coding:utf-8 -*-
import requests
import json
import re
import MeCab

class LrcCrawler:
    def __init__(self, netease_url='http://music.163.com/#/m/song?id=28465396'):
        self.url = netease_url

        # can access from outside
        self.ori_lrc, self.trans_lrc = self.get_lyric()

    def __get_songid(self):
        index = self.url.find('id=')
        return self.url[index + 3:]

    def get_lyric(self):
        songid = self.__get_songid()
        lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(songid) + '&lv=1&kv=1&tv=-1'
        try:
            lyric = requests.get(lrc_url)
            json_obj = lyric.text
            j = json.loads(json_obj)
            orlrc = j['lrc']['lyric']
            lrc = j['tlyric']['lyric']
            return orlrc, lrc
        except Exception as e:
            print(e)


class LrcParser:
    def __init__(self, ori_lrc, trans_lrc,):
        self.__ori_lrc = ori_lrc
        self.__trans_lrc = trans_lrc

        #can access from outside
        self.least_len = 12
        self.time_lst, self.trans_lst, self.ori_lst = self.__get_all_lst()
        self.block_amount = len(self.time_lst)


    def __get_all_lst(self):
        time_pattern = re.compile(r'^\[\d{2}:\d{2}\.\d{2,3}\]')

        trans_lst = [x for x in self.__trans_lrc.split('\n') if len(x) > self.least_len and re.match(time_pattern, x)]
        ori_lst = [x for x in self.__ori_lrc.split('\n') if len(x) > self.least_len and re.match(time_pattern, x)]

        time_lst = []
        trans_lst_no_time = []
        ori_lst_no_time = []

        for i in trans_lst:
            m = re.match(time_pattern, i)
            trans_lst_no_time.append(i.split(']')[1])
            time_lst.append(m.group())

        for i in ori_lst:
            if not re.match(time_pattern, i).group() in time_lst:
                continue
            ori_lst_no_time.append(i.split(']')[1])

        return time_lst, trans_lst_no_time, ori_lst_no_time


class TemplateGenerator:
    def __init__(self, time_lst, trans_lst, ori_lst, url='/Users/yuhu/Desktop/日语歌曲翻译/歌词翻译txt版/', file_name='奏.txt'):
        self.__time_lst = time_lst
        self.__trans_lst = trans_lst
        self.__ori_lst = ori_lst

        self.target_url = url
        self.file_name = file_name
        self.analyzer = LyricAnalyzer(ori_lst)

    def write_to_file(self):
        f = open(self.target_url + self.file_name, 'a')

        def write_analysis(sentence_idx):
            for word in self.analyzer.sentenceidx_word_dict[sentence_idx]:
                f.write(word[0] + ':')
                for info in word[1:]:
                    f.write(info + ' ')

        f.write('time_start')
        for i in self.__time_lst:
            f.write('\r\n' + i)
        f.write('\r\ntime_end')
        for i in range(0, len(self.__time_lst)):
            f.write('\r\n{}.'.format(i + 1) + self.__ori_lst[i])
            f.write('\r\n')
            #write_analysis(i)
            f.write('\r\n' + self.__trans_lst[i])
            f.write('\r\n')
        f.close()


class LyricAnalyzer:
    def __init__(self, ori_lst):
        self.__ori_lst = ori_lst
        self.mecab = MeCab.Tagger("-Ochasen")
        self.sentenceidx_word_dict = self.lyric_analyze()
        self.get_info_amount = 3   # get 0, 2, 3

    '''
    ['夢\tユメ\t夢\t名詞-一般\t\t', 'なら\tナラ\tだ\t助動詞\t特殊・ダ\t仮定形', 
    'ば\tバ\tば\t助詞-接続助詞\t\t', 'どれほど\tドレホド\tどれほど\t副詞-一般\t\t', 
    'よかっ\tヨカッ\tよい\t形容詞-自立\t形容詞・アウオ段\t連用タ接続',  'EOS', '']
    '''
    def __one_sentence_analyze(self, sentence):
        filt_sentence = re.sub('\(.*?\)', '', sentence)
        result_lst = str(self.mecab.parse(filt_sentence)).split('\n')[:-2]  #TODO delete str, unstable -2!!
        word_lst = []
        for word in result_lst:
            word_info_lst = [v for k, v in enumerate(word.split('\t')) if k in (0, 2, 3)]
            word_lst.append(word_info_lst)

        return word_lst

    def lyric_analyze(self):
        sentenceidx_word_dict = {}
        for index, v in enumerate(self.__ori_lst):
            sentenceidx_word_dict.setdefault(index, self.__one_sentence_analyze(v))
        return sentenceidx_word_dict











a = LrcCrawler()
parser = LrcParser(a.ori_lrc, a.trans_lrc)
gen = TemplateGenerator(parser.time_lst, parser.trans_lst, parser.ori_lst)
gen.write_to_file()



'''
    def __get_all_timestamp(self):
        all_time = re.findall('\[\d{2}:\d{2}\.\d{2,3}\]', self.__trans_lrc)
        print(all_time)
        return all_time
'''

'''
print(gen.trans_lrc_list)
print(gen.all_time_stamp)
print('lst.len{} and timelst.len{}'.format(len(gen.trans_lrc_list), len(gen.all_time_stamp)))
#b = re.sub('\[\d{2}:\d{2}\.\d{2,3}\]', '', a.trans_lrc)
#b = re.split('\[d{2}:\d{2}\.\d{2,3}\](\W+?)', a.trans_lrc)
#b = a.trans_lrc.split('\n')
#print(b)
#c = a.trans_lrc.split('\n')
#print(c[:3])
'''

'''
note:
word_info_lst = [v for k, v in enumerate(word.split('\t')) if k in (0, 2, 3)]
这个方法感觉很不错！因为k的值易于更改。3的系数也想要，直接加就可以了。

'''