import sys
from PyQt5.QtWidgets import QApplication
from type_changer_window import Test_window

def main():
    app = QApplication(sys.argv)
    ui = Test_window()
    ui.show()
    sys.exit(app.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()