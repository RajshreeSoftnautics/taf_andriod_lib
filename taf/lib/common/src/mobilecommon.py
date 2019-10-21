####################################################################
# This is mobile common python library of Test Automation Framework.
####################################################################

import os
import re
import subprocess


class mobilecommon():

    def checkAppiumStatus(self):
        """
        check appium server running or not and return process id list
        """
        try:
            appiumProcess = []
            pid = subprocess.Popen("pgrep [n]ode", shell=True,
                                   stdout=subprocess.PIPE)
            for process in pid.stdout:
                appiumProcess.append(process.decode('utf-8').rstrip())
            return appiumProcess
        except Exception as error:
            return (False, error)

    def stopAppium(self, pid):
        """
        stop appium server
        Args:
        pid: appium server process id
        """
        try:
            state = os.system("kill -9 " + str(pid))
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
