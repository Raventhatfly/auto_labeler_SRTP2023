import json

from ui import Ui_MainWindow
import sys
from PyQt5.QtGui import QIcon  # 用于添加图标
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot
from ui_data import UI_data


class Test_window(QMainWindow, Ui_MainWindow):  # 继承至界面文件的主窗口类

    def __init__(self):
        super().__init__()  # 使用超类，继承父类的属性及方法
        self.setupUi(self)  # 构造窗体界面
        # self.setWindowIcon(QIcon("./img/result.png"))
        self.setWindowTitle("Test_button")  # 设置窗体主体
        self.data = UI_data()
        self.data.load_defualt()
        self.initUI()


    def initUI(self):
        self.pushButtonDefault1.clicked.connect(self.default1_callback)
        self.pushButtonConfirm.clicked.connect(self.confirm_callback)
        self.ButtonSelectPart1.clicked.connect(self.select1_callback)
        self.ButtonDelete1.clicked.connect(self.delete1_callback)
        self.ButtonSelectPart2.clicked.connect(self.select2_callback)
        self.ButtonDelete2.clicked.connect(self.delete2_callback)
        self.ButtonAddAnswer1.clicked.connect(self.addAnswer1_callback)
        self.ButtonAddAnswer2.clicked.connect(self.addAnswer2_callback)
        self.pushButtonGenerate.clicked.connect(self.generate_callback)

    def select1_callback(self):
        if self.textEdit_SelfDefine1.toPlainText() == "":
            self.listWidgetWrite1.addItem(self.listWidgetQuestion1.currentItem().text())
        else:
            self.listWidgetWrite1.addItem(self.textEdit_SelfDefine1.toPlainText())
    def delete1_callback(self):
        selected_items = self.listWidgetWrite1.selectedItems()
        if selected_items:
            for item in selected_items:
                self.listWidgetWrite1.takeItem(self.listWidgetWrite1.row(item))
    def select2_callback(self):
        if self.textEdit_SelfDefine2.toPlainText() == "":
            self.listWidgetWrite2.addItem(self.listWidgetQuestion2.currentItem().text())
        else:
            self.listWidgetWrite2.addItem(self.textEdit_SelfDefine2.toPlainText())

    def delete2_callback(self):
        selected_items = self.listWidgetWrite2.selectedItems()
        if selected_items:
            for item in selected_items:
                self.listWidgetWrite2.takeItem(self.listWidgetWrite2.row(item))

    def default1_callback(self):
        # self.data.load_defualt()
        self.textEdit_w.setText(str(self.data.width))
        self.textEdit_h.setText(str(self.data.height))
        self.textEdit.setText(str(self.data.fps))
        self.textEdit_len1.setText(str(self.data.length_minute))
        self.textEdit_len2.setText(str(self.data.length_second))
    def confirm_callback(self):
        self.data.width = int(self.textEdit_w.toPlainText())
        self.data.height = int(self.textEdit_h.toPlainText())
        self.data.fps = int(self.textEdit.toPlainText())
        self.data.path = self.textEdit_path.toPlainText()
        self.data.num_frames = (int(self.data.length_minute)*60+self.data.length_second)+int(self.data.fps)
        if self.listWidget_class.currentItem() is not None:
            self.data.class_name = self.listWidget_class.currentItem().text()
        text = "Number of frames:" + str(self.data.num_frames) + "\n"\
             + "Frame Rate:" + str(self.data.fps) + "\n" + "Width:" + str(self.data.width) + "\n"\
             + "Height:" + str(self.data.height) + "\n" + "Class:" + self.data.class_name
        self.textBrowserInfo.setText(text)

    def addAnswer1_callback(self):
        if self.textEditAnswer1.toPlainText() != "":
            question = self.listWidgetWrite1.currentItem().text()
            answer = self.textEditAnswer1.toPlainText()
            self.data.questions1[question] = answer
            self.listWidgetWrite1.currentItem().setText(question + " Answer: " + answer)
            print(self.data.questions1)

    def addAnswer2_callback(self):
        if (self.textEditAnswer2.toPlainText() != "") and (self.textEditTime1 != "") and (self.textEditTIme2 != ""):
            question = self.listWidgetWrite2.currentItem().text()
            answer = self.textEditAnswer2.toPlainText()
            time_stamp = (int(self.textEditTime1.toPlainText()) * 60 + int(self.textEditTIme2.toPlainText())) * self.data.fps
            result = (answer,time_stamp)
            self.data.questions2[question] = result
            self.listWidgetWrite2.currentItem().setText(question + " Answer: " + answer + " Time: "+ str(time_stamp))
            print(self.data.questions2)

    def generate_callback(self):
        if self.textEditFileName.toPlainText() != "":
            self.data.file_name = self.textEditFileName.toPlainText()
        self.data.file_name += ".json"
        print(self.data.file_name)
        with open(self.data.file_name,"w") as file:
            dict = self.data.defaut_data.copy()
            dict["caption"] = self.textEdit_desciprition.toPlainText()
            dict["info"]["w"] = self.data.width
            dict["info"]["h"] = self.data.height
            dict["info"]["fps"] = self.data.fps
            dict["info"]["num_frame"] = self.data.num_frames
            # for question, answer in self.data.questions1:
            #     dict["global"].append({"question":question,"answer":answer})
            json.dump(dict,file,indent=1)
