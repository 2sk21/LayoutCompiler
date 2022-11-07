# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

import xml.etree.ElementTree as ET
import csv
import re
import argparse

# This pattern occurs repeatedly
def getOptionalElement(parent, tagname):
    x = parent.find(tagname)
    if x != None:
        return x.text
    else:
        return ''


def getFileName(sensorsX, setCounter, objectName):
    className = sensorsX.attrib['class']
    comps = className.split('.')
    sensorType = comps[2]
    sensorSubType = ''
    if sensorType == 'cmri':
        sensorSubType = comps[3]
    firstSensor = sensorsX.find(objectName)
    sn = firstSensor.find('systemName').text
    x = re.compile(r'(\S*?)\d+$')
    y = x.match(sn)
    busName = y.groups()[0]
    if sensorSubType:
        return sensorType + '_' + sensorSubType + '_' + busName + '_' + str(setCounter) + ".csv"
    else:
        return sensorType + '_' + busName + '_' + str(setCounter) + ".csv"

def extractSensors(sensorsX, sensorSetCounter, outputDir):
    sensorFileName = getFileName(sensorsX, sensorSetCounter, 'sensor')
    if sensorFileName:
        with open(outputDir + sensorFileName, 'w') as outFile:
            tablewriter = csv.writer(outFile)
            headings = ['Columns',  'System name', 'User name', 'Inverted', 'Comment', 'Use global debounce timer' ]
            tablewriter.writerow(headings)
            row = [ 'class', sensorsX.attrib['class']]
            tablewriter.writerow(row)
            gdt = sensorsX.find('globalDebounceTimers')
            for sensorX in sensorsX:
                if sensorX.tag == 'defaultInitialState':
                    row = [ 'defaultInitialState', sensorX.text ]
                    tablewriter.writerow(row)
                elif sensorX.tag == 'globalDebounceTimers':
                    row = [ 'globalDebounceTimers', sensorX.find('goingActive').text, sensorX.find('goingInActive').text]
                    tablewriter.writerow(row)
                elif sensorX.tag == "sensor":
                    inverted = False
                    if "inverted" in sensorX.attrib:
                        inverted = sensorX.attrib['inverted'] == "true"
                    systemName = ''
                    userName = ''
                    comment = ''
                    useGlobalDebounceTimer = ''
                    for t in sensorX:
                        if t.tag == 'systemName':
                            systemName = t.text
                        elif t.tag == 'userName':
                            userName = t.text
                        elif t.tag == 'comment':
                            comment = t.text
                        elif t.tag == 'useGlobalDebounceTimer':
                            useGlobalDebounceTimer = t.text
                    tablewriter.writerow(['sensor', str(systemName), str(userName), str(inverted), comment, useGlobalDebounceTimer])
    else:
        print('Could not determine file name for sensors ' + sensorSetCounter)

def extractTurnouts(turnoutsX, turnoutSetCounter, outputDir):
    turnoutFileName = getFileName(turnoutsX, turnoutSetCounter, 'turnout')
    if turnoutFileName:
        with open(outputDir + turnoutFileName, 'w') as outFile:
            tablewriter = csv.writer(outFile)
            headings = ['Columns',  'System name', 'User name', 'Comment', 'Feedback', 'Sensor 1', 'Sensor 2', 'Inverted', 'Control type', 'Automate']
            tablewriter.writerow(headings)
            row = [ 'class', turnoutsX.attrib['class']]
            tablewriter.writerow(row)
            ops = turnoutsX.find('operations')
            if ops != None:
                if ops.attrib['automate'] != None:
                    row = [ 'operations_automate', ops.attrib['automate']]
                    tablewriter.writerow(row) 
                for op in ops:
                    row = [ 'operations', op.attrib['name'], op.attrib['class'], op.attrib['interval'], op.attrib['maxtries']]
                    tablewriter.writerow(row)
            dcs = turnoutsX.find('defaultclosedspeed')
            if dcs != None:
                row = [ 'defaultclosedspeed', dcs.text]
                tablewriter.writerow(row)
            dts = turnoutsX.find('defaultthrownspeed')
            if dts != None:
                row = [ 'defaultthrownspeed', dts.text]
                tablewriter.writerow(row)
            for turnoutX in turnoutsX:
                if turnoutX.tag == "turnout":
                    systemName = turnoutX.find('systemName').text

                    # User name is optional
                    userName = ''
                    userNameX = turnoutX.find('userName')
                    if userNameX != None:
                        userName = userNameX.text

                    # Comment is optional
                    comment = ''
                    commentX = turnoutX.find('comment')
                    if commentX != None:
                        comment = commentX.text

                    # sensor1 is optional
                    sensor1 = ''
                    if 'sensor1' in turnoutX.attrib:
                        sensor1 = turnoutX.attrib['sensor1']
                    
                    # sensor2 is optional
                    sensor2 = ''
                    if 'sensor2' in turnoutX.attrib:
                        sensor2 = turnoutX.attrib['sensor2']

                    # controlType is optional
                    controlType = ''
                    if 'controlType' in turnoutX.attrib:
                        controlType = turnoutX.attrib['controlType']

                    #propertiesL = []
                    #propertiesX = turnoutX.find('properties')
                    #if propertiesX != None:
                    #    for propertyX in propertiesX:
                    #        key = propertyX.find('key').text
                    #        value = propertyX.find('value').text
                    #        propertiesL.append((key,value))
                    #properties = str(propertiesL)

                    row = [ 'turnout',                  # 0
                        systemName,                     # 1
                        userName,                       # 2
                        comment,                        # 3
                        turnoutX.attrib['feedback'],    # 4
                        sensor1,                        # 5
                        sensor2,                        # 6
                        turnoutX.attrib['inverted'],    # 7
                        controlType,                    # 8
                        turnoutX.attrib['automate']     # 9
                        ]
                    tablewriter.writerow(row)

