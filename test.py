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

def optionalTagMatchesByPattern(original, updated, pattern):
    t = original.findall(pattern)
    u = updated.findall(pattern)
    if len(t) != len(u):
        return False
    if len(t) == 1 and len(u) == 1:
        originalChild = t[0]
        updatedChild = u[0]
        return originalChild.text == updatedChild.text
    return len(t) == 0 and len(u) == 0


def getSensorBySystemName(root, systemName):
    queryString = ".sensors/sensor/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    if len(sensors) != 1:
        return None
    else:
        return sensors[0]

def getTurnoutBySystemName(root, systemName):
    queryString = ".turnouts/turnout/systemName[.='%s']/.." % systemName
    turnouts = root.findall(queryString)
    if len(turnouts) != 1:
        return None
    else:
        return turnouts[0]

def getLightBySystemName(root, systemName):
    queryString = ".lights/light/systemName[.='%s']/.." % systemName
    lights = root.findall(queryString)
    if len(lights) != 1:
        return None
    else:
        return lights[0]

def getSignalheadBySystemName(root, systemName):
    queryString = ".signalheads/signalhead/systemName[.='%s']/.." % systemName
    signalheads = root.findall(queryString)
    if len(signalheads) != 1:
        return None
    else:
        return signalheads[0]

def getAllSensors(root):
    queryString = '.sensors/sensor'
    return root.findall(queryString)

def getAllTurnouts(root):
    queryString = '.turnouts/turnout'
    return root.findall(queryString)

def getAllLights(root):
    queryString = '.lights/light'
    return root.findall(queryString)

def getAllSignalheads(root):
    queryString = '.signalheads/signalhead'
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

def lightMatches(originalLight, updatedLight):
    if not attributeMatches(originalLight, updatedLight, 'minIntensity'):
        return False
    if not attributeMatches(originalLight, updatedLight, 'maxIntensity'):
        return False
    if not attributeMatches(originalLight, updatedLight, 'transitionTime'):
        return False
    if not optionalTagMatches(originalLight, updatedLight, 'userName'):
        return False
    if not optionalTagMatches(originalLight, updatedLight, 'comment'):
        return False
    originalLightcontrol = originalLight.find('lightcontrol')
    updatedLightcontrol = updatedLight.find('lightcontrol')
    if originalLightcontrol is None:
        if updatedLightcontrol is None:
            pass
        else:
            return False
    else:
        if updatedLightcontrol is None:
            return False
        else:
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'controlType'):
                return False
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'controlSensor'):
                return False
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'sensorSense'):
                return False
    return True

def lightsMatch(originalRoot, updatedRoot):
    originalLights = getAllLights(originalRoot)
    updatedLights = getAllLights(updatedRoot)
    numOriginalLights = len(originalLights)
    numUpdatedLights = len(updatedLights)
    if numOriginalLights != numUpdatedLights:
        print('Number of lights do not match', numOriginalLights, numUpdatedLights)
        originalSet = set(originalLights)
        updatedSet = set(updatedLights)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num lights matches', len(originalLights))
    for originalLight in originalLights:
        originalSystemName = originalLight.find('systemName').text
        print('Checking light', originalSystemName)
        updatedLight = getLightBySystemName(originalRoot, originalSystemName)
        if updatedLight == None:
            print('Missing updated light')
            return False
        elif not lightMatches(originalLight, updatedLight):
            print('Light mismatch', originalSystemName)
            return False
    return True

def signalheadMatches(originalSignalhead, updatedSignalhead):
    if not attributeMatches(originalSignalhead, updatedSignalhead, 'class'):
        return False
    if not optionalTagMatches(originalSignalhead, updatedSignalhead, 'userName'):
        return False
    if not optionalTagMatches(originalSignalhead, updatedSignalhead, 'comment'):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='green']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='yellow']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='red']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./appearance[@defines='thrown']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./appearance[@defines='closed']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='aspect']"):
        return False
    return True

def signalHeadsMatch(originalRoot, updatedRoot):
    originalSignalheads = getAllSignalheads(originalRoot)
    updatedSignalheads = getAllSignalheads(updatedRoot)
    numOriginalSignalheads = len(originalSignalheads)
    numUpdatedSignalheads = len(updatedSignalheads)
    if numOriginalSignalheads != numUpdatedSignalheads:
        print('Number of signalheads do not match', numOriginalSignalheads, numUpdatedSignalheads)
        originalSet = set(originalSignalheads)
        updatedSet = set(updatedSignalheads)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num signalheads match', numOriginalSignalheads)
    for originalSignalhead in originalSignalheads:
        originalSystemName = originalSignalhead.find('systemName').text
        print('Checking signalhead', originalSystemName)
        updatedSignalhead = getSignalheadBySystemName(originalRoot, originalSystemName)
        if updatedSignalhead is None:
            print('Missing updated signalhead')
            return False
        elif not signalheadMatches(originalSignalhead, updatedSignalhead):
            print('Signalhead mismatch', originalSystemName)
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
    if not lightsMatch(originalRoot, updatedRoot):
        return
    if not signalHeadsMatch(originalRoot, updatedRoot):
        return
    print('Test passed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the original layout.xml with result of round trip through extract and compile')
    parser.add_argument('originalFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('updatedFile', type=str, help='XML file result of running round trip extract followed by compile')
    args = parser.parse_args()

    main(args)