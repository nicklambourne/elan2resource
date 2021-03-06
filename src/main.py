import sys
from PyQt5.QtWidgets import QApplication
from widgets.icon import ApplicationIcon
from windows import PrimaryWindow

if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.setWindowIcon(ApplicationIcon())
    Main = PrimaryWindow(App)
    Main.show()
    sys.exit(App.exec_())