def extractLights(lightsX, lightSetCounter, outputDir):
    lightFileName = getFileName(lightsX, lightSetCounter, 'light')
    if lightFileName:
        with open(outputDir + lightFileName, 'w') as outFile:
            tablewriter = csv.writer(outFile)
            headings = ['Columns', 'System name', 'User name', 'Comment', 'Min intensity', 'Max intensity', 'Transition time', 'Control type', 'Control sensor', 'Sensor sense']
            tablewriter.writerow(headings)
            row = [ 'class', lightsX.attrib['class']]
            tablewriter.writerow(row)
            for lightX in lightsX:
                systemName = lightX.find('systemName').text
                userName = getOptionalElement(lightX, 'userName')
                comment = getOptionalElement(lightX, 'comment')
                controlType = ''
                controlSensor = ''
                sensorSense = ''
                lightcontrolX = lightX.find('lightcontrol')
                if lightcontrolX != None:
                    controlType = lightcontrolX.attrib['controlType']
                    controlSensor = lightcontrolX.attrib['controlSensor']
                    sensorSense = lightcontrolX.attrib['sensorSense']
                minIntensity = lightX.attrib['minIntensity']
                maxIntensity = lightX.attrib['maxIntensity']
                transitionTime = lightX.attrib['transitionTime']
                row = ['light', systemName, userName, comment, minIntensity, maxIntensity, transitionTime, controlType, controlSensor, sensorSense]
                tablewriter.writerow(row)

def extractSignalHeads(signalHeadsX, outputDir):
    with open(outputDir + 'signalheads_tripleturnout.csv', 'w') as outFile:
        tablewriter = csv.writer(outFile)
        row = [ 'Columns', 'System name', 'User name', 'Comment', 'Green', 'Yellow', 'Red' ]
        tablewriter.writerow(row)
        row = [ 'class', signalHeadsX.attrib['class']]
        tablewriter.writerow(row)
        for signalHeadX in signalHeadsX:
            cl = signalHeadX.attrib['class']
            if cl == 'jmri.implementation.configurexml.TripleTurnoutSignalHeadXml':
                systemName = signalHeadX.find('systemName').text
                userName = getOptionalElement(signalHeadX, 'userName')
                comment = getOptionalElement(signalHeadX, 'comment')
                green = ''
                yellow = ''
                red = ''
                for child in signalHeadX:
                    if child.tag == 'turnoutname':
                        if child.attrib['defines'] == 'red':
                            red = child.text
                        elif child.attrib['defines'] == 'yellow':
                            yellow = child.text
                        elif child.attrib['defines'] == 'green':
                            green = child.text
                row = [ 'signalhead', systemName, userName, comment, green, yellow, red ]
                tablewriter.writerow(row)
    with open(outputDir + 'signalheads_singleturnout.csv', 'w') as outFile:
        tablewriter = csv.writer(outFile)
        row = [ 'Columns', 'System name', 'User name', 'Comment', 'Thrown', 'Closed', 'Aspect' ]
        tablewriter.writerow(row)
        row = [ 'class', signalHeadsX.attrib['class']]
        tablewriter.writerow(row)
        for signalHeadX in signalHeadsX:
            cl = signalHeadX.attrib['class']
            if cl == 'jmri.implementation.configurexml.SingleTurnoutSignalHeadXml':
                systemName = signalHeadX.find('systemName').text
                userName = getOptionalElement(signalHeadX, 'userName')
                comment = getOptionalElement(signalHeadX, 'comment')
                thrown = ''
                closed = ''
                aspect = ''
                for child in signalHeadX:
                    if child.tag == 'appearance':
                        if child.attrib['defines'] == 'thrown':
                            thrown = child.text
                        elif child.attrib['defines'] == 'closed':
                            closed = child.text
                    elif child.tag == 'turnoutname':
                        if child.attrib['defines'] == 'aspect':
                            aspect = child.text
                row = [ 'signalhead', systemName, userName, comment, thrown, closed, aspect ]
                tablewriter.writerow(row)
            

