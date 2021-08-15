from first import  *

from usbcdc import *
from ymodem import  *

import PyQt5.QtWidgets as PQW
import PyQt5.QtCore as PQC

class MyWindow(QtWidgets.QWidget, Ui_Form):

    signal_OneParameter = PQC.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.cdc =UsbCdc()
        self.cdc.open()
        self.ymodem_sender = YMODEM(self.cdc.sender_getc,self.cdc.sender_putc)

        self.fileName =''
        self.setupUi(self)
        self.btn_push_file_2.clicked.connect(self.msg)
        self.btn_del_file.clicked.connect(self.delMp3File)
        self.btn_play_music.clicked.connect(self.playMp3File)
        self.btn_push_file.clicked.connect(self.pushFile)
        self.progressBar.setValue(0)

        self.signal_OneParameter.connect(self.setValue_OneParameter)

    def delMp3File(self):
        self.cdc.sender_putc('atdele'.encode())
        print('play mp3 file')

    def playMp3File(self):
        self.cdc.sender_putc('atplay'.encode())
        print('delete mp3 file')
    def setValue_OneParameter(self, value):
        self.progressBar.setValue(value)


    def upgrade_callback(self,total_packets, file_size,file_name):
        print(int(total_packets * 100/file_size), '%')
        self.signal_OneParameter.emit(int(total_packets * 100/file_size))

    def ymodem_send(self,file):
        self.cdc.sender_putc('atpush'.encode())

        try:
            file_stream = open(file, 'rb')
        except IOError as e:
            raise Exception("Open file fail!")
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file)

        #   rate = baudratebox.get()

        #   try:
        #       serial_reconnect(baud_rate = int(rate), timeout=5)
        #   except Exception as e:
        #      messagebox.showinfo(title="Error", message="Connection error！")
        #       return

        try:
            self.ymodem_sender.send(file_stream, file_name, file_size,callback=self.upgrade_callback)
        except Exception as e:
            file_stream.close()
            raise
        file_stream.close()

    def msg(self, Filepath):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "*.mp3")
        print('hh ：', directory)
        self.fileName = directory[0]
        self.fileT.setText(self.fileName)

    def pushFile(self):
        upgrade_thread = threading.Thread(target=self.ymodem_send, args=(self.fileName,))
        upgrade_thread.start()
