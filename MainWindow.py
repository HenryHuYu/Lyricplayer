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
from PyQt5.QtWidgets import QFontDialog


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    # path = '/Users/yuhu/Music/网易云音乐/東山奈央/夏祭り.mp3'
    path = '/Users/yuhu/Music/网易云音乐/Lemon.mp3'

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.current_block = 0

        self.player = Player(self)


        self.lrc_textBrowser.setFont(QFont('宋体', 25))

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


# 真正的音乐播放器
# lyric 感觉应该写入这个类， 也就是包含一个lyric 的变量

class Player(QMediaPlayer):
    def __init__(self, parent: Window = None):   # 标注类型辅助，不知道标注Window好，还是Qframe
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent

        self.playWidget = self.parent.bottomframe  #control widget
        self.song_duration = eyed3.load(Window.path).info.time_secs

        self.lrc = TxtReader(url='/Users/yuhu/Desktop/日语歌曲翻译/歌词翻译txt版/Lemon.txt')
        self.currentLrc = 0

        self.url = QUrl.fromLocalFile(Window.path)
        self.content = QMediaContent(self.url)
        self.setMedia(self.content)

        self.setconnects()


    def setconnects(self):
        self.durationChanged.connect(self.duration_changed)
        self.bufferStatusChanged.connect(self.buffering_progress)
        self.positionChanged.connect(self.position_changed)

        self.parent.playbutton.clicked.connect(self.play_or_pause)
        self.parent.pausebutton.clicked.connect(self.play_or_pause)

        self.parent.pausebutton.hide()

        self.parent.vmutebutton.clicked.connect(self.set_volume)
        self.parent.volumebutton.clicked.connect(self.mute_volume)
        self.parent.vmutebutton.hide()
        self.parent.volumeslider.setRange(0, 100)
        self.parent.volumeslider.setValue(100)
        self.parent.volumeslider.sliderMoved.connect(self.set_volume)

        self.parent.progress_slider.sliderMoved.connect(self.position_set)
        self.parent.progress_slider.setRange(0, self.song_duration)


    def duration_changed(self, duration):
        print(duration)
        duration /= 1000

    def buffering_progress(self, buffer):
        print(buffer)

    def play_or_pause(self):
        if self.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
            self.play()
            self.parent.pausebutton.show()

        elif self.state() == QMediaPlayer.PlayingState:
            self.pause()
            self.parent.pausebutton.hide()

    def state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.currentLrc = 0

    def mute_volume(self):
        self.setVolume(0)
        self.parent.volumebutton.hide()
        self.parent.vmutebutton.show()

    def set_volume(self):
        self.setVolume(self.parent.volumeslider.value())
        print(self.parent.volumeslider.value())
        self.parent.vmutebutton.hide()
        self.parent.volumebutton.show()

    def position_set(self, position):
        value = position * 1000
        self.setPosition(value)

        for i in range(0, self.lrc.block_amount):
            if value < self.lrc.timeaxis_lst[i]:
                self.currentLrc = max(0, i - 1)
                break

    def position_changed(self, position):
        self.parent.progress_slider.setValue(position / 1000)

        def min_sec(x):
            return '{}'.format(int(x / 60)).zfill(2) + ':' + '{}'.format(int(x % 60)).zfill(2)

        self.parent.songtimelabel.setText('{}/{}'.format(min_sec(position / 1000), min_sec(self.song_duration)))

        if self.currentLrc >= self.lrc.block_amount:
            return
        if position > self.lrc.timeaxis_lst[self.currentLrc]:
            self.parent.lrc_textBrowser.setPlainText('')

            analyzer_no_parenthesis = self.prettifier.delete_parenthesis(
                self.lrc.analyzer_lst[self.currentLrc])
            self.parent.lrc_textBrowser.append(analyzer_no_parenthesis)

            self.currentLrc += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())


