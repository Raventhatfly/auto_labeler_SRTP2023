import json

from ui import Ui_MainWindow
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
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
        self.ButtoFileIncre.clicked.connect(self.increment_callback)

    def select1_callback(self):
        if self.data.current_questions1 >= 5:
            QMessageBox.warning(self, "Warning", "Reaches Maximum Data Records(5 Records)", QMessageBox.Cancel)
            return
        if self.listWidgetQuestion1.currentItem() is None and self.textEdit_SelfDefine1.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Plase select a question.", QMessageBox.Cancel)
            return
        if self.textEdit_SelfDefine1.toPlainText() == "":
            selected_item = self.listWidgetQuestion1.currentItem()
            # if selected_item.listWidget()==self.listWidgetQuestion2:
            self.listWidgetWrite1.addItem(selected_item.text())
            row = self.listWidgetQuestion1.row(selected_item)
            self.listWidgetQuestion1.takeItem(row)
        else:
            self.listWidgetWrite1.addItem(self.textEdit_SelfDefine1.toPlainText())
        self.data.current_questions1 = self.data.current_questions1 + 1


    def delete1_callback(self):
        selected_items = self.listWidgetWrite1.selectedItems()
        if selected_items:
            text = ""
            for item in selected_items:
                text = item.text()
                self.listWidgetWrite1.takeItem(self.listWidgetWrite1.row(item))
            question = text.split(' Answer:')[0]
            self.listWidgetQuestion1.addItem(question)
            print(self.data.questions1)
            if question in self.data.questions1:
                self.data.questions1.pop(question)
            print(self.data.questions1)
            self.data.current_questions1 = self.data.current_questions1 - 1


    def select2_callback(self):
        if self.data.current_questions2 >= 15:
            QMessageBox.warning(self, "Warning", "Reaches Maximum Data Records(15 Records)", QMessageBox.Cancel)
            return
        if self.listWidgetQuestion2.currentItem() is None and self.textEdit_SelfDefine2.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Plase select a question.", QMessageBox.Cancel)
            return
        if self.textEdit_SelfDefine2.toPlainText() == "":
            selected_item = self.listWidgetQuestion2.currentItem()
            # if selected_item.listWidget()==self.listWidgetQuestion2:
            self.listWidgetWrite2.addItem(selected_item.text())
            row = self.listWidgetQuestion2.row(selected_item)
            self.listWidgetQuestion2.takeItem(row)
        else:
            self.listWidgetWrite2.addItem(self.textEdit_SelfDefine2.toPlainText())
        self.data.current_questions2 = self.data.current_questions2 + 1
        print(self.data.current_questions2)

    def delete2_callback(self):
        selected_items = self.listWidgetWrite2.selectedItems()
        if selected_items:
            text = ""
            for item in selected_items:
                text = item.text()
                self.listWidgetWrite2.takeItem(self.listWidgetWrite2.row(item))
            question = text.split(' Answer:')[0]
            self.listWidgetQuestion2.addItem(question)
            print(self.data.questions2)
            if question in self.data.questions2:
                self.data.questions2.pop(question)
            print(self.data.questions2)
            self.data.current_questions2 = self.data.current_questions2 - 1

    def default1_callback(self):
        # self.data.load_defualt()
        self.textEdit_w.setText(str(self.data.width))
        self.textEdit_h.setText(str(self.data.height))
        self.textEdit.setText(str(self.data.fps))
        self.textEdit_len1.setText(str(self.data.length_minute))
        self.textEdit_len2.setText(str(self.data.length_second))
    def confirm_callback(self):
        try:
            self.data.width = int(self.textEdit_w.toPlainText())
            self.data.height = int(self.textEdit_h.toPlainText())
            self.data.fps = int(self.textEdit.toPlainText())
            self.data.path = self.textEdit_path.toPlainText()
            self.data.num_frames = (int(self.data.length_minute)*60+self.data.length_second) * int(self.data.fps)
            if self.listWidget_class.currentItem() is not None:
                self.data.class_name = self.listWidget_class.currentItem().text()
            text = "Number of frames:" + str(self.data.num_frames) + "\n"\
                 + "Frame Rate:" + str(self.data.fps) + "\n" + "Width:" + str(self.data.width) + "\n"\
                 + "Height:" + str(self.data.height) + "\n" + "Class:" + self.data.class_name + "\n"\
                 + "Path:" + str(self.data.path)
            self.textBrowserInfo.setText(text)
        except:
            QMessageBox.warning(self, "Warning", "Please fill in all the box in Basic Settings or press Use Default!", QMessageBox.Cancel)

    def addAnswer1_callback(self):
        if self.textEditAnswer1.toPlainText() != "":
            question = self.listWidgetWrite1.currentItem().text()
            answer = self.textEditAnswer1.toPlainText()
            self.data.questions1[question] = answer
            self.listWidgetWrite1.currentItem().setText(question + " Answer: " + answer)
            print(self.data.questions1)

    def addAnswer2_callback(self):
        if self.textEditAnswer2.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Please fill in the answer!", QMessageBox.Cancel)
        elif self.textEditTime1.toPlainText()=="" or self.textEditTIme2.toPlainText()=="":
            QMessageBox.warning(self, "Warning", "Please fill in the time!", QMessageBox.Cancel)
        elif (self.textEditAnswer2.toPlainText() != "") and (self.textEditTime1.toPlainText() != "") and (self.textEditTIme2.toPlainText() != ""):
            question = self.listWidgetWrite2.currentItem().text()
            answer = self.textEditAnswer2.toPlainText()
            time_stamp = (int(self.textEditTime1.toPlainText()) * 60 + int(self.textEditTIme2.toPlainText())) * self.data.fps
            result = (answer,time_stamp)
            self.data.questions2[question] = result
            self.listWidgetWrite2.currentItem().setText(question + " Answer: " + answer + " Time: "+ str(time_stamp))
            print(self.data.questions2)

    def generate_callback(self):
        if self.data.current_questions1 < 5 or self.data.current_questions2 < 15:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle("Confirmation")
            message_box.setText("Global Questions less than 5 or BreakPoint questions less than 15.\nAre you sure you want to proceed?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)

            result = message_box.exec_()
            if result == QMessageBox.Yes:
                print("User chose 'Yes'. Proceeding...")
                # Your action or function call goes here
            else:
                print("User chose 'No'. Action canceled.")
                return
        if self.textEditFileName.toPlainText() != "":
            self.data.file_name = self.textEditFileName.toPlainText()
        self.data.file_name += ".json"
        print(self.data.file_name)
        path = "json_generated/" + self.data.file_name
        print(path)
        with open(path,"w") as file:
            dict = self.data.defaut_data.copy()

            dict["caption"] = self.textEdit_desciprition.toPlainText()
            dict["info"]["w"] = self.data.width
            dict["info"]["h"] = self.data.height
            dict["info"]["fps"] = self.data.fps
            dict["info"]["video_path"] = self.data.path
            dict["info"]["num_frame"] = self.data.num_frames
            dict["info"]["video_path"] = self.data.path
            for question, answer in self.data.questions1.items():
                dict["global"].append({"question":question,"answer":answer})
            print(self.data.questions2)
            for question, data in self.data.questions2.items():
                dict["breakpoint"].append({"time":data[1],"question":question,"answer":data[0]})
            json.dump(dict,file,indent=1)
            print("global questions number:%d"%self.data.current_questions1)
            print("breakpoint questions number:%d"%self.data.current_questions2)



    def increment_callback(self):
        try:
            number = int(self.textEditFileName.toPlainText())
            number = number + 1
            self.data.file_name = str(number)
            self.textEditFileName.clear()
            self.textEditFileName.setText(self.data.file_name)
        except:
            pass
