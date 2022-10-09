import xml.etree.ElementTree as ET
import csv
import re

def getSensorFileName(sensorsX, setCounter):
    className = sensorsX.attrib["class"]
    comps = className.split(".")
    sensorType = comps[2]
    sensorSubType = ""
    if sensorType == "cmri":
        sensorSubType = comps[3]
    firstSensor = sensorsX.find("sensor")
    sn = firstSensor.find("systemName").text
    x = re.compile(r'(\S*?)\d+$')
    y = x.match(sn)
    busName = y.groups()[0]
    if sensorSubType:
        return sensorType + '_' + sensorSubType + '_' + busName + '_' + str(setCounter) + ".csv"
    else:
        return sensorType + '_' + busName + '_' + str(setCounter) + ".csv"

def extractSensors(sensorsx, sensorSetCounter):
    sensorFileName = getSensorFileName(sensorsx, sensorSetCounter)
    if sensorFileName:
        with open(sensorFileName, "w") as outFile:
            tablewriter = csv.writer(outFile)
            for sensorx in sensorsx:
                if sensorx.tag == "sensor":
                    inverted = False
                    if "inverted" in sensorx.attrib:
                        inverted = sensorx.attrib['inverted'] == "true"
                    systemName = ""
                    userName = ""
                    for t in sensorx:
                        if t.tag == "systemName":
                            systemName = t.text
                        elif t.tag == "userName":
                            userName = t.text
                    tablewriter.writerow([str(systemName), str(userName), str(inverted)])

def main():
    tree = ET.parse('SampleData/test1.xml')
    root = tree.getroot()
    sensorSetCounter = 0
    for child in root:
        if child.tag == "sensors":
            sensorSetCounter += 1
            extractSensors(child, sensorSetCounter)

main()