def extractSignalMasts(signalMastsX, outputDir):
    with open(outputDir + 'signalmasts.csv', 'w') as outFile:
        tablewriter = csv.writer(outFile)
        row = [ 'Columns', 'System name', 'User name', 'Unlit', 'Disabled aspects' ]
        tablewriter.writerow(row)
        row = [ 'class', signalMastsX.attrib['class']]
        tablewriter.writerow(row)
        for signalMastX in signalMastsX:
            systemName = ''
            userName = ''
            unlit='no'
            disabledAspects = []
            for child in signalMastX:
                if child.tag == 'systemName':
                    systemName = child.text
                elif child.tag == 'userName':
                    userName = child.text
                elif child.tag == 'unlit':
                    unlit = child.attrib['allowed']
                elif child.tag == 'disabledAspects':
                    for c in child:
                        disabledAspects.append(c.text)
            da = '(' + ','.join(disabledAspects) + ')'
            row = [ 'signalmast', systemName, userName, unlit, disabledAspects]
            tablewriter.writerow(row)

def extractBlocks(blocksX, outputDir):
    with open(outputDir + 'blocks.csv', 'w') as outFile:
        tablewriter = csv.writer(outFile)
        row = [ 'Columns', 'System name', 'User name', 'length', 'curve', 'comment', 'permissive', 'Occupancy sensor']
        tablewriter.writerow(row)
        row = [ 'class', blocksX.attrib['class']]
        tablewriter.writerow(row)
        for child in blocksX:
            if child.tag == 'defaultspeed':
                row = [ 'defaultspeed', child.text ]
            elif child.tag == 'block':
                blockX = child
                # Block elements are present in duplicate to break circularity in the code
                # Only the instance with the permissive child element needs to be considered
                permissiveX = blockX.find('permissive')
                if permissiveX != None:
                    length = blockX.attrib['length']
                    curve = blockX.attrib['curve']
                    systemName = blockX.find('systemName').text
                    userName = ''
                    userNameX = blockX.find('userName')
                    if userNameX != None:
                        userName = userNameX.text
                    comment = ''
                    commentX = blockX.find('comment')
                    if commentX != None:
                        comment = commentX.text
                    permissive = permissiveX.text
                    occupancySensor = getOptionalElement(blockX, 'occupancysensor')
                    row = ['block', systemName, userName, length, curve, comment, permissive, occupancySensor]
                    tablewriter.writerow(row)

def extractXMLblob(root, filename, outputDir):
    with open(outputDir + filename, 'w') as outFile:
        t = ET.tostring(root, encoding='unicode')
        outFile.write(t)

def removeElements(root, tagName):
    elements = root.findall(tagName)
    for e in elements:
        root.remove(e)

def main(args):
    ifn = args.inputFile
    tree = ET.parse(ifn)
    root = tree.getroot()
    sensorSetCounter = 0
    turnoutSetCounter = 0
    lightSetCounter = 0
    outputDir = args.csvDir
    if not outputDir.endswith('/'):
        outputDir = outputDir + '/'
    for child in root:
        if child.tag == "sensors":
            sensorSetCounter += 1
            extractSensors(child, sensorSetCounter, outputDir)
        elif child.tag == 'turnouts':
            turnoutSetCounter += 1
            extractTurnouts(child, turnoutSetCounter, outputDir)
        elif child.tag == 'lights':
            lightSetCounter += 1
            extractLights(child, lightSetCounter, outputDir)
        elif child.tag == 'signalheads':
            extractSignalHeads(child, outputDir)
        elif child.tag == 'signalmasts':
            extractSignalMasts(child, outputDir)
        elif child.tag == 'blocks':
            extractBlocks(child, outputDir)
    # Finally, we create a reduced version of the layout config XML file with
    # the externally managed objects removed.
    # Commented this out as the reduced XML is no longer necessary (11/5/2022)
    #removeElements(root, 'sensors')
    #removeElements(root, 'turnouts')
    #removeElements(root, 'lights')
    #removeElements(root, 'signalheads')
    #removeElements(root, 'signalmasts')
    #removeElements(root, 'blocks')
    #tree.write(outputDir + 'reduced.xml')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deconstruct a JMRI XML formatted layout description file')
    parser.add_argument('inputFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('--csvDir', type=str, default='.', help='Directory in which to write the generated CSV files')
    args = parser.parse_args()
    main(args)
