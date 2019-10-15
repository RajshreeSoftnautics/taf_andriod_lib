####################################################################
# This is main script of Test Automation Framework.
# User have to run this script with command line arguments.
# It will take inputes from config.xml file and set prerequisite.
# It will also generate report and send email.
####################################################################

import os
import sys
import time
import getopt
from multiprocessing import Process
import src.common
import src.sendemail
import src.reportgenerator
import lib.android.src.android

from robot.api import ExecutionResult, ResultVisitor

totalSuite = 0
passedSuite = 0
failedSuite = 0
statistics = {}
suiteResult = {}

CONFIG_FILE_PATH = "config/config.xml"
ROBOT_ARG_FILE_PATH = "config/robotarg.txt"
ROBOT_LOG_DIR_PATH = "results"


class suiteresults(ResultVisitor):

    def start_suite(self, suite):
        try:
            suiteList = suite.tests
            if not suiteList:
                pass
            else:
                global totalSuite
                totalSuite += 1
                if suite.status == "PASS":
                    global passedSuite
                    passedSuite += 1
                else:
                    global failedSuite
                    failedSuite += 1

                global suiteResult
                suiteResult[suite.name] = {}
                suiteResult[suite.name]["doc"] = str(suite.doc)
                suiteResult[suite.name]["tags"] = None
                suiteResult[suite.name]["status"] = str(suite.status)
                suiteResult[suite.name]["failmsg"] = str(suite.message)
                suiteResult[suite.name]["starttime"] = str(suite.starttime)
                suiteResult[suite.name]["endtime"] = str(suite.endtime)
                suiteResult[suite.name]["runtime"] = str(
                    (suite.elapsedtime/float(1000))/60)
                suiteResult["total"] = str(totalSuite)
                suiteResult["pass"] = str(passedSuite)
                suiteResult["fail"] = str(failedSuite)

        except Exception as error:
            return (False, error)


class testresults(ResultVisitor):

    def visit_test(self, test):
        try:
            global statistics
            statistics[test.name] = {}
            statistics[test.name]["doc"] = str(test.doc)
            statistics[test.name]["tags"] = ", ".join(test.tags)
            statistics[test.name]["status"] = str(test.status)
            statistics[test.name]["failmsg"] = str(test.message)
            statistics[test.name]["starttime"] = str(test.starttime)
            statistics[test.name]["endtime"] = str(test.endtime)
            statistics[test.name]["runtime"] = str(
                (test.elapsedtime/float(1000))/60)

        except Exception as error:
            return(False, error)


