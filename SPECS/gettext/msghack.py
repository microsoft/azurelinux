#!/usr/bin/python3
## -*- coding: utf-8 -*-
## Copyright (C) 2001, 2004, 2008, 2012 Red Hat, Inc.
## Copyright (C) 2001 Trond Eivind Glomsrød <teg@redhat.com>

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A msghack replacement
"""

import sys

class GTMessage:
    """
    A class containing a message, its msgid and various references pointing at it
    """

    def __init__(self,id=None,message=None,refs=[]):
        """
        The constructor for the GTMessage class
        @self The object instance
        @message The message
        @id The messageid associated with the object
        """
        self._message=message.strip()
        self._id=id.strip()
        self._refs=[]
        for ref in refs:
            self._refs.append(ref)

    def __str__(self):
        """
        Return a string representation of the object
        @self The object instance
        """
        res=""
        for ref in self._refs:
            res=res+ref+"\n"
        res=res+"msgid %s\nmsgstr %s\n" % (self._id,self._message)
        return res

    def invertedStrings(self):
        """
        Returns a string representation, but with msgid and msgstr inverted.
        Note: Don't invert the "" string
        @self The object instance
        """
        res=""
        for ref in self._refs:
            res=res+ref+"\n"
        if not self._id=="\"\"":
            res=res+"msgid %s\nmsgstr %s\n" % (self._message,self._id)
        else:
            res=res+"msgid %s\nmsgstr %s\n" % (self._id,self._message)
        return res

    def emptyMsgStrings(self):
        """
        Return a string representation of the object, but leave the msgstr
        empty - create a pot file from a po file
        Note: Won't remove the "" string
        @self The object instance
        """
        res=""
        for ref in self._refs:
            res=res+ref+"\n"
        if not self._id=="\"\"":
            res=res+"msgid %s\nmsgstr \"\"\n" % (self._id)
        else:
            res=res+"msgid %s\nmsgstr %s\n" % (self._id,self._message)
        return res
        
    def compareMessage(self,msg):
        """
        Return  if the messages have identical msgids, 0 otherwise
        @self The object instance
        @msg The message to compare to
        """

        if self._id == msg._id:
            return 1
        return 0
        

class GTMasterMessage:
    """
    A class containing a message, its msgid and various references pointing at it
    The difference between GTMessage and GTMasterMessage is that this class
    can do less operations, but is able to store multiple msgstrs with identifiers
    (usually language, like 'msgst(no)'
    """

    def __init__(self,id=None,refs=[]):
        """
        The constructor for the GTMessage class
        @self The object instance
        @id The messageid associated with the object
        """
        self._id=id
        self._refs=[]
        self._messages=[]
        for ref in refs:
            self._refs.append(ref)

    def addMessage(self,message,identifier):
        """
        Add a new message and identifier to the GTMasterMessage object
        @self The object instance
        @message The message to append
        @identifier The identifier of the message
        """
        self._messages.append((identifier,message))

    def __str__(self):
        """
        Return a string representation of the object
        @self The object instance
        """
        res=""
        for ref in self._refs:
            res=res+ref+"\n"
        res=res+"msgid %s\n" % self._id
        for message in self._messages:
            res=res+"msgstr(%s) %s\n" %(message[0],message[1])
        res=res+"\n"
        return res

class GTFile:
    """
    A class containing the GTMessages contained in a file
    """

    def __init__(self,filename):
        """
        The constructor of the GTMFile class
        @self The object instance
        @filename The  file to initialize from
        """
        self._filename=filename
        self._messages=[]
        self.readFile(filename)

    def __str__(self):
        """
        Return a string representation of the object
        @self The object instance
        """
        res=""
        for message in self._messages:
            res=res+str(message)+"\n"
        return res

    def invertedStrings(self):
        """
        Return a string representation of the object, with msgid and msgstr
        swapped. Will remove duplicates...
        @self The object instance
        """

        msght={}
        msgar=[]

        for message in self._messages:
            if message._id=='""' and len(msgar)==0:
                msgar.append(GTMessage(message._id,message._message,message._refs))
                continue
            msg=GTMessage(message._message,message._id,message._refs)
            if msg._id not in msght:
                msght[msg._id]=msg
                msgar.append(msg)
            else:
                msg2=msght[msg._id]
                for ref in msg._refs:
                    msg2._refs.append(ref)
        res=""
        for message in msgar:
            res=res+str(message)+"\n"
        return res

    def msgidDupes(self):
        """
        Search for duplicates in the msgids.
        @self The object instance
        """
        msgids={}
        res=""
        for message in self._messages:
            msgid=message._id
            if msgid in msgids:
                res=res+"Duplicate: %s\n" % (msgid)
            else:
                msgids[msgid]=1
        return res

    def getMsgstr(self,msgid):
        """
        Return the msgstr matching the given id. 'None' if missing
        @self The object instance
        @msgid The msgid key
        """

        for message in self._messages:
            if msgid == message._id:
                return message._message
        return None

    def emptyMsgStrings(self):
        """
        Return a string representation of the object, but leave the msgstr
        empty - create a pot file from a po file
        @self The object instance
        """
        
        res=""
        for message in self._messages:
            res=res+message.emptyMsgStrings()+"\n"
        return res

            
    def append(self,B):
        """
        Append entries from dictionary B which aren't
        already present in this dictionary
        @self The object instance
        @B the dictionary to append messages from
        """

        for message in B._messages:
            if not self.getMsgstr(message._id):
                self._messages.append(message)
                

    def readFile(self,filename):
        """
        Read the contents of a file into the GTFile object
        @self The object instance
        @filename The name of the file to read
        """
        
        file=open(filename,"r")
        msgid=""
        msgstr=""
        refs=[]
        lines=[]
        inmsgid=0
        inmsgstr=0
        templines=file.readlines()
        for line in templines:
            lines.append(line.strip())
        for line in lines:
            pos=line.find('"')
            pos2=line.rfind('"')
            if line and line[0]=="#":
                refs.append(line.strip())
            if inmsgstr==0 and line[:6]=="msgstr":
                msgstr=""
                inmsgstr=1
                inmsgid=0
            if inmsgstr==1:
                if pos==-1:
                    inmsgstr=0
                    #Handle entries with and without "" consistently
                    if msgid[:2]=='""' and len(msgid)>4: 
                        msgid=msgid[2:]
                    if msgstr[:2]=='""' and len(msgstr)>4: 
                        msgstr=msgstr[2:]
                    message=GTMessage(msgid,msgstr,refs)
                    self._messages.append(message)
                    msgstr=""
                    msgid=""
                    refs=[]
                else:
                    msgstr=msgstr+line[pos:pos2+1]+"\n"
            if inmsgid==0 and line[:5]=="msgid":
                msgid=""
                inmsgid=1
            if inmsgid==1:
                if pos==-1:
                    inmsgid=0
                else:
                    msgid=msgid+line[pos:pos2+1]+"\n"
        if msgstr and msgid:
            message=GTMessage(msgid,msgstr,refs)
            self._messages.append(message)


class GTMaster:
    """
    A class containing a master catalogue of gettext dictionaries
    """

    def __init__(self,dicts):
        """
        The constructor for the GTMaster class
        @self The object instance
        @dicts An array of dictionaries to merge
        """
        self._messages=[]
        self.createMaster(dicts)

    def createMaster(self,dicts):
        """
        Create the master catalogue
        @self The object instance
        @dicts An array of dictionaries to merge
        """

        self._master=dicts[0]
        self._dicts=dicts[1:]

        for message in self._master._messages:
            gtm=GTMasterMessage(message._id,message._refs)
            gtm.addMessage(message._message,self._master._filename[:-3])
            for dict in self._dicts:
                res=dict.getMsgstr(message._id)
                if(res):
                    gtm.addMessage(res,dict._filename[:-3])
            self._messages.append(gtm)

    def __str__(self):
        """
        Return a string representation of the object
        @self The object instance
        """
        res=""
        for message in self._messages:
            res=res+str(message)+"\n"
        return res

def printUsage():
    "Print the usage messages"
    print("Usage: " + str(sys.argv[0]) + " [OPTION] file.po [ref.po]\n\
This program can be used to alter .po files in ways no sane mind would think about.\n\
    -o                result will be written to FILE\n\
    --invert          invert a po file by switching msgid and msgstr\n\
    --master          join any number of files in a master-formatted catalog\n\
    --empty           empty the contents of the .po file, creating a .pot\n\
    --append          append entries from ref.po that don't exist in file.po\n\
\n\
Note: It is just a replacement of msghack for backward support.\n")


if __name__=="__main__":
    output=None
    res=None
    if("-o") in sys.argv:
        if (len(sys.argv)<=sys.argv.index("-o")+1):
                print("file.po and ref.po are not specified!\n")
                printUsage()
                exit(1)
        output=sys.argv[sys.argv.index("-o")+1]
        sys.argv.remove("-o")
        sys.argv.remove(output)
    if("--invert") in sys.argv:
        if (len(sys.argv)<=sys.argv.index("--invert")+1):
            print("file.po is not specified!\n")
            printUsage()
            exit(1)
        file=sys.argv[sys.argv.index("--invert")+1]
        gtf=GTFile(file)
        res1=gtf.msgidDupes()
        if res1:
            sys.stderr.write(res1)
            sys.exit(1)
        res=str(gtf.invertedStrings())
    elif("--empty") in sys.argv:
        if (len(sys.argv)<=sys.argv.index("--empty")+1):
            print("file.po is not specified!\n")
            printUsage()
            exit(1)
        file=sys.argv[sys.argv.index("--empty")+1]
        gtf=GTFile(file)
        res=str(gtf.emptyMsgStrings())
    elif("--master") in sys.argv:
        if (len(sys.argv)<=sys.argv.index("--master")+1):
            print("file.po is not specified!\n")
            printUsage()
            exit(1)
        loc=sys.argv.index("--master")+1
        gtfs=[]
        for file in sys.argv[loc:]:
            gtfs.append(GTFile(file))
        master=GTMaster(gtfs)
        res=str(master)
    elif("--append") in sys.argv:
        if (len(sys.argv)<=sys.argv.index("--append")+2):
            print("file.po and/or ref.po are not specified!\n")
            printUsage()
            exit(1)
        file=sys.argv[sys.argv.index("--append")+1]
        file2=sys.argv[sys.argv.index("--append")+2]
        gtf=GTFile(file)
        gtf2=GTFile(file2)
        gtf.append(gtf2)
        res=str(gtf)
    else:
        #print("Not implemented: "+str(sys.argv))
        printUsage()
        sys.exit(1)
    if not output:
        print(res)
    else:
        file=open(output,"w")
        file.write(res)
    sys.exit(0)
