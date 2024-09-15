import sys
from PyQt5 import QtWidgets
from ui.main_page import MainPage

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MainPage()
    sys.exit(app.exec_())
