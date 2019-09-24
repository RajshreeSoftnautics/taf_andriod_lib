# Test Automation Framework

It will run given test suite(s) using robot framework and create summary xlsx report using robot framework output.xml file and send email with all result attachments to one or more users given in config file.

### Prerequisites
* Linux System
* Python 3.x.x
* Robot Framework

### Installing

* Python 3 (https://www.python.org/downloads/) 
* pip3 (sudo apt install python3-pip)
* Robot Framework (pip3 install robotframework)
* xmltodict (pip3 install xmltodict)
* json (pip3 install jsonlib)
* openpyxl (pip3 install openpyxl)

## How to use

### Test Configuration

* Go to taf/config/config.xml file and provide appropriate data.
* If user want to use any robot framework command line options rather than(-o, -l, -r, -d, -i, -e, -A) then go to taf/config/robotarg.txt file and add that all command line options.

### Run Test Framework

* Go to taf/ and run "python3 main.py -h", It will give you help how to run test automation framework.
* To run sample test case run "python3 main.py -t ../tests/test.robot"

### Test Results

* Go to taf/results/<year-month-date>/
* That folder will contain all robot framework logs: output-<testsuitename>-<yearmonthdate>-<hrminsec>.xml,
                                                      log-<testsuitename>-<yearmonthdate>-<hrminsec>.html,
                                                      report-<testsuitename>-<yearmonthdate>-<hrminsec>.html
* That folder will also contain summary report: Summary-Report-<yearmonthdate>-<hrminsec>.xlsx
