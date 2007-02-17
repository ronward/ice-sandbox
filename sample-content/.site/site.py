#
#    Copyright (C) 2005  Distance and e-Learning Centre, 
#    University of Southern Queensland
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import sys
if sys.path.count("../ice")==0: sys.path.append("../ice")
from ice_globals import *



class baseSite(icesite):
    def __init__(self):
        icesite.__init__(self)
        

    def traverse(self):
        title = "Ice web application"
        if self.node('packages'):
            title = "Packages"
            if self.node('courseware'):
                if self.renode( '^.*$', 'deptname' ):
                    if self.renode( '^.*$', 'coursecode' ):
                        if self.renode( '^\d\d\d\d$', 'year' ):
                            if self.renode( '^s\d$', 'semester' ):
                                self["package-path"] = self.pathToHere
            elif self.renode('^.*$', 'code'):
                ##HACK: These are required until we refactor the coursenode() method
                #self['coursecode'] = ''
                #self['deptname'] = ''
                #self['facname'] = ''
                #self['year'] = ''
                #self['semester'] = ''
                self["package-path"] = self.pathToHere
        elif self.node('courseware'):
            title = 'Courseware'
            if self.node('faculty'):
                if self.renode('^.+$', 'facname'):
                    title = self.getFacultyName(self['facname'])
                    if self.renode('^.+$', 'deptname'):
                        self["deptname"] = self["deptname"].upper()
                        title = self.getDepartmentName(self['deptname'])
                        if self.renode('^\d\d\d\d$', 'coursecode'):
                            if self.renode('^\d\d\d\d$', 'year'):
                                if self.renode('^s\d$', 'semester'):
                                    self["semester"] = self["semester"].upper() 
                                    self["package-path"] = self.pathToHere
        
        if self["package-path"] and self.rep.isdir(self["package-path"])==True:
            packageNode = True
        else:
            packageNode = False
            self["package-path"] = ""
            
        self._getManifest()
        self._executeFunction()
        
        if packageNode==True and self["body"]==None:
            if self.currentNode==None or self.currentNode=="default.htm":
                self._default_htm()
            elif self.currentNode=="toc.htm":
                self._toc_htm()
        
        if self["title"]==None:
            self["title"] = title
    

# ++++ Extra ICE Function ++++

from ice_functions import addFunction, removeFunction, replaceFunction, getFunction, packageOnly, itemOnly, packageRootOnly

#Sample local (Ice) function
def sampleFunction(self):
    print "sampleFunction()"
    l = self.rep.listdir(self["package-path"] + "/.skin/templates")
    s = ""
    for i in l:
        s += os.path.splitext(i)[0] + "<br/>"
    self['body'] = s
    self['statusbar'] = "Sample status bar text!<br/>The end."
#addFunction(sampleFunction, position=19, postRequired=False, label="Sample", title="Just a simple sample function")











