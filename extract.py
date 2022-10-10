import xml.etree.ElementTree as ET
import csv
import re
import argparse

def getSensorFileName(sensorsX, setCounter):
    className = sensorsX.attrib['class']
    comps = className.split('.')
    sensorType = comps[2]
    sensorSubType = ''
    if sensorType == 'cmri':
        sensorSubType = comps[3]
    firstSensor = sensorsX.find('sensor')
    sn = firstSensor.find('systemName').text
    x = re.compile(r'(\S*?)\d+$')
    y = x.match(sn)
    busName = y.groups()[0]
    if sensorSubType:
        return sensorType + '_' + sensorSubType + '_' + busName + '_' + str(setCounter) + ".csv"
    else:
        return sensorType + '_' + busName + '_' + str(setCounter) + ".csv"

def extractSensors(sensorsX, sensorSetCounter, outputDir):
    sensorFileName = getSensorFileName(sensorsX, sensorSetCounter)
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

def extractTurnouts(turnoutsX, turnoutSetCounter, outputDir):
    pass

def main(args):
    ifn = args.inputFile
    tree = ET.parse(ifn)
    root = tree.getroot()
    sensorSetCounter = 0
    turnoutSetCounter = 0
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deconstruct a JMRI XML formatted layout description file')
    parser.add_argument('inputFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('--outputDir', type=str, default='.', help='Directory in which to write the generated CSV files')
    args = parser.parse_args()
    main(args)
