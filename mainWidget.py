from first import  *


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.fileName =''
        self.setupUi(self)
        self.btn_push_file_2.clicked.connect(self.msg)

    def msg(self, Filepath):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "*.mp3")
        print('hh ：', directory)
        fileName = directory[0]
        self.fileT.setText(fileName)

    def connectPushFile(self,func):
        self.btn_push_file.clicked.connect(func)

    def getFileName(self):
        return  self.fileName

    def changeProgress(self,value):
        self.progressBar.setValue(value)

