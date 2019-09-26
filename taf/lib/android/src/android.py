####################################################################
# This is android python library of Test Automation Framework.
####################################################################

import os
import subprocess


class android():

    def __init__(self):
        pass

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
            pass
        except Exception as error:
            return (False, error)


if __name__ == "__main__":
    objMain = android()
    objMain.startAppium()
    objMain.stopAppium()
    objMain.startAppium()
    objMain.stopAppium()
