import json

from type_changer_ui import Ui_MainWindow
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, Qt
import copy

class Test_window(QMainWindow, Ui_MainWindow):

    path_prefix = "D:/ZJUI/SRTP/数据标注/电影/"
    class_type = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon/img.png"))
        self.setWindowTitle("Json Generator")
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.pushButton_callback)
        self.listWidget.clicked.connect(self.show_class_callback)
        self.pushButton_2.clicked.connect(self.write_json_callback)

    def pushButton_callback(self):
        text = self.textEdit.toPlainText()
        try:
            num = int(text)
            num += 1
            self.textEdit.setText(str(num))
        except:
            pass

    def show_class_callback(self):
        self.class_type = self.listWidget.currentItem().text()
        self.label_class.setText(self.class_type)

    def write_json_callback(self):
        file_name = self.textEdit.toPlainText() + ".json"
        path = self.path_prefix + file_name
        print(path)
        try:
            with open(path,'r') as f:
                content = json.load(f)
                if self.class_type is not None:
                    content['info']['class'] = self.class_type
                print(content)
        except:
            print("failed")
        else:
            with open(path,'w') as f:
                json.dump(content,f,indent=1)
                QMessageBox.warning(self, "Success!", "File "+file_name+" has been modified.", QMessageBox.Cancel)