import json

from ui import Ui_MainWindow
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, Qt
from ui_data import UI_data
import copy

class Test_window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon/img.png"))
        self.setWindowTitle("Json Generator")
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
        self.ButtonTime30s.clicked.connect(self.plus30s_callback)
        self.ButtonTimePlus1s.clicked.connect(self.plus1s_callback)
        self.ButtonTimeMinus1s.clicked.connect(self.mius1s_callback)
        self.ButtonTimeReset.clicked.connect(self.time_reset_callback)

    def select1_callback(self):
        if self.data.current_questions1 >= 5:
            QMessageBox.warning(self, "Warning", "Reaches Maximum Data Records(5 Records)", QMessageBox.Cancel)
            return
        if self.listWidgetQuestion1.currentItem() is None and self.textEdit_SelfDefine1.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Plase select a question.", QMessageBox.Cancel)
            return
        text = ""
        if self.textEdit_SelfDefine1.toPlainText() == "":
            selected_item = self.listWidgetQuestion1.currentItem()
            text  = selected_item.text()
            self.listWidgetWrite1.addItem(text)
            row = self.listWidgetQuestion1.row(selected_item)
            self.listWidgetQuestion1.takeItem(row)
        else:
            text = self.textEdit_SelfDefine1.toPlainText()
            self.listWidgetWrite1.addItem(text)
            self.textEdit_SelfDefine1.clear()
        self.listWidgetWrite1.setCurrentItem(self.listWidgetWrite1.item(len(self.data.question1_ready_list)))
        self.data.question1_ready_list.append({"question": text, "answer": ""})
        self.show_quesitons_num_info()
        print(self.data.question1_ready_list)
    def select2_callback(self):
        if self.data.current_questions2 >= 15:
            QMessageBox.warning(self, "Warning", "Reaches Maximum Data Records(15 Records)", QMessageBox.Cancel)
            return
        if self.listWidgetQuestion2.currentItem() is None and self.textEdit_SelfDefine2.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Plase select a question.", QMessageBox.Cancel)
            return
        text = ""
        self_define = False
        if self.textEdit_SelfDefine2.toPlainText() == "":
            selected_item = self.listWidgetQuestion2.currentItem()
            text = selected_item.text()
            self.listWidgetWrite2.addItem(selected_item.text())
        else:
            self.listWidgetWrite2.addItem(self.textEdit_SelfDefine2.toPlainText())
            text = self.textEdit_SelfDefine2.toPlainText()
            self_define = True
            self.textEdit_SelfDefine2.clear()
        self.listWidgetWrite2.setCurrentItem(self.listWidgetWrite2.item(len(self.data.question2_ready_list)))
        # data structure: (Time, Question, Answer, Self Defien?)-1 time means time not added
        self.data.question2_ready_list.append({"time":-1,"question":text,"answer":"","self_define":self_define})
        # self.data.current_questions2 = len(self.data.question2_ready_list)
        self.show_quesitons_num_info()
        print(self.data.question2_ready_list)

    def delete1_callback(self):
        selected_item = self.listWidgetWrite1.currentItem()
        if selected_item is not None:
            row = self.listWidgetWrite1.row(selected_item)
            text = selected_item.text()
            self.listWidgetWrite1.takeItem(row)
            question = self.data.question1_ready_list[row]["question"]
            self.data.question1_ready_list.pop(row)
            self.listWidgetQuestion1.addItem(question)
            # self.data.current_questions1 = len(self.data.question1_ready_list)
            self.show_quesitons_num_info()
            print(self.data.question1_ready_list)

    def delete2_callback(self):
        selected_item = self.listWidgetWrite2.currentItem()
        if selected_item is not None:
            row = self.listWidgetWrite2.row(selected_item)
            text = selected_item.text()
            self.listWidgetWrite2.takeItem(row)
            if self.data.question2_ready_list[row]["self_define"] == True:
                self.listWidgetQuestion2.addItem(self.data.question2_ready_list[row]["question"])
            self.data.question2_ready_list.pop(row)
            # self.data.current_questions1 = len(self.data.question1_ready_list)
            self.show_quesitons_num_info()
            print(self.data.question2_ready_list)

    def default1_callback(self):
        self.data.load_defualt()
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
            self.data.length_minute = int(self.textEdit_len1.toPlainText())
            self.data.length_second = int(self.textEdit_len2.toPlainText())
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
        if self.listWidgetWrite1.currentItem() is None:
            QMessageBox.warning(self, "Warning", "Please select the question to add answer with!", QMessageBox.Cancel)
        elif self.textEditAnswer1.toPlainText() != "":
            current_item = self.listWidgetWrite1.currentItem()
            row = self.listWidgetWrite1.row(current_item)
            question = self.data.question1_ready_list[row]["question"]
            answer = self.textEditAnswer1.toPlainText()
            self.data.question1_ready_list[row]["answer"] = answer
            self.listWidgetWrite1.currentItem().setText(question + " Answer: " + answer)
            self.show_quesitons_num_info()
            print(self.data.question1_ready_list)

    def addAnswer2_callback(self):
        if self.textEditAnswer2.toPlainText() == "":
            QMessageBox.warning(self, "Warning", "Please fill in the answer!", QMessageBox.Cancel)
        elif self.textEditTime1.toPlainText()=="" or self.textEditTIme2.toPlainText()=="":
            QMessageBox.warning(self, "Warning", "Please fill in the time!", QMessageBox.Cancel)
        elif self.listWidgetWrite2.currentItem() is None:
            QMessageBox.warning(self, "Warning", "Please select the question to add answer with!", QMessageBox.Cancel)
        elif (self.textEditAnswer2.toPlainText() != "") and (self.textEditTime1.toPlainText() != "") and (self.textEditTIme2.toPlainText() != ""):
            current_item = self.listWidgetWrite2.currentItem()
            row = self.listWidgetWrite2.row(current_item)
            # data structure: (Time, Question, Answer, Self Defien?)-1 time means time not added
            question = self.data.question2_ready_list[row]["question"]
            answer = self.textEditAnswer2.toPlainText()
            self.data.question2_ready_list[row]["answer"] = answer
            try:
                time_stamp = (int(self.textEditTime1.toPlainText()) * 60 + int(self.textEditTIme2.toPlainText())) * self.data.fps
                self.data.question2_ready_list[row]["time"] = time_stamp
                self.listWidgetWrite2.currentItem().setText(question + " Answer: " + answer + " Time: "+ str(time_stamp))
                self.show_quesitons_num_info()
                print(self.data.question2_ready_list)
            except:
                QMessageBox.warning(self, "Warning", "Time stamp must be integers!", QMessageBox.Cancel)


    def generate_callback(self):
        if self.data.current_questions1_with_answer < 5 or self.data.current_questions2_with_answer < 15:
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
        # path = "json_generated/" + self.data.file_name
        path = "D:/ZJUI/SRTP/数据标注/电影/" + self.data.file_name
        print(path)
        try:
            with open(path,'r') as file:
                pass
        except:
            with open(path,"w") as file:
                dict = copy.deepcopy(self.data.defaut_data.copy())
                # dict = self.data.defaut_data.copy()

                dict["caption"] = self.textEdit_desciprition.toPlainText()
                dict["info"]["w"] = self.data.width
                dict["info"]["h"] = self.data.height
                dict["info"]["fps"] = self.data.fps
                dict["info"]["video_path"] = self.data.path
                dict["info"]["num_frame"] = self.data.num_frames
                dict["info"]["video_path"] = self.data.path
                dict["info"]["class"] = self.data.class_name
                for data1 in self.data.question1_ready_list:
                    if data1["answer"] != "":
                        dict["global"].append({"question":data1["question"],"answer":data1["answer"]})
                for data2 in self.data.question2_ready_list:
                    if data2["answer"] != "":
                        dict["breakpoint"].append({"time":data2["time"],"question":data2["question"],"answer":data2["answer"]})
                json.dump(dict,file,indent=1)
                print(self.data.defaut_data)
            # self.listWidgetWrite1.clear()
            self.listWidgetWrite2.clear()
            # self.data.question1_ready_list = []
            self.data.question2_ready_list = []
            # self.data.current_questions1 = 0
            self.data.current_questions2 = 0
            # self.data.current_questions1_with_answer = 0
            self.data.current_questions2_with_answer = 0
            self.show_quesitons_num_info()


        else:
            QMessageBox.warning(self, "Warning",
                                "File already exists. Change the file name or delete the original one.",
                                QMessageBox.Cancel)

    def increment_callback(self):
        try:
            number = int(self.textEditFileName.toPlainText())
            number = number + 1
            self.data.file_name = str(number)
            self.textEditFileName.clear()
            self.textEditFileName.setText(self.data.file_name)
        except:
            pass

    def plus30s_callback(self):
        try:
            minutes = int(self.textEditTime1.toPlainText())
            seconds = int(self.textEditTIme2.toPlainText())
            seconds = seconds + 30
            if seconds >= 60:
                seconds -= 60
                minutes += 1
            self.textEditTime1.setText(str(minutes))
            self.textEditTIme2.setText(str(seconds))
        except:
            QMessageBox.warning(self, "Warning",
                                "Please enter integer time!",
                                QMessageBox.Cancel)

    def plus1s_callback(self):
        try:
            minutes = int(self.textEditTime1.toPlainText())
            seconds = int(self.textEditTIme2.toPlainText())
            seconds = seconds + 1
            if seconds >= 60:
                seconds -= 60
                minutes += 1
            self.textEditTime1.setText(str(minutes))
            self.textEditTIme2.setText(str(seconds))
        except:
            QMessageBox.warning(self, "Warning",
                                "Please enter integer time!",
                                QMessageBox.Cancel)

    def mius1s_callback(self):
        try:
            minutes = int(self.textEditTime1.toPlainText())
            seconds = int(self.textEditTIme2.toPlainText())
            seconds = seconds - 1
            if seconds < 0:
                seconds += 60
                minutes -= 1
                if minutes < 0 :
                    minutes = 0
                    seconds = 0
            self.textEditTime1.setText(str(minutes))
            self.textEditTIme2.setText(str(seconds))
        except:
            QMessageBox.warning(self, "Warning",
                                "Please enter integer time!",
                                QMessageBox.Cancel)

    def time_reset_callback(self):
        self.textEditTime1.setText(str(0))
        self.textEditTIme2.setText(str(0))

    def get_num_answered(self,ready_list):
        num = 0
        for iter in ready_list:
            if iter["answer"] != "":
                num += 1
        return num

    def show_quesitons_num_info(self):
        num_q1 = len(self.data.question1_ready_list)
        num_q2 = len(self.data.question2_ready_list)
        self.data.current_questions1 = num_q1
        self.data.current_questions2 = num_q2
        num_answered_q1 = self.get_num_answered(self.data.question1_ready_list)
        num_answered_q2 = self.get_num_answered(self.data.question2_ready_list)
        self.data.current_questions1_with_answer = num_answered_q1
        self.data.current_questions2_with_answer = num_answered_q2
        text1 = "Total:"+str(num_q1)+" Answered:"+str(num_answered_q1) + " Fps:"+str(self.data.fps)
        text2 = "Total:" + str(num_q2) + " Answered:" + str(num_answered_q2) + " Fps:"+str(self.data.fps)
        self.label_num_1.setText(text1)
        self.label_num_2.setText(text2)

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        text = event.text()

        # Handle the key press event based on the key code and modifiers
        # print("Key Pressed:", text)
        # print("Key Code:", key)
        # print("Modifiers:", modifiers)

        # if key == Qt.Key_Up:
        #     print("Up key was pressed.")
        #     if self.textEditAnswer2.hasFocus():
        #         print("history")
        if key == Qt.Key_Return:
            if self.listWidgetQuestion1.currentItem() is not None:
                self.select1_callback()
            if self.listWidgetQuestion2.currentItem() is not None:
                self.select2_callback()
