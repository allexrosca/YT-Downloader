import sys
import ctypes
from PySide2 import QtCore, QtWidgets, QtGui
from UI import YTDownloaderUI


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    user32 = ctypes.windll.user32
    interface = YTDownloaderUI()
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    interface.resize(int(width - width / 3), int(height - height / 4))
    interface.show()
    interface.buttons['Exit'].clicked.connect(app.exit)
    sys.exit(app.exec_())
