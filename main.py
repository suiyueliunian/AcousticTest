# coding=utf-8


from ctypes import *
import serial.tools.list_ports
import threading
from ymodem import YMODEM
import os
from time import sleep

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from first import *


ser = serial.Serial(bytesize=8, parity='N', stopbits=1, timeout=1, write_timeout=3)
linsten_lock = threading.Lock()


def upgrade_callback(total_packets, file_size, file_name):
    print('hhh')



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



def sender_getc(size):
    return ser.read(size) or None


def sender_putc(data):
    send_data_mutex.acquire()
    ser.write(data)
    send_data_mutex.release()


send_data_mutex = threading.Lock()
ymodem_sender = YMODEM(sender_getc, sender_putc)




def main():
    ser.port = "com30"
    ser.baudrate = 115200  # int(baud_rate)
    ser.open()
    print("hhh")
    ymodem_send("./1.txt")

def sendMp3File(self):
    print('dddddd')
    upgrade_thread = threading.Thread(target=ymodem_send,args = ("./1.txt",))
    upgrade_thread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ser.port = "com30"
    ser.baudrate = 115200  # int(baud_rate)
    ser.open()

    myWin = MyWindow()
    myWin.connectPushFile(sendMp3File)
    myWin.show()
    sys.exit(app.exec_())

