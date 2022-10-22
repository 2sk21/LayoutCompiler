# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

import xml.etree.ElementTree as ET
import csv
import re
import argparse
from pathlib import Path

def loadSensorFile(fileName, root, elementCounter):
    with open(fileName, 'r') as inputFile:
        sensorReader = csv.reader(inputFile)
        sensorsX = ET.Element('sensors')
        root.insert(elementCounter, sensorsX)
        for row in sensorReader:
            if row[0] == 'class':
                className = row[1]
                sensorsX.attrib['class'] = className
            elif row[0] == 'defaultInitialState':
                defaultInitialState = row[1]
                dis = ET.SubElement(sensorsX, 'defaultInitialState')
                dis.text = defaultInitialState
            else:
                sensorX = ET.SubElement(sensorsX, 'sensor')
                sensorX.attrib['inverted'] = row[2]
                systemNameX = ET.SubElement(sensorX, 'systemName')
                systemNameX.text = row[0]
                if row[1] != '':
                    userNameX = ET.SubElement(sensorX, 'userName')
                    userNameX.text = row[1]
                if row[3] != '':
                    commentX = ET.SubElement(sensorX, 'comment')
                    commentX.text = row[3]

def main(args):
    # Load the reduced XML file
    inputDir = args.inputDir
    if not inputDir.endswith('/'):
        inputDir = inputDir + '/'
    tree = ET.parse(inputDir + 'reduced.xml')
    root = tree.getroot()
    elementCounter = 1 # The index of the the insertion point for the next element
    
    # Get a list of the CSV files for sensors, turnouts and lights
    p = Path(inputDir)
    csvf = list(p.glob('*.csv'))
    sensorFileNames = [ str(x) for x in csvf if str(x).find('S') > 0 ]
    turnoutFileNames = [ str(x) for x in csvf if str(x).find('T') > 0 ]
    lightsFileNames = [ str(x) for x in csvf if str(x).find('L') > 0 ]

    for sensorFileName in sensorFileNames:
        loadSensorFile(sensorFileName, root, elementCounter)
        elementCounter += 1

    tree.write('layout.xml')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deconstruct a JMRI XML formatted layout description file')
    parser.add_argument('--inputDir', type=str, default='.', help='Directory containing the CSV and XML files.')
    args = parser.parse_args()
    main(args)
