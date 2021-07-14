import serial
from time import sleep
import os
import subprocess
from get_nic.getnic import interfaces
from threading import Thread


def startPing():
    ETHs = interfaces()
    os.mkdir("/root/check_test")
    while True:
        PING_STATUS = False
        for eth in[item for item in ETHs if len(item) >= 3]:
            Thread(target=ping, args=(eth)).start()
        sleep(5)
        if PING_STATUS:
            restartEth()
            sleep(35)
        else:
            sleep(55)


def ping(eth, server='goggle.com', count=3):
    cmd = "ping -c {} -I {} {}".format(count, eth, server).split(' ')
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode()
    lines = output.split("\n")
    loss = int(lines[-3].split(',')[2].split()[0][:-1])

    if loss == 100:
        try:
            countLoss = int(open(f"/root/check_test/{eth}_state", "r").read())
        except:
            countLoss = 0

        fail = open(f"/root/check_test/{eth}_state", "w")
        countLoss += 1
        fail.write(countLoss)
        fail.close()
        if countLoss == 10:
            global PING_STATUS
            PING_STATUS = True
    else:
        try:
            os.remove(os.path.join("/root/check_test/", f"{eth}_state"))
        except:
            pass


class Send:
    def __init__(self, func, *args, **kwargs):
        self.func = func

    def getSerial(self):
        return serial.Serial(self.port, baudrate=self.baudrate)

    def closeSerial(self, serial_: serial.Serial):
        serial_.close()

    def __call__(self, *args, **kwargs):
        self.baudrate = kwargs.get("baudrate", 9600)
        self.port = kwargs.get("port", "COM3")
        self.baudrate = kwargs.get("baudrate", 9600)
        self.data = kwargs.get("data", None)

        serial_ = self.getSerial()
        if self.data: self.func(self, serial_, self.data)
        else: self.func(self, serial_)
        self.closeSerial(serial_)

    def write(self, serial_: serial.Serial, data:str):
        serial_.write(data.encode('utf-8'))


@Send
def startEth(self: Send, serial):
    self.write(serial, "L1HIGH")
    sleep(10)
    self.write(serial, "L2HIGH")


@Send
def restartEth(self: Send, serial):
    self.write(serial, "L1LOW")
    sleep(5)
    self.write(serial, "L2LOW")
    sleep(5)
    self.write(serial, "L1HIGH")
    sleep(10)
    self.write(serial, "L2HIGH")


@Send
def shutdownEth(self: Send, serial):
    self.write(serial, "L1LOW")
    sleep(5)
    self.write(serial, "L2LOW")
    sleep(5)
    os.system('shutdown now')


@Send
def rebootEth(self: Send, serial):
    self.write(serial, "L1LOW")
    sleep(5)
    self.write(serial, "L2LOW")
    sleep(5)
    os.system('reboot now')


@Send
def arduino(self: Send, serial, data):
    self.write(serial, data)


if __name__ == '__main__':
    startPing()