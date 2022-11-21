from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from struct import *


COM = "COM6"

# настройки
app = QtWidgets.QApplication([])
ui = uic.loadUi("GUI.ui")  # подключение дизайна окна
ui.setWindowTitle("micro_GUI")  # название окна

serial = QSerialPort()
serial.setBaudRate(115200)
ports = QSerialPortInfo.availablePorts()
port_list = [port.portName() for port in ports]
ui.combo_box.addItems(port_list)


# логика программы -- общение с микроконтроллером
def startRecord():
    message_1: bytes = b'\x7E\x00\xA1\x00\x00\x00\x00\xAB\x7E'
    serial.write(message_1)
    # ui.TL3.setText("wait response")
    print(message_1)


def send_button_clicked():
    print()
    txs = ui.send_number.displayText()
    if txs.count('.') == 0:
        print("send_button_clicked(): it is not float")
        return
    txs = float(txs)
    out = pack('<f', txs)
    output_list = [int(0xE7), out[0], out[1], out[2], out[3]]
    print(out, output_list)
    message = bytearray(output_list)
    print(message)
    serial.write(message)

    #int
    # print()
    # txs = ui.send_number.displayText()
    # txs = int(txs)
    # out = pack('<I', txs)
    # output_list = [int(0xE7), 0, 0, 0, out[0]]
    # print(out, output_list)
    # message = bytearray(output_list)
    # print(message)
    # serial.write(message)



def on_read():
    # if not serial.canReadLine():
    #     print("on_read(): Error")
    #     return
    rx = serial.read(4)
    print(rx)
    try:
        data = unpack('<f', rx)
        print(data[0])
        print(float(data[0]))
        ui.print_number.setText(str(data[0]))
    except Exception as e:
        print(e)


# открыть порт
def on_open():
    serial.setPortName(ui.combo_box.currentText())
    serial.open(QIODevice.ReadWrite)


# закрыть порт
def on_close():
    serial.close()


serial.readyRead.connect(on_read)
ui.open_button.clicked.connect(on_open)
ui.close_button.clicked.connect(on_close)
ui.send_button.clicked.connect(send_button_clicked)

ui.show()
app.exec()
