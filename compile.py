# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

import xml.etree.ElementTree as ET
import csv
import re
import argparse
from pathlib import Path

# This program loads externally managed objects in this order:
# Sensors
# turnouts
# lights
# reporters
# signalheads
# signalmasts
# blocks

# There will generally be many files with sensor data
def loadSensorFile(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        sensorReader = csv.reader(inputFile)
        sensorsX = ET.Element('sensors')
        root.insert(elementCounter, sensorsX)
        for row in sensorReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                className = row[1]
                sensorsX.attrib['class'] = className
            elif row[0] == 'defaultInitialState':
                defaultInitialState = row[1]
                dis = ET.SubElement(sensorsX, 'defaultInitialState')
                dis.text = defaultInitialState
            elif row[0] == 'globalDebounceTimers':
                globalDebounceTimersX = ET.SubElement(sensorsX, 'globalDebounceTimers')
                goingActiveX = ET.SubElement(globalDebounceTimersX, 'goingActive')
                goingActiveX.text = row[1]
                goingInActiveX = ET.SubElement(globalDebounceTimersX, 'goingInActive')
                goingInActiveX.text = row[2]
            elif row[0] == 'sensor':
                sensorX = ET.SubElement(sensorsX, 'sensor')
                systemNameX = ET.SubElement(sensorX, 'systemName')
                systemNameX.text = row[1]
                if row[2].strip() != '':
                    userNameX = ET.SubElement(sensorX, 'userName')
                    userNameX.text = row[2]
                sensorX.attrib['inverted'] = row[3]
                if row[4].strip() != '':
                    commentX = ET.SubElement(sensorX, 'comment')
                    commentX.text = row[4]
                if row[5].strip() != '':
                    useGlobalDebounceTimerX = ET.SubElement(sensorX, 'useGlobalDebounceTimer')
                    useGlobalDebounceTimerX.text = row[5]

def loadTurnoutFile(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        turnoutReader = csv.reader(inputFile)
        turnoutsX = ET.Element('turnouts')
        root.insert(elementCounter, turnoutsX)
        operationsX = ET.SubElement(turnoutsX, 'operations')
        for row in turnoutReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                className = row[1]
                turnoutsX.attrib['class'] = className
            elif row[0] == 'operations_automate':
                operationsX.attrib['automate'] = row[1]
            elif row[0] == 'operations':
                operationX = ET.SubElement(operationsX, 'operation')
                name = row[1]
                className = row[2]
                interval = row[3]
                maxtries = row[4]
                operationX.attrib['name'] = name
                operationX.attrib['class'] = className
                operationX.attrib['interval'] = interval
                operationX.attrib['maxtries'] = maxtries
            elif row[0] == 'defaultclosedspeed':
                defaultClosedSpeedX = ET.SubElement(turnoutsX, 'defaultclosedspeed')
                defaultClosedSpeedX.text = row[1]
            elif row[0] == 'defaultthrownspeed':
                defaultThrownSpeedX = ET.SubElement(turnoutsX, 'defaultthrownspeed')
                defaultThrownSpeedX.text = row[1]
            elif row[0] == 'turnout':
                turnoutX = ET.SubElement(turnoutsX, 'turnout')
                
                systemName = row[1]
                systemNameX = ET.SubElement(turnoutX, 'systemName')
                systemNameX.text = systemName

                userName = row[2]
                if userName.strip() != '':
                    userNameX = ET.SubElement(turnoutX, 'userName')
                    userNameX.text = userName

                comment = row[3]
                if comment.strip() != '':
                    commentX = ET.SubElement(turnoutX, 'comment')
                    commentX.text = comment

                feedback = row[4]
                turnoutX.attrib['feedback'] = feedback

                sensor1 = row[5]
                if sensor1 != '':
                    turnoutX.attrib['sensor1'] = sensor1

                sensor2 = row[6]
                if sensor2.strip() != '':
                    turnoutX.attrib['sensor2'] = sensor2

                inverted = row[7]
                turnoutX.attrib['inverted'] = inverted

                controlType = row[8]
                if controlType.strip() != '':
                    turnoutX.attrib['controlType'] = controlType

                automate = row[9]
                turnoutX.attrib['automate'] = automate

                # Special addition for Loconet turnouts: disable sending OFF message
                if systemName.startswith('L'):
                    propertiesX = ET.SubElement(turnoutX, 'properties')
                    propertyX = ET.SubElement(propertiesX, 'property')
                    ET.SubElement(propertyX, 'key').text = 'Send ON/OFF'
                    valueX = ET.SubElement(propertyX, 'value')
                    valueX.attrib['class'] = 'java.lang.Boolean'
                    valueX.text = 'false'

                divergingSpeed = row[10]
                if divergingSpeed.strip() != '':
                    ET.SubElement(turnoutX, 'divergingSpeed').text = divergingSpeed

                straightSpeed = row[11]
                if straightSpeed.strip() != '':
                    ET.SubElement(turnoutX, 'straightSpeed').text = straightSpeed

                #propertiesS = row[10]
                #propertiesL = eval(propertiesS)
                #if len(propertiesL) > 0:
                #    propertiesX = ET.SubElement(turnoutX, 'properties')
                #    for kvp in propertiesL:
                #        propertyX = ET.SubElement(propertiesX, 'property')
                #        keyX = ET.SubElement(propertyX, 'key')
                #        keyX.text = kvp[0]
                #        valueX = ET.SubElement(propertyX, 'value')
                #        valueX.text = kvp[1]

def loadLightFile(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        lightReader = csv.reader(inputFile)
        lightsX = ET.Element('lights')
        root.insert(elementCounter, lightsX)
        for row in lightReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                lightsX.attrib['class'] = row[1]
            elif row[0] == 'light':
                systemName = row[1]
                userName = row[2]
                comment = row[3]
                minIntensity = row[4]
                maxIntensity = row[5]
                transitionTime = row[6]
                controlType = row[7]
                controlSensor = row[8]
                sensorSense = row[9]
                lightX = ET.SubElement(lightsX, 'light')
                ET.SubElement(lightX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(lightX, 'userName').text = userName
                if comment != '':
                    ET.SubElement(lightX, 'comment').text = comment
                lightX.attrib['minIntensity'] = minIntensity
                lightX.attrib['maxIntensity'] = maxIntensity
                lightX.attrib['transitionTime'] = transitionTime
                
                if controlType != '' and controlSensor != '' and sensorSense != '':
                    lightcontrolX = ET.SubElement(lightX, 'lightcontrol')
                    lightcontrolX.attrib['controlType'] = controlType
                    lightcontrolX.attrib['controlSensor'] = controlSensor
                    lightcontrolX.attrib['sensorSense'] = sensorSense

def loadReporterFile(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        reporterReader = csv.reader(inputFile)
        reportersX = ET.Element('reporters')
        root.insert(elementCounter, reportersX)
        for row in reporterReader:
            if len(row) == 0:
                continue
            elif row[0] == 'class':
                reportersX.attrib['class'] = row[1]
            elif row[0] == 'reporter':
                systemName = row[1]
                userName = row[2]
                comment = row[3]
                reporterX = ET.SubElement(reportersX, 'reporter')
                ET.SubElement(reporterX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(reporterX, 'userName').text = userName
                if comment != '':
                    ET.SubElement(reporterX, 'comment').text = comment

def loadSignalHeads(inputDir, root, elementCounter):
    signalHeadsX = ET.Element('signalheads')
    root.insert(elementCounter, signalHeadsX)
    with open(inputDir + 'signalheads_tripleturnout.csv', 'r') as inputFile:
        signalHeadsReader = csv.reader(inputFile)
        for row in signalHeadsReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                signalHeadsX.attrib['class'] = row[1]
            elif row[0] == 'signalhead':
                systemName = row[1]
                userName = row[2]
                comment = row[3]
                green = row[4]
                yellow = row[5]
                red = row[6]
                signalHeadX = ET.SubElement(signalHeadsX, 'signalhead')
                signalHeadX.attrib['class'] = 'jmri.implementation.configurexml.TripleTurnoutSignalHeadXml'
                ET.SubElement(signalHeadX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(signalHeadX, 'userName').text = userName
                if comment != '':
                    ET.SubElement(signalHeadX, 'comment').text = comment
                if green != '':
                    turnoutnameX = ET.SubElement(signalHeadX, 'turnoutname')
                    turnoutnameX.text = green
                    turnoutnameX.attrib['defines'] = 'green'
                if yellow != '':
                    turnoutnameX = ET.SubElement(signalHeadX, 'turnoutname')
                    turnoutnameX.text = yellow
                    turnoutnameX.attrib['defines'] = 'yellow'
                if red != '':
                    turnoutnameX = ET.SubElement(signalHeadX, 'turnoutname')
                    turnoutnameX.text = red
                    turnoutnameX.attrib['defines'] = 'red'
    with open(inputDir + 'signalheads_singleturnout.csv', 'r') as inputFile:
        signalHeadsReader = csv.reader(inputFile)
        for row in signalHeadsReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                signalHeadsX.attrib['class'] = row[1]
            elif row[0] == 'signalhead':
                systemName = row[1]
                userName = row[2]
                comment = row[3]
                thrown = row[4]
                closed = row[5]
                aspect = row[6]
                signalHeadX = ET.SubElement(signalHeadsX, 'signalhead')
                signalHeadX.attrib['class'] = 'jmri.implementation.configurexml.SingleTurnoutSignalHeadXml'
                ET.SubElement(signalHeadX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(signalHeadX, 'userName').text = userName
                if comment != '':
                    ET.SubElement(signalHeadX, 'comment').text = comment
                if thrown != '':
                    appearanceX = ET.SubElement(signalHeadX, 'appearance')
                    appearanceX.text = thrown
                    appearanceX.attrib['defines'] = 'thrown'
                if closed != '':
                    appearanceX = ET.SubElement(signalHeadX, 'appearance')
                    appearanceX.text = closed
                    appearanceX.attrib['defines'] = 'closed'
                if aspect != '':
                    turnoutnameX = ET.SubElement(signalHeadX, 'turnoutname')
                    turnoutnameX.text = aspect
                    turnoutnameX.attrib['defines'] = 'aspect'


def loadSignalMasts(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        signalMastsReader = csv.reader(inputFile)
        signalMastsX = ET.Element('signalmasts')
        root.insert(elementCounter, signalMastsX)
        for row in signalMastsReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                signalMastsX.attrib['class'] = row[1]
            elif row[0] == 'signalmast' or row[0] == 'virtualsignalmast' or row[0] == 'mqttsignalmast':
                systemName = row[1]
                userName = row[2].strip()
                comment = row[3].strip()
                unlit = row[4]
                da = row[5].strip()
                if da == '':
                    disabledAspects = []
                else:
                    disabledAspects = eval(row[5])
                if row[0] == 'signalmast':
                    signalMastX = ET.SubElement(signalMastsX, 'signalmast')
                    signalMastX.attrib['class'] = 'jmri.implementation.configurexml.SignalHeadSignalMastXml'
                elif row[0] == 'virtualsignalmast':
                    signalMastX = ET.SubElement(signalMastsX, 'virtualsignalmast')
                    signalMastX.attrib['class'] = 'jmri.implementation.configurexml.VirtualSignalMastXml'
                elif row[0] == 'mqttsignalmast':
                    signalMastX = ET.SubElement(signalMastsX, 'mqttsignalmast')
                    signalMastX.attrib['class'] = 'jmri.jmrix.mqtt.configurexml.MqttSignalMastXml'
                ET.SubElement(signalMastX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(signalMastX, 'userName').text = userName
                if comment != '':
                    ET.SubElement(signalMastX, 'comment').text = comment
                ET.SubElement(signalMastX, 'unlit').attrib['allowed'] = unlit
                if len(disabledAspects) > 0:
                    disabledAspectsX = ET.SubElement(signalMastX, 'disabledAspects')
                    for d in disabledAspects:
                        ET.SubElement(disabledAspectsX, 'disabledAspect').text = d

def loadBlocks(fileName, root, elementCounter):
    blocksX = ET.Element('blocks')
    root.insert(elementCounter, blocksX)
    # Create forward reference blocks
    with open(fileName, 'r') as inputFile:
        blocksReader = csv.reader(inputFile)
        for row in blocksReader:
            if len(row) == 0:
                continue
            if row[0] == 'class':
                blocksX.attrib['class'] = row[1]
            elif row[0] == 'defaultspeed':
                ET.SubElement(blocksX, 'defaultspeed').text = row[1]
            elif row[0] == 'block':
                systemName = row[1]
                userName = row[2]
                blockX = ET.SubElement(blocksX, 'block')
                blockX.attrib['systemName'] = systemName
                ET.SubElement(blockX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(blockX, 'userName').text = systemName
    # Now create the full blocks
    with open(fileName, 'r') as inputFile:
        blocksReader = csv.reader(inputFile)
        for row in blocksReader:
            if len(row) == 0:
                continue
            if row[0] == 'block':
                systemName = row[1]
                userName = row[2]
                length = row[3]
                curve = row[4]
                comment = row[5]
                permissive = row[6]
                occupancySensor = row[7]
                speed = row[8]
                reporterSystemName = row[9]
                reporterUseCurrent = row[10]
                blockX = ET.SubElement(blocksX, 'block')
                blockX.attrib['systemName'] = systemName
                ET.SubElement(blockX, 'systemName').text = systemName
                if userName != '':
                    ET.SubElement(blockX, 'userName').text = userName
                if length != '':
                    blockX.attrib['length'] = length
                if curve != '':
                    blockX.attrib['curve'] = curve
                if comment != '':
                    ET.SubElement(blockX, 'comment').text = comment
                if speed != '':
                    ET.SubElement(blockX, 'speed').text = speed
                if permissive != '':
                    ET.SubElement(blockX, 'permissive').text = permissive
                if occupancySensor != '':
                    ET.SubElement(blockX, 'occupancysensor').text = occupancySensor
                if reporterSystemName != '':
                    reporterX = ET.SubElement(blockX, 'reporter')
                    reporterX.attrib['systemName'] = reporterSystemName
                    reporterX.attrib['useCurrent'] = reporterUseCurrent

def removeElements(root, tagName):
    elements = root.findall(tagName)
    for e in elements:
        root.remove(e)

def main(args):
    # Load the reduced XML file
    inputDir = args.csvDir
    if not inputDir.endswith('/'):
        inputDir = inputDir + '/'
    tree = ET.parse(args.layoutFile)
    root = tree.getroot()

    # Remove all of the objects that are externally managed
    removeElements(root, 'sensors')
    removeElements(root, 'turnouts')
    removeElements(root, 'lights')
    removeElements(root, 'reporters')
    removeElements(root, 'signalheads')
    removeElements(root, 'signalmasts')
    removeElements(root, 'blocks')

    elementCounter = 1 # The index of the the insertion point for the next element
    
    # Get a list of the CSV files for sensors, turnouts and lights
    p = Path(inputDir)
    csvf = list(p.glob('*.csv'))
    fileNames = [ str(x) for x in csvf ]
    sensorFileNames = [ x for x in fileNames if x.find('sensor_') > 0 ]
    turnoutFileNames = [ x for x in fileNames if x.find('turnout_') > 0 ]
    lightsFileNames = [ x for x in fileNames if x.find('light_') > 0 ]
    reportersFileNames = [ x for x in fileNames if x.find('reporter_') > 0 ]

    for sensorFileName in sensorFileNames:
        try:
            loadSensorFile(sensorFileName, root, elementCounter)
            elementCounter += 1
        except:
            print('Skipping loading sensor file ' + sensorFileName)

    for turnoutFileName in turnoutFileNames:
        try:
            loadTurnoutFile(turnoutFileName, root, elementCounter)
            elementCounter += 1
        except:
            print('Skipping loading turnout file ' + turnoutFileName)

    for lightFileName in lightsFileNames:
        try:
            loadLightFile(lightFileName, root, elementCounter)
            elementCounter += 1
        except:
            print('Skipping loading lights file ', lightFileName)

    for reporterFileName in reportersFileNames:
        try:
            loadReporterFile(reporterFileName, root, elementCounter)
            elementCounter += 1
        except:
            print('Skipping loading reporter file ' + reporterFileName)

    elementCounter += 1 # Skip past the memories tag

    try:
        loadSignalHeads(inputDir, root, elementCounter)
        elementCounter += 1
    except:
        print('Skipping loading of signal heads')

    try:
        loadSignalMasts(inputDir + 'signalmasts.csv', root, elementCounter)
        elementCounter += 1
    except:
        print('Skipping loading signal masts')

    try:
        loadBlocks(inputDir + 'blocks.csv', root, elementCounter)
    except:
        print('Skipping loading blocks')

    ET.indent(tree)
    comps = args.layoutFile.split('.')
    newFileName = comps[0] + '_updated.' + comps[1]
    tree.write(newFileName, xml_declaration=True, encoding='UTF-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deconstruct a JMRI XML formatted layout description file')
    parser.add_argument('--csvDir', type=str, default='.', help='Directory containing the CSV files.')
    parser.add_argument('layoutFile', type=str, help='JMRI layout description file in XML format')
    args = parser.parse_args()

    main(args)
