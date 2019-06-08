# GTA DragonFF - Blender scripts to edit basic GTA formats
# Copyright (C) 2019  Parik

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import map_structures
from collections import namedtuple

# Data types
Vector = namedtuple("Vector", "x y z")

# Base for all IPL / IDE section reader / writer classes
#######################################################
class GenericSectionUtility: 

    def __init__(self, sectionName, dataStructures):
        self.sectionName = sectionName
        self.dataStructures = dataStructures

    #######################################################
    def read(self, fileStream):

        entries = []

        line = fileStream.readline().strip()
        while line != "end":

            # Split line and trim individual elements
            lineParams = [e.strip() for e in line.split(",")]

            # Get the correct data structure for this section entry
            dataStructure = self.getDataStructure(lineParams)

            # Validate data structure
            if(dataStructure == None):
                print(type(self).__name__+" error: No appropriate data structure found")
                print("    Section name: " + self.sectionName)
                print("    Line parameters: " + str(lineParams))
            elif(len(dataStructure._fields) != len(lineParams)):
                print(
                    type(self).__name__+" error: Number of line parameters "
                    "doesn't match the number of structure fields."
                )
                print("    Section name: " + self.sectionName)
                print("    Data structure name: " + dataStructure.__name__)
                print("    Data structure: " + str(dataStructure._fields))
                print("    Line parameters: " + str(lineParams))
            else:
                # Add entry
                entries.append(dataStructure(*lineParams))
                # Read next line
                line = fileStream.readline().strip()

        return entries

    def getDataStructure(self, lineParams):
        return self.dataStructures[self.sectionName]

    #######################################################
    def write(self):
        pass

#######################################################
class OBJSSectionUtility(GenericSectionUtility):
    def getDataStructure(self, lineParams):

        if(len(lineParams) == 5):
            dataStructure = self.dataStructures["objs_1"]
        elif(len(lineParams) == 6):
            dataStructure = self.dataStructures["objs_2"]
        elif(len(lineParams) == 7):
            dataStructure = self.dataStructures["objs_3"]
        elif(len(lineParams) == 8):
            dataStructure = self.dataStructures["objs_4"]
        else:
            print(type(self).__name__ + " error: Unknown number of line parameters")
            dataStructure = None
        
        return dataStructure

#######################################################
class TOBJSectionUtility(GenericSectionUtility):
    def getDataStructure(self, lineParams):

        if(len(lineParams) == 7):
            dataStructure = self.dataStructures["tobj_1"]
        elif(len(lineParams) == 8):
            dataStructure = self.dataStructures["tobj_2"]
        elif(len(lineParams) == 9):
            dataStructure = self.dataStructures["tobj_3"]
        elif(len(lineParams) == 10):
            dataStructure = self.dataStructures["tobj_4"]
        else:
            print(type(self).__name__ + " error: Unknown number of line parameters")
            dataStructure = None
        
        return dataStructure

#######################################################
class CARSSectionUtility(GenericSectionUtility):
    def getDataStructure(self, lineParams):
        print("'cars' aren't yet implemented boi")


# List of IPL/IDE sections which require a section utility that's different
# from the default one.
specialSections = {
    'objs': OBJSSectionUtility,
    'tobj': TOBJSectionUtility,
    'cars': CARSSectionUtility
}

# Utility for reading / writing to map data files (.IPL, .IDE)
#######################################################
class MapDataUtility:

    # Returns a dictionary of sections found in the given file
    #######################################################
    def read(filename, dataStructures):

        print('\nMapDataUtility reading: ' + filename)

        sections = {}

        with open(filename) as fileStream:
            line = fileStream.readline().strip()
            while line:

                # Presume we have a section start
                sectionName = line
                sectionUtility = None

                if line in specialSections:
                    # Section requires some special reading / writing procedures
                    sectionUtility = specialSections[sectionName](sectionName, dataStructures)
                elif line in dataStructures:
                    # Section is generic, can be read / written to with the default utility
                    sectionUtility = GenericSectionUtility(sectionName, dataStructures)

                if sectionUtility != None:
                    sections[sectionName] = sectionUtility.read(fileStream)
                    print(sectionName + ': ' + str(len(sections[sectionName])) + ' entries')

                # Get next section
                line = fileStream.readline().strip()
        
        return sections