import sys
from Lyricwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QFileDialog, QListWidgetItem
from PyQt5 import QtWidgets

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import *

from PyQt5.QtMultimedia import *
import eyed3
from TxtReader import TxtReader
import re
import random

import time
from PyQt5.QtWidgets import QFontDialog
from TEST import Prettifier
'''
问题汇总：
1。 durationchanged
2。 为何用Endofmedia无法自动切换到下一个歌曲，找到原因，是因为status会变为loaded media导致进入stopped状态。
    目前用一个wanna play的flag进行解决
3. 如果一个槽函数正在执行，一个新的信号发射了，会怎么样
'''

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    # path = '/Users/yuhu/Music/网易云音乐/東山奈央/夏祭り.mp3'
    path = '/Users/yuhu/Desktop/Lyricplayer/musics/Lemon.mp3'

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.player = Player(self)

        with open('QSS/playerbutton.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


'''
class PlayListWindow(QFrame):
    def __init__(self, parent=None):
        super(PlayListWindow, self).__init__()
        self.setParent(parent)
'''

class ListWidgetItem(QListWidgetItem):
    def __init__(self, url, index):
        super(ListWidgetItem, self).__init__()
        self.url = url
        self.index = index  # 列表中的第index首歌

# 自定义继承自Qmediaplaylist的类
# TODO 关于最开始初始状态的情况，无歌单的初始化

class PlayList(QMediaPlaylist):
    double_clicked_inlist = pyqtSignal(str)

    def __init__(self, parent: Window = None):
        super(PlayList, self).__init__()
        self.setObjectName('playlist')
        # UI
        self.parent = parent
        self.playWidget = self.parent.bottomframe

        self.parent.frame_list.hide()

        # list control
        self.parent.playbackbutton_1.show()
        self.parent.playbackbutton_2.hide()
        self.parent.playbackbutton_3.hide()
        self.setPlaybackMode(QMediaPlaylist.Sequential)

        self.indexlist = []
        self.curr_index = 0
        self.str_urllist = []  # used for urls store


        # connects
        self.setconnects()

    # text: 1 : ran, 2 : seq, 3 : loop
    def setconnects(self):
        # playback mode control
        self.mediaInserted.connect(self.inserted)
        self.parent.playbackbutton_2.clicked.connect(self.set_ranplayback)
        self.parent.playbackbutton_3.clicked.connect(self.set_seqplayback)
        self.parent.playbackbutton_1.clicked.connect(self.set_singleloopplayback)

        # playlistWidget
        self.parent.pushButton_listshow.clicked.connect(self.show_or_hide)
        self.parent.playlistWidget.itemDoubleClicked.connect(self.set_song)
        self.parent.list_hidebutton.clicked.connect(self.show_or_hide)

    def inserted(self, start, end):
        self.indexlist.append(len(self.indexlist))
        newsong = ListWidgetItem(self.str_urllist[start], start)
        newsong.setText(self._getname_from_url(self.str_urllist[start]) + '  index {}'.format(start))
        self.parent.playlistWidget.addItem(newsong)

    def _getname_from_url(self, url: str):
        return url.split('/')[-1][:-4]


    def set_ranplayback(self):
        self.setPlaybackMode(QMediaPlaylist.Random)
        random.shuffle(self.indexlist)
        # 作用是使当前播放的音乐不变，之后的音乐shuffle过后随机取
        self.curr_index = self.indexlist.index(self.currentIndex())
        self.parent.playbackbutton_3.show()
        self.parent.playbackbutton_1.hide()
        self.parent.playbackbutton_2.hide()
        print(self.indexlist)

    def set_seqplayback(self):
        self.setPlaybackMode(QMediaPlaylist.Sequential)
        self.indexlist.sort()
        self.curr_index = self.indexlist.index(self.currentIndex())
        self.parent.playbackbutton_1.show()
        self.parent.playbackbutton_2.hide()
        self.parent.playbackbutton_3.hide()

    def set_singleloopplayback(self):
        self.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        self.parent.playbackbutton_2.show()
        self.parent.playbackbutton_1.hide()
        self.parent.playbackbutton_3.hide()

    def get_currenturl(self):
        return self.str_urllist[self.indexlist[self.curr_index]]

    def get_current_whichsong(self):
        return self.indexlist[self.curr_index]

    # 重载两个函数，主要是为了实现自己的random播放, 这样父类的content的list就会保持不变，随时通过index去取用即可
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

    def show_or_hide(self):
        if self.parent.frame_list.isVisible():
            self.parent.frame_list.hide()
        else:
            self.parent.frame_list.show()

    # 由于这个类中访问不到player，所以无法set content，所以想到发射信号。
    def set_song(self, listwidgetitem: ListWidgetItem):

        self.curr_index = self.indexlist.index(listwidgetitem.index)
        self.setCurrentIndex(listwidgetitem.index)
        self.double_clicked_inlist.emit(listwidgetitem.url)



# 真正的音乐播放器
# lyric 感觉应该写入这个类， 也就是包含一个lyric 的变量

class Player(QMediaPlayer):

    finish2next = pyqtSignal()  # ??

    def __init__(self, parent: Window = None):   # 标注类型辅助，不知道标注Window好，还是Qframe
        super(Player, self).__init__()
        self.setObjectName('player')
        # UI
        self.parent = parent
        self.playWidget = self.parent.bottomframe  #control widget, 暂时没有用到

        # playlist
        self.playlist = PlayList(self.parent)
        self.setPlaylist(self.playlist)

        # song itself
        self.set_media_content(content=QMediaContent(self.playlist.currentMedia()))
        self.song_duration = 0
        if not self.playlist.mediaCount() == 0:
            self.set_song_duration()
            self.parent.progress_slider.setRange(0, self.song_duration)
        self.wannaplay = False

        # lrc thing
        self.lrc = TxtReader(url='/Users/yuhu/Desktop/日语歌曲翻译/歌词翻译txt版/Lemon.txt')
        self.currentLrc = 0
        self.prettifier = Prettifier()

        # connections
        self.setconnects()



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

        #list thing
        self.parent.nextbutton.clicked.connect(self._next_song)
        self.parent.prevbutton.clicked.connect(self._prev_song)
        self.finish2next.connect(self.next_song)
        self.playlist.double_clicked_inlist.connect(self._set_song_from_list)

        #media changed
        self.mediaChanged.connect(self.song_changed)
        self.mediaStatusChanged.connect(self.status_changed)

        # file and related
        self.parent.openfilebutton.clicked.connect(self.openfile)

    def openfile(self):
        fd = QFileDialog(self.parent)
        fd.setNameFilter("Musics (*.mp3)")
        fd.setViewMode(QFileDialog.Detail)
        fd.setFileMode(QFileDialog.ExistingFiles)
        if fd.exec():
            filenames = fd.selectedFiles()
            for i in filenames:
                self.add_media_and_url(i)
        else:
            print('didnt choose any file!')

    def set_song_duration(self):
        self.song_duration = eyed3.load(self.playlist.get_currenturl()).info.time_secs

    def add_media_and_url(self, url: str):
        if 'http' in url or 'file' in url:
            tmpurl = QUrl(url)
        else:
            tmpurl = QUrl.fromLocalFile(url)
        content = QMediaContent(tmpurl)
        # 下面两句话的顺序不可改变，涉及到信号和槽
        self.playlist.str_urllist.append(url)  # 暂时不传tmpurl， 若涉及网络需要传tmpurl 可以再改
        self.playlist.addMedia(content)

    def _set_song_from_list(self, url: str):
        self.wannaplay = True
        self.set_media_content(url=url)


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
        if state == QMediaPlayer.StoppedState:
            self.parent.pausebutton.hide()
            self.parent.playbutton.show()
            self.currentLrc = 0

            #self.next_song() #这个如果加上，本意是为了歌曲截止的时候跳转，但会出现问题

        elif state == QMediaPlayer.PlayingState:
            self.parent.playbutton.hide()
            self.parent.pausebutton.show()

        elif state == QMediaPlayer.PausedState:
            self.parent.pausebutton.hide()
            self.parent.playbutton.show()

    def status_changed(self, status):
        print(status)

        if status == QMediaPlayer.EndOfMedia:
            # self.next_song() 这句话不能在这里使用，他妈因为这个函数没到完成medialoaded的时候执行不完。
            self.finish2next.emit()

        elif status == QMediaPlayer.LoadedMedia and self.wannaplay:
            self.play()


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

    def song_changed(self):
        self.set_song_duration()
        self.parent.progress_slider.setRange(0, self.song_duration)


    def next_song(self):
        self.playlist.next()
        self.set_media_content(content=self.playlist.currentMedia())
        print('status before play is {}'.format(self.mediaStatus()))
        self.wannaplay = True
        self.play()


        print('already playing')

    def _next_song(self):
        # 主要是为了在单曲循环的条件下，能够切换到下一首, 切换条件与顺序播放相同, 可以用QObject.sender(self).objectName()解决
        if self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.next_song()
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)


    def prev_song(self):
        self.playlist.previous()
        self.set_media_content(content=self.playlist.currentMedia())
        self.wannaplay = True
        self.play()

    def _prev_song(self):  # for singleloop click next button， 主要是为了在单曲循环的条件下，能够切换到下一首, 切换条件与顺序播放相同
        if self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.prev_song()
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

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
    # how to show lrc
    def lrc_show(self):
        self.parent.lrc_textBrowser.setPlainText('')
        analyzer_no_parenthesis = self.prettifier.delete_parenthesis(
            self.lrc.analyzer_lst[self.currentLrc])
        self.parent.lrc_textBrowser.append(analyzer_no_parenthesis)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())


