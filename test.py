# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

# Compare the original layout.xml with result of round trip through extract and compile

import xml.etree.ElementTree as ET
import argparse

def attributeMatches(original, updated, attributeName):
    if attributeName in original.attrib:
        if attributeName in updated.attrib:
            return original.attrib[attributeName] == updated.attrib[attributeName]
        else:
            return False
    else:
        if attributeName in updated.attrib:
            return False
        else:
            return True

def optionalTagMatches(original, updated, tagName):
    originalChild = original.find(tagName)
    updatedChild = updated.find(tagName)
    if originalChild == None:
        if updatedChild == None:
            return True
        else:
            return False
    else:
        if updatedChild == None:
            return False
        else:
            return originalChild.text == updatedChild.text

def getSensorBySystemName(root, systemName):
    queryString = ".sensors/sensor/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    if len(sensors) != 1:
        return None
    else:
        return sensors[0]

def getTurnoutBySystemName(root, systemName):
    queryString = ".turnouts/turnout/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    if len(sensors) != 1:
        return None
    else:
        return sensors[0]

def getAllSensors(root):
    queryString = ".sensors/sensor"
    return root.findall(queryString)

def getAllTurnouts(root):
    queryString = ".turnouts/turnout"
    return root.findall(queryString)

def sensorMatches(original, updated):
    if not attributeMatches(original, updated, 'inverted'):
        return False
    if not optionalTagMatches(original, updated, 'userName'):
        return False
    return optionalTagMatches(original, updated, 'comment')


def sensorsMatch(originalRoot, updatedRoot):
    originalSensors = getAllSensors(originalRoot)
    updatedSensors = getAllSensors(updatedRoot)
    if len(originalSensors) != len(updatedSensors):
        print('Error: number of sensors do not match')
        return False
    print('Num sensors matches', len(originalSensors))
    for originalSensor in originalSensors:
        originalSystemName = originalSensor.find('systemName').text
        print('Checking sensor ', originalSystemName)
        updatedSensor = getSensorBySystemName(updatedRoot, originalSystemName)
        if updatedSensor == None:
            print('Error missing sensor in update: ', originalSystemName)
            return False
        elif not sensorMatches(originalSensor, updatedSensor):
            print('Sensor mismatch', originalSystemName)
            return False
    return True

def turnoutMatches(original, updated):
    if not attributeMatches(original, updated, 'feedback'):
        return False
    if not attributeMatches(original, updated, 'inverted'):
        return False
    if not attributeMatches(original, updated, 'automate'):
        return False
    if not attributeMatches(original, updated, 'controlType'):
        return False
    if not attributeMatches(original, updated, 'sensor1'):
        return False
    if not attributeMatches(original, updated, 'sensor2'):
        return False
    if not optionalTagMatches(original, updated, 'userName'):
        return False
    if not optionalTagMatches(original, updated, 'comment'):
        return False
    return True
    

def turnoutsMatch(originalRoot, updatedRoot):
    originalTurnouts = getAllTurnouts(originalRoot)
    updatedTurnouts = getAllTurnouts(updatedRoot)
    if len(originalTurnouts) != len(updatedTurnouts):
        print('Number of turnouts do not match')
        return False
    print('Num turnouts matches', len(originalTurnouts))
    for originalTurnout in originalTurnouts:
        originalSystemName = originalTurnout.find('systemName').text
        print('Checking turnout', originalSystemName)
        updatedTurnout = getTurnoutBySystemName(originalRoot, originalSystemName)
        if updatedTurnout == None:
            print('Missing updated turnout')
            return False
        elif not turnoutMatches(originalTurnout, updatedTurnout):
            print('Turnout mismatch', originalSystemName)
            return False
        
    return True

def main(args):
    print('Original file: ', args.originalFile, 'Updated file:', args.updatedFile)
    originalTree = ET.parse(args.originalFile)
    originalRoot = originalTree.getroot()
    updatedTree = ET.parse(args.updatedFile)
    updatedRoot = updatedTree.getroot()
    if not sensorsMatch(originalRoot, updatedRoot):
        return
    if not turnoutsMatch(originalRoot, updatedRoot):
        return
    print('Test passed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the original layout.xml with result of round trip through extract and compile')
    parser.add_argument('originalFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('updatedFile', type=str, help='XML file result of running round trip extract followed by compile')
    args = parser.parse_args()

    main(args)