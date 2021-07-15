import serial
from time import sleep
import os
import subprocess
from get_nic.getnic import interfaces
from threading import Thread
import platform
import smtplib


def startPing():
    ETHs = interfaces()
    gmail = Gmail('vivereecombattere@gmail.com', '8d4cfaadd')
    try:
        os.mkdir("/root/check_test")
    except:
        pass
    while True:
        PING_STATUS = False
        for eth in[item for item in ETHs if len(item) >= 3]:
            Thread(target=ping, args=(eth, gmail,)).start()
        sleep(10)
        if PING_STATUS:
            restartEth()
            sleep(30)
        else:
            sleep(50)


def ping(eth, gmail, server='google.com', count=3):
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
        fail.write(str(countLoss))
        fail.close()
        if countLoss == 10:
            global PING_STATUS
            PING_STATUS = True
        elif countLoss == 60:
            gmail.send_message('asd', eth)
        elif countLoss > 60:
            os.remove(os.path.join("/root/check_test/", f"{eth}_state"))

    else:
        try:
            os.remove(os.path.join("/root/check_test/", f"{eth}_state"))
        except:
            pass


class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, subject, eth):
        headers = [
            "From: " + self.email,
            "Subject: " + f"ПК - '{platform.node()}'"+'\n'+f"Сетевой интерфейс '{eth}' недоступен!",
            "To: " + self.email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(self.email, self.email, (headers + "\r\n\r\n" + f"Сетевой интерфейс '{eth}' недоступен!").encode('utf-8'))


class Send:
    def __init__(self, func, *args, **kwargs):
        self.func = func

    def getSerial(self):
        return serial.Serial(self.port, baudrate=self.baudrate)

    def closeSerial(self, serial_: serial.Serial):
        serial_.close()

    def __call__(self, *args, **kwargs):
        self.port = kwargs.get("port", "/dev/ttyUSB0")
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
