import serial
from time import sleep
import os
import subprocess
from get_nic.getnic import *
from threading import Thread
import platform
import smtplib


def startPing():
    IPs = ['192.168.11.100',
        '192.168.12.100',
        '192.168.13.100',
        '192.168.14.100',
        '192.168.15.100',
        '192.168.16.100',
        '192.168.17.100',
        '192.168.18.100',
        '192.168.19.100',
        '192.168.20.100',
        '192.168.21.100',
        '192.168.22.100',
        '192.168.23.100',
        '192.168.24.100',
        '192.168.25.100',
        '192.168.26.100',
        '192.168.27.100',
        '192.168.28.100',
        '192.168.29.100',
        '192.168.30.100'
     ]
    try:
        os.mkdir("/root/check_test")
    except:
        pass
    while True:

        PING_STATUS = False
        print("[INFO] SLEEPING 60 SECONDS!")
        for ip in IPs:
            Thread(target=ping, args=(ip, )).start()
        sleep(20)
        print(PING_STATUS)

        if PING_STATUS:
            print("[INFO] RESTART ETH!")
            restartEth()
            sleep(20)
        else:
            sleep(40)


def ping(ip, server='1.1.1.1', count=3, ct=False):
    command = "ping -c {} -I {} {}".format(count, ip, server)
    cmd = command.split(' ')
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode()
    lines = output.split("\n")
    try:
        try:
            loss = float(lines[-3].split(',')[2].split()[0][:-1])
        except:
            loss = 100
        if loss == 100 and ct:
            try:
                countLoss = int(open(f"/root/check_test/{ip}_state", "r").read())
            except:
                countLoss = 0
            print(f"[INFO] command - ", command, f", loss - {loss}", f", count Loss - {countLoss}")

            fail = open(f"/root/check_test/{ip}_state", "w")
            fail.write(str(countLoss))
            print(countLoss, str(countLoss))
            fail.close()

            if countLoss == 10:
                global PING_STATUS
                PING_STATUS = True
                print(PING_STATUS)

            elif countLoss == 60:
                gmail = Gmail('vivereecombattere@gmail.com', '8d4cfaadd')
                gmail.send_message('', ip)
                os.remove(os.path.join("/root/check_test/", f"{ip}_state"))

        elif not ct and loss == 100:
            ping(ip, server, ct=True)
        else:
            try:
                #print(f"[INFO] command - ", command, f", loss - {loss}")
                os.remove(os.path.join("/root/check_test/", f"{ip}_state"))
            except:
                pass
    except BaseException as e:
        print(f"{'-'*49}\n[INFO] ERROR - {e};\n PING OUT - {output}")


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
            "Subject: " + f"ПК - '{platform.node()}'"+'\n'+f"Сетевой интерфейс '{eth}' недоступен!",
            ]
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
        print(data)
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
    gmail = Gmail('vivereecombattere@gmail.com', '8d4cfaadd')
    gmail.send_message("", "TEST")