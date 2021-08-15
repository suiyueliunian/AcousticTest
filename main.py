# coding=utf-8


from ctypes import *
import serial.tools.list_ports
import threading
from ymodem import YMODEM
import os

import PyQt5.QtCore as PQC
from time import sleep

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWidget import *


ser = serial.Serial(bytesize=8, parity='N', stopbits=1, timeout=1, write_timeout=3)
linsten_lock = threading.Lock()

def sender_getc(size):
    return ser.read(size) or None


def sender_putc(data):
    send_data_mutex.acquire()
    ser.write(data)
    send_data_mutex.release()

ymodem_sender = YMODEM(sender_getc, sender_putc)



def upgrade_callback(total_packets, file_size, file_name):
    print(round(float(total_packets)/file_size,4)*100,'%')
#    myWin.changeProgress(round(float(total_packets)/file_size,4)*100)

def ymodem_send(file):
    global ymodem_sender
    ser.write('atpush'.encode())

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
        ymodem_sender.send(file_stream, file_name, file_size, callback=upgrade_callback)
    except Exception as e:
        file_stream.close()
        raise
    file_stream.close()





send_data_mutex = threading.Lock()




def sendMp3File(self):
    print('dddddd')
    upgrade_thread = threading.Thread(target=ymodem_send,args = ("./1.txt",))
    upgrade_thread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    for port in serial.tools.list_ports.comports():
        print(port.hwid,port.name)
        if port.hwid.find('2C7C:6001')>=0 and port.hwid.find('x.5')>=0:
            ser.port = port.name
            ser.baudrate = 115200  # int(baud_rate)
            ser.open()
            break

    myWin = MyWindow()
    myWin.connectPushFile(sendMp3File)
    myWin.show()
    myWin.show()
    sys.exit(app.exec_())

