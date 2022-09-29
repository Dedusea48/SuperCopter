from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


app = QtWidgets.QApplication([])
ui = uic.loadUi("copter.ui")
ui.setWindowTitle("SerialGUI")

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo.availablePorts()
for port in ports:
    portList.append(port.portName())
# ui.comL.addItems(portList)  #Добавление портов в combobox

def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    print(data)

def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)

def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    # print(txs)
    serial.write(txs.encode())

def onClose():
    serial.close()

def ledControl(val):
    print(val)

def fanControl(val):
    print(val)

def bulbControl(val):
    print(val)

serial.readyRead.connect(onRead)

# ui.openB.clicked.connect(onOpen)
# ui.closeB.clicked.connect(onClose)

# ui.ledC.stateChanged.connect(ledControl)

vals = [10, 11, 12]
serialSend(vals)

ui.show()
app.exec()