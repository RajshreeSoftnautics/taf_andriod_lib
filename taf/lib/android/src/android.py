####################################################################
# This is android python library of Test Automation Framework.
####################################################################

import os
import re
import subprocess


class android():

    def __init__(self):
        self.devices = []
        self.deviceDict = {}

    def checkAppiumServerStatus(self):
        try:
            pid = subprocess.Popen("pgrep [n]ode", shell=True,
                                   stdout=subprocess.PIPE)
            return pid.stdout.readline().decode('utf-8').rstrip()
        except Exception as error:
            return (False, error)

    def stopAppium(self, port=4723):
        """
        stop appium server
        Args:
        port: port number on which appium server runs
        """
        try:
            state = os.system("kill $(lsof -t -i:" + str(port) + ")")
            return state
        except Exception as error:
            return (False, error)

    def startAppium(self, port=4723):
        """
        start appium server
        Args:
        port: port number on which appium server runs
        """
        try:
            state = subprocess.Popen("appium -p " + str(port),
                                     shell=True,
                                     stdout=subprocess.PIPE)
            while True:
                if "started" in state.stdout.readline().decode("UTF-8"):
                    break
            return True
        except Exception as error:
            return (False, error)

    def getConnectedDeviceList(self):
        """
        gives list of connected emulator(s) and real device(s)
        """
        try:
            deviceList = (subprocess.check_output(["adb", "devices"])
                          .decode('utf-8').split("\n"))
            deviceList = deviceList[1:]
            deviceList = list(filter(None, deviceList))
            for device in deviceList:
                deviceId, deviceStatus = re.split(r'\s+', device, maxsplit=1)
                self.deviceDict[deviceId] = deviceStatus
            if self.deviceDict:
                self.devices.append(self.deviceDict)
            return self.devices

        except Exception as error:
            return (False, error)
