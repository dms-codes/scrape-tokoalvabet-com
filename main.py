   def runQt():
    from PyQt6 import uic
    from PyQt6.QtWidgets import QMainWindow,QApplication,QLineEdit,QTextEdit,QPushButton,QLabel,QFileDialog
    from PyQt6.QtGui import QPixmap,QImage
    import os
    import sys

    class UI(QMainWindow):
        def __init__(self):
            super(UI,self).__init__() app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
