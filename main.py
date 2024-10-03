import sys
from PyQt5 import QtWidgets
from ui.skeleton import Skeleton

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Skeleton()
    sys.exit(app.exec_())
