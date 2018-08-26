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
        self.lrc_reader = TxtReader(url='/Users/yuhu/Desktop/日语歌曲翻译/歌词翻译txt版/Lemon.txt')
        self.current_block = 0

        self.player = QMediaPlayer()
        self.song_duration = eyed3.load(WindowCtrl.path).info.time_secs

        self.player.bufferStatusChanged.connect(self.bufferingProgress)
        self.player.durationChanged.connect(self.duration_changed)
        self.playbutton.clicked.connect(self.play_or_pause)
        self.pausebutton.clicked.connect(self.play_or_pause)
        self.openfilebutton.clicked.connect(self.openfiles)
        self.pausebutton.hide()

        self.vmutebutton.clicked.connect(self.set_volume)
        self.volumebutton.clicked.connect(self.mute_volume)
        self.vmutebutton.hide()
        self.volumeslider.setRange(0, 100)
        self.volumeslider.setValue(100)
        self.volumeslider.sliderMoved.connect(self.set_volume)

        self.progress_slider.sliderMoved.connect(self.position_set)
        self.progress_slider.setRange(0, self.song_duration)

        self.lrc_textBrowser.setFont(QFont('宋体', 25))

        h = '<html><body><p style="font-family:verdana;font-size:80%;color:green">\
            This is a paragraph with some text in it. This is a paragraph with some text in it. <br>\
            This is a paragraph with some text in it. This is a paragraph with some text in it.\
            </p>\
            </body>\
            </html>'
        self.ori_webEngineView.setHtml(h)

        with open('QSS/playerbutton.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.prettifier = Prettifier()

        self.player.positionChanged.connect(self.position_changed)
        self.player.stateChanged.connect(self.state_changed)

        self.url = QUrl.fromLocalFile(WindowCtrl.path)
        self.content = QMediaContent(self.url)
        self.player.setMedia(self.content)

    def play_or_pause(self):

        if self.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
            self.player.play()
            self.pausebutton.show()


        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pausebutton.hide()

    def state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.current_block = 0

    def duration_changed(self, duration):
        duration /= 1000

    def setup_slider(self):
        pass

    def position_set(self, position):
        value = position * 1000
        self.player.setPosition(value)

        for i in range(0, self.lrc_reader.block_amount):
            if value < self.lrc_reader.timeaxis_lst[i]:
                self.current_block = max(0, i - 1)
                break

    def mute_volume(self):
        self.player.setVolume(0)
        self.vmutebutton.show()

    def set_volume(self):
        self.player.setVolume(self.volumeslider.value())
        self.vmutebutton.hide()

    def bufferingProgress(self):
        pass

    def position_changed(self, position):
        self.progress_slider.setValue(position / 1000)

        def min_sec(x):
            return '{}'.format(int(x / 60)).zfill(2) + ':' + '{}'.format(int(x % 60)).zfill(2)

        self.songtimelabel.setText('{}/{}'.format(min_sec(position / 1000), min_sec(self.song_duration)))

        if self.current_block >= self.lrc_reader.block_amount:
            return
        if position > self.lrc_reader.timeaxis_lst[self.current_block]:
            self.lrc_textBrowser.setPlainText('')

            analyzer_no_parenthesis = self.prettifier.delete_parenthesis(
                self.lrc_reader.analyzer_lst[self.current_block])
            self.lrc_textBrowser.append(analyzer_no_parenthesis)

            # ori_pron = self.get_block_ori_with_pronounce(self.current_block)
            # ori_chg_font = self.prettifier.change_font(ori_pron)

            # trans = self.prettifier.change_font(self.lrc_reader.trans_lst[self.current_block])
            html = self.lrc_html_for_roller(3)

            self.ori_webEngineView.setHtml(html)

            self.current_block += 1

    ##suitable for odd
    def lrc_html_for_roller(self, line_to_show):
        html = ''
        range_block_to_show = []
        if self.current_block == 0:
            range_block_to_show = range(0, line_to_show)
        elif self.current_block == self.lrc_reader.block_total - 1:
            range_block_to_show = range(self.current_block - line_to_show + 1, self.current_block + 1)
        else:
            range_block_to_show = range(self.current_block - int((line_to_show - 1) / 2), self.current_block +
                                        int((line_to_show - 1) / 2) + 1)

        for i in range_block_to_show:
            if i == self.current_block:
                html += self.prettifier.change_font(self.get_block_ori_with_pronounce(i), color='orange') \
                        + '<br>' + \
                        self.prettifier.change_font(self.lrc_reader.translate_lst[i], color='orange') + '<br>' + '<br>'
            else:
                html += self.prettifier.change_font(self.get_block_ori_with_pronounce(i)) + \
                        '<br>' + self.lrc_reader.translate_lst[i] + '<br>' + '<br>'
            self.prettifier.change_font(html)
        return html

    def get_block_ori_with_pronounce(self, block):
        ori_sentence = self.lrc_reader.original_lst[block].split('.')[1]
        analyze_sentence = self.lrc_reader.analyzer_lst[block]
        pronounce = self.lrc_reader.find_kanji_hiragana(analyze_sentence)

        pronounced_ready = ori_sentence
        for k, v in pronounce.items():
            pronounced_ready = pronounced_ready.replace(k, self.prettifier.pronounce_annotate(k, v))
        return pronounced_ready

    def openfiles(self):
        song = QFileDialog.getOpenFileName(parent=self, caption='Select Song', filter='Sound Files(*.mp3)')
        print(song)


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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())



# 真正的音乐播放器
class Player(QMediaPlayer):
    def __init__(self, parent: Window = None):   # 标注类型辅助，不知道标注Window好，还是Qframe
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent

        self.playWidget = self.parent.bottomframe  #control widget
        self.setPlaylist(QMediaPlaylist())



