# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

# Compare the original layout.xml with result of round trip through extract and compile

import xml.etree.ElementTree as ET
import csv
import re
import argparse

def getSensorBySystemName(root, systemName):
    queryString = ".sensors/sensor/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    if len(sensors) != 1:
        return None
    else:
        return sensors[0]

def getAllSensors(root):
    queryString = ".sensors/sensor"
    return root.findall(queryString)

def sensorsMismatch(original, updated):
    if original.attrib['inverted'] != updated.attrib['inverted']:
        return True
    originalUserNameX = original.find('userName')
    updatedUserNameX = updated.find('userName')
    if (originalUserNameX != None) and (updatedUserNameX != None) and (originalUserNameX.text != updatedUserNameX.text):
        return True
    originalCommentX = original.find('comment')
    updatedCommentX = updated.find('comment')
    if (originalCommentX != None) and (updatedCommentX != None) and (originalCommentX.text != updatedCommentX.text):
        return True
    return False

def main(args):
    print('Original file: ', args.originalFile, 'Updated file:', args.updatedFile)
    originalTree = ET.parse(args.originalFile)
    originalRoot = originalTree.getroot()
    updatedTree = ET.parse(args.updatedFile)
    updatedRoot = updatedTree.getroot()

    originalSensors = getAllSensors(originalRoot)
    updatedSensors = getAllSensors(updatedRoot)
    if len(originalSensors) != len(updatedSensors):
        return 'Error: number of sensors do not match'
    print('Num sensors matches', len(originalSensors))
    for originalSensor in originalSensors:
        originalSystemName = originalSensor.find('systemName').text
        updatedSensor = getSensorBySystemName(updatedRoot, originalSystemName)
        if updatedSensor == None:
            print('Error missing sensor in update: ', originalSystemName)
            return
        elif sensorsMismatch(originalSensor, updatedSensor):
            print('Sensor mismatch', originalSystemName)
            return

    print('Test passed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the original layout.xml with result of round trip through extract and compile')
    parser.add_argument('originalFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('updatedFile', type=str, help='XML file result of running round trip extract followed by compile')
    args = parser.parse_args()

    main(args)