class main():

    def __init__(self):
        self.platform = None
        self.tests = None
        self.parallel = False
        self.testsToRun = ""
        self.testsToSkip = ""
        self.testResult = {}
        self.testStatistics = {}
        self.suiteStatistics = {}
        self.deviceList = []
        self.commonObj = src.common.common()
        self.sendmailObj = src.sendemail.sendemail()
        self.reportObj = src.reportgenerator.reportgenerator()
        self.andLibObj = lib.android.src.android.android()

    def _suiteStatistics(self, xmlFileList):
        """
        Method to return suite statistics.
        Args:
        xmlFileList: robot output xml file(s) list
        """
        for suite in xmlFileList:
            if os.path.exists(suite):
                result = ExecutionResult(suite)
                result.visit(suiteresults())
            else:
                print("xml file not found: " + str(suite))

    def _testStatistics(self, xmlFileList):
        """
        Method to return test statistics.
        Args:
        xmlFileList: robot output xml file(s) list
        """
        for test in xmlFileList:
            if os.path.exists(test):
                result = ExecutionResult(test)
                result.visit(testresults())
                stats = result.statistics
                global statistics
                statistics["total"] = stats.total.all.total
                statistics["pass"] = stats.total.all.passed
                statistics["fail"] = stats.total.all.failed
                testSuiteName = test.split("/")[-1]
                self.testResult[testSuiteName] = statistics
                statistics = {}
            else:
                print("xml file not found: " + str(test))

        return(self.testResult)

    def _usage(self):
        """
        Usage print
        """
        self.help = """
                     ##############################
                     Test Automation Framework Help
                     ##############################

                     Arguments:
                     **********
                     -c/--component: Provide android/ios component.
                                     This is mandatory if your test runs over\
 android or ios.

                     -t/--testsuite: Provide absolute path of Test Suite.
                                     This is mandatory tag.

                     -i/--include: Select test cases to run by tag.

                     -e/--exclude: Select test cases not to run by tag.

                     -p/--parallel: Run parallel execution over all connected\
 android/iOS device/emulator(s). (Works with android/iOS component only.)

                     -h/--help: Print Usage.

                     Examples:
                     *********
                     1) python main.py -c android -t \
/home/xyz/automation/Mobile.robot
                     2) python main.py -c iOS -p -t \
"/home/xyz/automation/iOS.robot /home/xyz/automation/Mobile.robot"
                     3) python main.py -c cloud -t \
"/home/xyz/automation/iOS.robot /home/xyz/automation/Mobile.robot" \
-i "reg_01 reg_09"
                     4) python main.py -t "/home/xyz/automation/iOS.robot \
/home/xyz/automation/Mobile.robot" -e reg_07
                    """
        print(self.help)

    def argParser(self):
        """
        Command line argument parser
        """
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'c:t:i:e:ph',
                                       ['component=', 'testsuite=',
                                        'include=', 'exclude=', 'parallel=',
                                        'help='])
        except getopt.GetoptError:
            self._usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self._usage()
                sys.exit(2)
            elif opt in ('-c', '--component'):
                self.platform = arg
            elif opt in ('-t', '--testsuite'):
                self.tests = arg
            elif opt in ('-i', '--include'):
                self.testsToRun = arg
            elif opt in ('-e', '--exclude'):
                self.testsToSkip = arg
            elif opt in ('-p', '--parallel'):
                self.parallel = True
            else:
                self._usage()
                sys.exit(2)

    def _configParser(self):
        """
        Parse config.xml data into python env variable
        """
        try:
            self.configDict = self.commonObj.xmlToDictConverter(
                CONFIG_FILE_PATH)

            # common section
            os.environ["environment"] = str(self.configDict['TAF']['common']
                                            ['environment'])
            os.environ["release"] = str(self.configDict['TAF']['common']
                                        ['release'])

            # email section
            os.environ["emailprotocol"] = str(self.configDict['TAF']['email']
                                              ['protocol'])
            os.environ["emailport"] = str(self.configDict['TAF']['email']
                                          ['port'])
            os.environ["emailserver"] = str(self.configDict['TAF']['email']
                                            ['smtpserver'])
            os.environ["emailfrom"] = str(self.configDict['TAF']['email']
                                          ['from'])
            os.environ["emailpassword"] = str(self.configDict['TAF']['email']
                                              ['password'])
            os.environ["emailto"] = str(self.configDict['TAF']['email']['to'])
            os.environ["emailcc"] = str(self.configDict['TAF']['email']['cc'])
            os.environ["emailbcc"] = str(self.configDict['TAF']['email']
                                         ['bcc'])
            os.environ["emailsubject"] = str(self.configDict['TAF']['email']
                                             ['subject'])
            os.environ["emailbody"] = str(self.configDict['TAF']['email']
                                          ['body'])

        except Exception as error:
            return (False, error)

    def _setPrerequisite(self):
        """
        Set prerequisite and command line error handling
        """
        try:
            if self.tests is None:
                self._usage()
                sys.exit(1)
            else:
                self.testList = self.tests.split()

            for suite in self.testList:
                if not os.path.isfile(suite):
                    print("Provide correct test suite path")
                    sys.exit(1)

            if self.platform is None:
                pass
            elif self.platform.lower() == "android":
                # set config android environment variables
                os.environ["platform"] = "Android"
                os.environ["apkpath"] = str(self.configDict['TAF']['android']
                                            ['apkpath'])
                os.environ["apppkg"] = str(self.configDict['TAF']['android']
                                           ['apppkg'])
                os.environ["appactivity"] = str(self.configDict['TAF']
                                                ['android']['appactivity'])

                # get connected device(s) list
                self.deviceList = self.andLibObj.getConnectedDeviceList()
                if self.deviceList:
                    self.device = []
                    for device in self.deviceList:
                        for key, value in device.items():
                            if value == "offline":
                                print("Device in offline mode...")
                                sys.exit(1)
                            else:
                                self.device.append(key)
                else:
                    print("Connected device or emulator Not Found...")
                    sys.exit(1)
            elif self.platform.lower() == "ios":
                os.environ["platform"] = "iOS"
            elif self.platform.lower() == "cloud":
                pass  # set cloud prerequisite
            else:
                print("Provide correct component\n")
                self._usage()
                sys.exit(1)

        except Exception as error:
            return (False, error)

    def robotRun(self, UDID, appiumPort, systemPort):
        """
        Run given test suite(s) using robot framework,
        generate report and send email
        """
        try:
            includeTags = self.testsToRun.split()
            includeCmd = ""
            for tag in includeTags:
                includeCmd += "-i " + tag + " "

            excludeTags = self.testsToSkip.split()
            excludeCmd = ""
            for tag in excludeTags:
                excludeCmd += "-e " + tag + " "

            xmlResultList = []
            self.robotResultList = []

            remoteURL = "http://localhost:" + str(appiumPort) + "/wd/hub"
            for testSuite in self.testList:
                robotCmd = ""
                currentDate = time.strftime("%Y-%m-%d")
                currentTime = time.strftime("%Y%m%d-%H%M%S")
                if not os.path.exists(ROBOT_LOG_DIR_PATH + "/" + currentDate):
                    os.makedirs(ROBOT_LOG_DIR_PATH + "/" + currentDate)

                testSuiteName = testSuite.split("/")[-1].split(".")[0]
                robotCmd = "robot -o output-" + testSuiteName + "-" + \
                           UDID + "_" + currentTime
                robotCmd += " -l log-" + testSuiteName + "-" + UDID + "_" + \
                            currentTime
                robotCmd += " -r report-" + testSuiteName + "-" + \
                            UDID + "_" + currentTime
                robotCmd += " -d " + ROBOT_LOG_DIR_PATH + "/" + \
                            currentDate + "/"
                robotCmd += " "
                robotCmd += includeCmd
                robotCmd += excludeCmd
                robotCmd += "-v remoteURL:" + remoteURL + " -v deviceName:" \
                            + UDID + " -v systemPort:" + str(systemPort)
                robotCmd += " -A " + ROBOT_ARG_FILE_PATH + " " + testSuite

                os.system(robotCmd)

                # collect robot result(s)
                xmlResultList.append(ROBOT_LOG_DIR_PATH + "/" + currentDate
                                     + "/output-" + testSuiteName + "-"
                                     + UDID + "_" + currentTime + ".xml")
                self.robotResultList.append(ROBOT_LOG_DIR_PATH + "/"
                                            + currentDate + "/log-"
                                            + testSuiteName + "-" + UDID
                                            + "_" + currentTime + ".html")
                self.robotResultList.append(ROBOT_LOG_DIR_PATH + "/"
                                            + currentDate + "/report-"
                                            + testSuiteName + "-" + UDID + "_"
                                            + currentTime + ".html")

            self.robotResultList.extend(xmlResultList)

            # generate result call
            self._suiteStatistics(xmlResultList)
            self.testStatistics = self._testStatistics(xmlResultList)
            self.suiteStatistics = suiteResult
            commonConfig = self.configDict['TAF']['common']

            xlsReportPath = ROBOT_LOG_DIR_PATH + "/" + currentDate + \
                "/" + "Summary-Report-" + currentTime + ".xlsx"

            self.reportObj.xlsReport(commonConfig, self.suiteStatistics,
                                     self.testStatistics, xlsReportPath)
            self.robotResultList.append(xlsReportPath)
            print("\n##########################################")
            print("Summary Report PATH: " + str(xlsReportPath))
            print("##########################################\n")

        except Exception as error:
            return (False, error)

    def suiteExecuter(self):
        if self.platform.lower() == "android" and self.parallel is True:
            appiumPort = 4722
            systemPort = 8199
            for UDID in self.device:
                appiumPort = int(appiumPort) + 1
                systemPort = int(systemPort) + 1
                process = Process(target=self.robotRun, args=(UDID,
                                  appiumPort, systemPort, ))
                process.start()
            process.join()

        elif self.platform.lower() == "android" and self.parallel is False:
            appiumPort = 4723
            systemPort = 8200
            self.robotRun(self.device[0], appiumPort, systemPort)

    def sendEmail(self):
        try:
            if os.environ["emailto"] == 'None':
                toAddr = []
            else:
                toAddr = os.environ["emailto"].split(",")
            if os.environ["emailcc"] == 'None':
                ccAddr = []
            else:
                ccAddr = os.environ["emailcc"].split(",")
            if os.environ["emailbcc"] == 'None':
                bccAddr = []
            else:
                bccAddr = os.environ["emailbcc"].split(",")

            # send email call
            print("Email Sending...")
            self.sendmailObj.sendEmail(os.environ["emailprotocol"],
                                       os.environ["emailserver"],
                                       os.environ["emailport"],
                                       os.environ["emailsubject"],
                                       os.environ["emailfrom"],
                                       os.environ["emailpassword"],
                                       toAddr, ccAddr, bccAddr,
                                       os.environ["emailbody"],
                                       self.robotResultList)

        except Exception as error:
            return (False, error)


if __name__ == "__main__":
    objMain = main()
    if len(sys.argv) < 1:
        objMain._usage()
    objMain.argParser()
    objMain._configParser()
    objMain._setPrerequisite()
    objMain.suiteExecuter()
    objMain.sendEmail()
