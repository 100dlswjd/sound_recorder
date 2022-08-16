import sys
import os
import winsound

from MyClass.recorde import recorder

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QCloseEvent
from ui.main_form import Ui_MainWindow

from threading import Thread

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self.recorder = recorder()
        self.recorde_flag = False
        self.btn_recorde.clicked.connect(self.recorde_handler)
        self.btn_play.clicked.connect(self.play_handler)
        self.save_file_name = "output.wav"
        self.save_file_path = resource_path(self.save_file_name)
    
    def recorde_handler(self):
        if self.recorde_flag:
            # 중지
            self.recorder.recorde_stop()
            self.btn_recorde.setText("▶")
            self.btn_play.setEnabled(True)
            self.recorde_thread = None
            pass
        else:
            # 녹음
            self.recorde_thread = Thread(target=self.thread_proc)
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.recorde_thread.start()
            self.btn_recorde.setText("정지")
            self.btn_play.setEnabled(False)
        self.recorde_flag = not(self.recorde_flag)
    
    def thread_proc(self):
        self.recorder.recorde_start()
    
    def play_handler(self):
        self.recorder.save_wav(self.save_file_path)
        winsound.PlaySound(self.save_file_path, winsound.SND_ASYNC)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()