import serial
from time import sleep
import os
import subprocess
from get_nic.getnic import interfaces
from threading import Thread


def startPing():
    ETHs = interfaces()
    while True:
        for eth in ETHs:
            Thread(target=ping, args=(eth))
        sleep(60)


def ping(eth, server='goggle.com', count=3, wait_sec=1):
    cmd = "ping -c {} -W {} -i {}".format(count, wait_sec, eth, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-2].split(',')[3].split()[1]
        loss = lines[-2].split(',')[2].split()[0]
        timing = lines[-1].split()[3].split('/')
        print(loss)
        return {
            'type': 'rtt',
            'min': timing[0],
            'avg': timing[1],
            'max': timing[2],
            'mdev': timing[3],
            'total': total,
            'loss': loss,
        }
    except Exception as e:
        print(e)
        return None


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