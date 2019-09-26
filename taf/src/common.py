####################################################################
# This is common python module script of Test Automation Framework.
####################################################################

import xmltodict
import json


class common():

    def __init__(self):
        pass

    def xmlToDictConverter(self, xmlFilePath):
        """
        convert given xml to dictionary
        Args:
        xmlFilePath: absolute path of xml file
        return: Dictionary
        """
        try:
            with open(xmlFilePath) as fp:
                con = xmltodict.parse(fp.read())
            dic = json.dumps(con)
            dic = json.loads(dic)
            return dic
        except Exception as error:
            return (False, error)
