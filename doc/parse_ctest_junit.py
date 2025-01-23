#!/usr/bin/env python3

import argparse
from typing import List
import xml.etree.ElementTree as ET

class CTestTestCase:
    name: str
    time: float
    status: str
    system_out: str

    def __init__(self, name, time, status, system_out):
        self.name = name
        self.time = time
        self.status = status
        self.system_out = system_out

def parseCTestJUnitFile(filename: str) -> List[CTestTestCase]:
    tree = ET.parse(filename)
    testsuite = tree.getroot()
    testcases = []
    for testcase_element in testsuite.findall("testcase"):
        name = testcase_element.get("name")
        time = float(testcase_element.get("time"))
        status = testcase_element.get("status")
        system_out = testcase_element.find("system-out").text
        testcase = CTestTestCase(name, time, status, system_out)
        testcases.append(testcase)
    return testcases

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", type=str, nargs='+')
    args = parser.parse_args()
    for filename in args.filenames:
        print(filename)
        for testcase in parseCTestJUnitFile(filename):
            print(f"  - name: {testcase.name}")
            print(f"    time: {testcase.time}")
            print(f"    status: {testcase.status}")
            # print(f"    system-out: |\n{testcase.system_out}")

if __name__ == "__main__":
    main()

