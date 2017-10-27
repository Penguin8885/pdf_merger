import sys
import os
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel)

from PyPDF2 import PdfFileMerger

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() #ウィンドウ初期化関数を呼び出し

    ##ウィンドウの初期化
    def initUI(self):
        self.setAcceptDrops(True) #アクセプトにしておくことでドラッグ&ドロップができる

        ##ウィンドウのレイアウトを構成
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(QLabel("drag and drop pdf files"))
        self.setLayout(self.mainLayout)
        ##ウィンドウの場所・サイズ・タイトルを決める
        self.setGeometry(300, 300, 120, 100)
        self.setWindowTitle('pdf merger')
        ##最後にウィンドウを表示
        self.show()

    ##ドラッグされたときにする処理
    def dragEnterEvent(self, event):
        event.accept() #アクセプトにしておくことでドラッグ&ドロップができる

    ##ドラッグ&ドロップされたときにする処理
    def dropEvent(self, event):
        event.accept() #アクセプトにしておくことでドラッグ&ドロップができる
        paths = [u.toLocalFile() for u in event.mimeData().urls()] #ドラッグ&ドロップされたファイルのパスをQt形式から通常の形式に変換
        for path in paths:
            _, ext = os.path.splitext(path) #ファイルパスを拡張子とそれ以外に分割
            if ext != '.pdf':
                return #変なファイルが混ざってたら何もしない
        merge_pdf(paths, os.path.dirname(paths[0])) #指定されたパスのファイルをマージする


def merge_pdf(file_paths, save_path):
    merger = PdfFileMerger() #マージ機を立ち上げる
    for file_ in file_paths:
        merger.append(file_) #PDFファイルを後ろに順にくっつけていく
    merger.write(save_path + '/merge' + datetime.datetime.today().strftime("%Y%m%d%H%M%S") + '.pdf') #mergeYYYYMMDDHHMMSS.pdfの名前で出力
    merger.close() #マージ機を終了させる

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())