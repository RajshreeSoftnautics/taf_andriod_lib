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
import src.common
import src.sendemail
import src.reportgenerator

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
        self.testsToRun = ""
        self.testsToSkip = ""
        self.testResult = {}
        self.testStatistics = {}
        self.suiteStatistics = {}
        self.commonObj = src.common.common()
        self.sendmailObj = src.sendemail.sendemail()
        self.reportObj = src.reportgenerator.reportgenerator()

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
                     -c/--component: Provide entry component\
(ex: android/iOS/cloud).

                     -t/--testsuite: Provide absolute path of Test Suite.
                                     This is mandatory tag.

                     -i/--include: Select test cases to run by tag.

                     -e/--exclude: Select test cases not to run by tag.

                     -h/--help: Print Usage.

                     Examples:
                     *********
                     1) python main.py -c android -t \
/home/xyz/automation/Mobile.robot
                     2) python main.py -c iOS -t \
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
            opts, args = getopt.getopt(sys.argv[1:], 'c:t:i:e:h',
                                       ['component=', 'testsuite=',
                                        'include=', 'exclude=', 'help='])
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

            os.environ["environment"] = str(self.configDict['TAF']['common']
                                            ['environment'])
            os.environ["release"] = str(self.configDict['TAF']['common']
                                        ['release'])

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
                pass  # set android prerequisite
            elif self.platform.lower() == "ios":
                pass  # set ios prerequisite
            elif self.platform.lower() == "cloud":
                pass  # set cloud prerequisite
            else:
                print("Provide correct component\n")
                self._usage()
                sys.exit(1)

        except Exception as error:
            return (False, error)

    def robotRun(self):
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
            robotResultList = []

            for testSuite in self.testList:
                robotRunCmd = ""
                currentDate = time.strftime("%Y-%m-%d")
                currentTime = time.strftime("%Y%m%d-%H%M%S")
                if not os.path.exists(ROBOT_LOG_DIR_PATH + "/" + currentDate):
                    os.makedirs(ROBOT_LOG_DIR_PATH + "/" + currentDate)

                testSuiteName = testSuite.split("/")[-1].split(".")[0]
                robotRunCmd = "robot -o output-" + testSuiteName + "-" + \
                              currentTime
                robotRunCmd += " -l log-" + testSuiteName + "-" + currentTime
                robotRunCmd += " -r report-" + testSuiteName + "-" + \
                               currentTime
                robotRunCmd += " -d " + ROBOT_LOG_DIR_PATH + "/" + \
                               currentDate + "/"
                robotRunCmd += " "
                robotRunCmd += includeCmd
                robotRunCmd += excludeCmd
                robotRunCmd += " -A " + ROBOT_ARG_FILE_PATH + " " + testSuite

                os.system(robotRunCmd)

                # collect robot result(s)
                xmlResultList.append(ROBOT_LOG_DIR_PATH + "/" + currentDate
                                     + "/output-" + testSuiteName + "-"
                                     + currentTime + ".xml")
                robotResultList.append(ROBOT_LOG_DIR_PATH + "/" + currentDate
                                       + "/log-" + testSuiteName + "-"
                                       + currentTime + ".html")
                robotResultList.append(ROBOT_LOG_DIR_PATH + "/" + currentDate
                                       + "/report-" + testSuiteName + "-"
                                       + currentTime + ".html")
            robotResultList.extend(xmlResultList)

            # generate result call
            self._suiteStatistics(xmlResultList)
            self.testStatistics = self._testStatistics(xmlResultList)
            self.suiteStatistics = suiteResult
            commonConfig = self.configDict['TAF']['common']

            xlsReportPath = ROBOT_LOG_DIR_PATH + "/" + currentDate + \
                "/" + "Summary-Report-" + currentTime + ".xlsx"

            self.reportObj.xlsReport(commonConfig, self.suiteStatistics,
                                     self.testStatistics, xlsReportPath)
            robotResultList.append(xlsReportPath)
            print("\n##########################################")
            print("Summary Report PATH: " + str(xlsReportPath))
            print("##########################################\n")

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
                                       robotResultList)

        except Exception as error:
            return (False, error)


if __name__ == "__main__":
    objMain = main()
    if len(sys.argv) < 1:
        objMain._usage()
    objMain.argParser()
    objMain._configParser()
    objMain._setPrerequisite()
    objMain.robotRun()
