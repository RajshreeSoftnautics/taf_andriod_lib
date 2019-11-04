####################################################################
# This is android python library of Test Automation Framework.
####################################################################

import os
import re
import subprocess
import time


class android():

    def __init__(self):
        self.devices = []
        self.deviceDict = {}

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

    def startScreenRecording(self, deviceId, saveFilePath):
        """
        start connected device screen recording
        Args:
        deviceId: connected device id
        saveFilePath: save recorded file location
        """
        try:
            cmd = ""
            cmd += "scrcpy --no-display -s " + str(deviceId)
            cmd += " -r " + str(saveFilePath) + ".mp4"
            os.system(cmd)

        except Exception as error:
            return (False, error)
