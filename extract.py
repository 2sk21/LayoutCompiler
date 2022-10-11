# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

import xml.etree.ElementTree as ET
import csv
import re
import argparse

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
            row = [ 'class', sensorsX.attrib['class']]
            tablewriter.writerow(row)
            dis = sensorsX.find('defaultInitialState')
            if dis != None:
                row = [ 'defaultInitialState', sensorsX.find('defaultInitialState').text]
                tablewriter.writerow(row)
            for sensorX in sensorsX:
                if sensorX.tag == "sensor":
                    inverted = False
                    if "inverted" in sensorX.attrib:
                        inverted = sensorX.attrib['inverted'] == "true"
                    systemName = ""
                    userName = ""
                    for t in sensorX:
                        if t.tag == "systemName":
                            systemName = t.text
                        elif t.tag == "userName":
                            userName = t.text
                    tablewriter.writerow([str(systemName), str(userName), str(inverted)])
    else:
        print('Could not determine file name for sensors ' + sensorSetCounter)

def extractTurnouts(turnoutsX, turnoutSetCounter, outputDir):
    turnoutFileName = getFileName(turnoutsX, turnoutSetCounter, 'turnout')
    if turnoutFileName:
        with open(outputDir + turnoutFileName, 'w') as outFile:
            tablewriter = csv.writer(outFile)
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
                    sn = turnoutX.find('systemName').text
                    commentX = turnoutX.find('comment')
                    comment = ''
                    if commentX != None:
                        comment = commentX.text
                    feedback = turnoutX.attrib['feedback']
                    sensor1 = ''
                    if 'sensor1' in turnoutX.attrib:
                        sensor1 = turnoutX.attrib['sensor1']
                    sensor2 = ''
                    if 'sensor2' in turnoutX.attrib:
                        sensor2 = turnoutX.attrib['sensor2']
                    row = [ 'turnout', sn, comment, feedback, sensor1, sensor2, turnoutX.attrib['inverted'], turnoutX.attrib['automate']]
                    tablewriter.writerow(row)

def extractLights(lightsX, lightSetCounter, outputDir):
    lightFileName = getFileName(lightsX, lightSetCounter, 'light')
    if lightFileName:
        with open(outputDir + lightFileName, 'w') as outFile:
            tablewriter = csv.writer(outFile)
            row = [ 'class', lightsX.attrib['class']]
            tablewriter.writerow(row)
            for lightX in lightsX:
                systemName = lightX.find('systemName').text
                minIntensity = lightX.attrib['minIntensity']
                maxIntensity = lightX.attrib['maxIntensity']
                transitionTime = lightX.attrib['transitionTime']
                row = [systemName, minIntensity, maxIntensity, transitionTime]
                tablewriter.writerow(row)

def extractSignalHeads(signalHeadsX, outputDir):
    with open(outputDir + 'signalheads.csv', 'w') as outFile:
        tablewriter = csv.writer(outFile)
        row = [ 'class', signalHeadsX.attrib['class']]
        tablewriter.writerow(row)
        for signalHeadX in signalHeadsX:
            cl = signalHeadX.attrib['class']
            row = [ 'class', cl]
            for child in signalHeadX:
                if child.tag == 'systemName':
                    row.append(child.text)
                elif child.tag == 'appearance':
                    row.append(('appearance', child.attrib['defines'], child.text))
                elif child.tag == 'turnoutname':
                    row.append(('turnoutname', child.attrib['defines'], child.text))
            tablewriter.writerow(row)
            

def main(args):
    ifn = args.inputFile
    tree = ET.parse(ifn)
    root = tree.getroot()
    sensorSetCounter = 0
    turnoutSetCounter = 0
    lightSetCounter = 0
    outputDir = args.outputDir
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deconstruct a JMRI XML formatted layout description file')
    parser.add_argument('inputFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('--outputDir', type=str, default='.', help='Directory in which to write the generated CSV files')
    args = parser.parse_args()
    main(args)
