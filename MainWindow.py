import sys
from Lyricwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import eyed3
from TxtReader import TxtReader
import re
import random
from PyQt5.QtWidgets import QFontDialog


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    # path = '/Users/yuhu/Music/网易云音乐/東山奈央/夏祭り.mp3'
    path = '/Users/yuhu/Desktop/Lyricplayer/musics/Lemon.mp3'

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.current_block = 0

        self.player = Player(self)

        with open('QSS/playerbutton.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())








class Prettifier:
    def test(self):
        print('reach here')

    def __init__(self):
        pass

    '''
    def string_to_html_prepare(self, st):
        st.replace("&", "&amp;")
        st.replace(">", "&gt;")
        st.replace("<", "&lt;")
        st.replace("\"", "&quot;")
        st.replace("\'", "&#39;")
        st.replace(" ", "&nbsp;")
        st.replace("\n", "<br>")
        st.replace("\r", "<br>")
    '''

    def string_to_html(self, color, st):

        _ = "<span style=\" color:#FF0000;\">{}</span>".format(st)
        return _

    def delete_parenthesis(self, st):
        return re.sub('[(,（](.*?)[),）]', '', st)

    def pronounce_annotate(self, kanji, hiragana):
        return '<ruby>{}<rp>(</rp><rt>{}</rt><rp>)</rp></ruby>'.format(kanji, hiragana)

    def change_font(self, st, color=None):  # rgb(254,200,170)
        if color:
            return '<font face = \"宋体\" font size=\"4\" color=\"{}\">{}</font>'.format(color, st)
        else:
            return '<font face= \"宋体\" font size=\"4\" color=\"black\">{}</font>'.format(st)



# 自定义继承自Qmediaplaylist的类
# TODO 关于最开始初始状态的情况
class PlayList(QMediaPlaylist):
    def __init__(self, parent: Window = None):
        super(PlayList, self).__init__()
        self.setObjectName('playlist')
        # UI
        self.parent = parent
        self.playWidget = self.parent.bottomframe

        # list control
        self.indexlist = []
        self.curr_index = 0

        # connects
        self.setconnects()

    def setconnects(self):
        self.mediaInserted.connect(self.inserted)
        self.parent.playbackbutton_ran.clicked.connect(self.set_ranplayback)
        self.parent.playbackbutton_seq.clicked.connect(self.set_seqplayback)
        self.parent.playbackbutton_singleloop.clicked.connect(self.set_singleloopplayback)



    def inserted(self, start, end):
        self.indexlist.append(len(self.indexlist))

    def set_ranplayback(self):
        self.setPlaybackMode(QMediaPlaylist.Random)
        random.shuffle(self.indexlist)

        # 作用是使当前播放的音乐不变，之后的音乐shuffle过后随机取
        self.curr_index = self.indexlist.index(self.currentIndex())
        print(self.indexlist)

    def set_seqplayback(self):
        self.setPlaybackMode(QMediaPlaylist.Sequential)
        self.indexlist.sort()

    def set_singleloopplayback(self):
        self.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

    # 重载两个函数，主要是为了实现自己的random播放
    def next(self):
        if not self.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            if self.curr_index == len(self.indexlist) - 1:
                self.curr_index = 0
            else:
                self.curr_index += 1
        self.setCurrentIndex(self.indexlist[self.curr_index])

    def previous(self):
        if not self.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            if self.curr_index == 0:
                self.curr_index = len(self.indexlist) - 1
            else:
                self.curr_index -= 1
        self.setCurrentIndex(self.indexlist[self.curr_index])




# 真正的音乐播放器
# lyric 感觉应该写入这个类， 也就是包含一个lyric 的变量

class Player(QMediaPlayer):
    def __init__(self, parent: Window = None):   # 标注类型辅助，不知道标注Window好，还是Qframe
        super(Player, self).__init__()
        self.setObjectName('player')
        # UI
        self.parent = parent
        self.playWidget = self.parent.bottomframe  #control widget, 暂时没有用到

        # playlist
        self.playlist = PlayList(self.parent)
        self.setPlaylist(self.playlist)

        self.list_test()

        # song itself
        self.set_media_content(content=QMediaContent(self.playlist.currentMedia()))
        self.song_duration = eyed3.load('/Users/yuhu/Desktop/Lyricplayer/musics/' + 'song1.mp3').info.time_secs

        # lrc thing
        self.lrc = TxtReader(url='/Users/yuhu/Desktop/日语歌曲翻译/歌词翻译txt版/Lemon.txt')
        self.currentLrc = 0
        self.prettifier = Prettifier()

        # connections
        self.setconnects()

    def list_test(self):
        baseurl = '/Users/yuhu/Desktop/Lyricplayer/musics/'
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(baseurl + 'song1.mp3')))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(baseurl + 'song2.mp3')))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(baseurl + 'song3.mp3')))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(baseurl + 'Lemon.mp3')))
        self.playlist.setCurrentIndex(0)

    def setconnects(self):

        #play or pause
        self.parent.playbutton.clicked.connect(self.play_or_pause)
        self.parent.pausebutton.clicked.connect(self.play_or_pause)
        self.parent.pausebutton.hide()
        self.stateChanged.connect(self.state_changed)

        # volume buttem and slider
        self.parent.vmutebutton.clicked.connect(self.set_volume)
        self.parent.volumebutton.clicked.connect(self.mute_volume)
        self.parent.vmutebutton.hide()
        self.parent.volumeslider.setRange(0, 100)
        self.parent.volumeslider.setValue(100)
        self.parent.volumeslider.sliderMoved.connect(self.set_volume)

        #song position
        self.positionChanged.connect(self.position_changed)
        self.parent.progress_slider.sliderMoved.connect(self.position_set)
        self.parent.progress_slider.setRange(0, self.song_duration)

        #next prev
        self.parent.nextbutton.clicked.connect(self.next_song)
        self.parent.prevbutton.clicked.connect(self.prev_song)

    def set_media_content(self, url=None, content=None):
        if url:
            Qurl = QUrl.fromLocalFile(url)
            content = QMediaContent(Qurl)
            self.setMedia(content)
        elif content:
            self.setMedia(content)
        else:
            print('no available content')

    # controls when play
    def play_or_pause(self):
        if self.playlist.mediaCount() == 0:
            print('no songs in the list')
            return

        if self.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
            self.play()
            self.parent.pausebutton.show()

        elif self.state() == QMediaPlayer.PlayingState:
            self.pause()
            self.parent.pausebutton.hide()
        else:
            pass

    def state_changed(self, state):
        print('state is {}'.format(self.state()))
        if state == QMediaPlayer.StoppedState:
            self.currentLrc = 0

        elif state == QMediaPlayer.PlayingState:
            self.parent.playbutton.hide()
            self.parent.pausebutton.show()

        elif state == QMediaPlayer.PausedState:
            self.parent.pausebutton.hide()
            self.parent.playbutton.show()

    def mute_volume(self):
        self.setVolume(0)
        self.parent.volumebutton.hide()
        self.parent.vmutebutton.show()

    def set_volume(self):
        self.setVolume(self.parent.volumeslider.value())
        self.parent.vmutebutton.hide()
        self.parent.volumebutton.show()

    def position_set(self, position):
        value = position * 1000
        self.setPosition(value)

        for i in range(0, self.lrc.block_amount):
            if value < self.lrc.timeaxis_lst[i]:
                self.currentLrc = max(0, i - 1)
                break

    def next_song(self):
        self.playlist.next()
        self.set_media_content(content=self.playlist.currentMedia())
        self.play()

    def prev_song(self):
        self.playlist.previous()
        self.set_media_content(content=self.playlist.currentMedia())
        self.play()

    def position_changed(self, position):
        self.parent.progress_slider.setValue(position / 1000)

        def min_sec(x):
            return '{}'.format(int(x / 60)).zfill(2) + ':' + '{}'.format(int(x % 60)).zfill(2)

        self.parent.songtimelabel.setText('{}/{}'.format(min_sec(position / 1000), min_sec(self.song_duration)))

        if self.currentLrc >= self.lrc.block_amount:
            return

        if position > self.lrc.timeaxis_lst[self.currentLrc]:
            self.lrc_show()
            self.currentLrc += 1

    # lrc and related
    def lrc_show(self):    #how to show lrc
        self.parent.lrc_textBrowser.setPlainText('')
        analyzer_no_parenthesis = self.prettifier.delete_parenthesis(
            self.lrc.analyzer_lst[self.currentLrc])
        self.parent.lrc_textBrowser.append(analyzer_no_parenthesis)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())


