"""Class holding all attributes related to preprocessing textFiles"""

import os
import csv
import numpy as np
import collections
from datetime import datetime

class PreprocessTextfiles:     
    # Column numbers
    tagCol = 0
    timeCol = 1
    dateCol = 2
    actionCol = 3   
    
    # string constants that define textFile
    seshStart_str = 'SeshStart'
    seshEnd_str = 'SeshEnd'   
    seshStartTag_str = '0000000000'
    seshEndTag_str = '0000000000'  
    
    def __init__(self, workingDir, foldersToIgnore):
        self.workingDir = workingDir
        self.foldersToIgnore = foldersToIgnore 
        
        self.txtList = self.getAllTextLocs(workingDir)
        self.textDict =self.importTextsToDict(self.txtList)
        
        self.linesSorted = []
        for i in range(len(self.textDict.items())):
            self.linesSorted.extend(self.textDict.items()[i][1]) 
            
        self.binnedLines = None
        
    def getAllTextLocs(self,workingDir):
        """
        Get a list of all text files in the given folder (including subdirectories)
        """
        txtList = []
        for root, dirs, files in os.walk(workingDir):
            for file in files:
                if file.endswith(".txt"):
                    print(os.path.join(root, file))
                    txtList.append(os.path.join(root, file))
        return txtList
    
    def importTextsToListofMat(self,txtList):
        """
        Import viable textFiles to a list of matrices
        Returns:
            [(lines,textFileLoc)] (tuple)
            lines: The lines of the textfile as a 2D list
            textFileLoc: The path of each textFile that was imported.      
        """    
        lines = []  
        textFileLoc=[]
        # Append them all into one matrix (the ones with the appropriate number of columns)
        for i in range(len(txtList)):
            textFile = txtList[i]
            try:
                with open(textFile) as f:
                    reader = csv.reader(f, delimiter="\t")
                    newLines = list(reader)
                print(str(len(newLines))+" - "+textFile)
                # Only consider textFile with more than 2 rows and that have 'SeshStart' in first line                                                                                               
                if len(newLines) > 2 and newLines[0][self.actionCol]==self.seshStart_str:
                    # Add a row for textFiles missing a SeshEnd          
                    if newLines[-1][self.actionCol] != self.seshEnd_str: 
                        newLines.append(newLines[-1][:])
                        newLines[-1][self.actionCol] = self.seshEnd_str
                        newLines[-1][self.tagCol] = self.seshEndTag_str
                    lines.append(newLines)
                    textFileLoc.append(txtList[i])
                else:
                    print("Text file does not have enough rows - "+textFile)
            except BaseException:
                print("Text file does not have enough columns - "+textFile)
        return(zip(lines,textFileLoc))
        
    def sort_X_BasedOn_Y_BeingSorted(self,X,Y):
        """Sorts X based on the result from Y being sorted"""
        X = np.array(X)
        Y = np.array(Y)
        inds = Y.argsort()
        return(X[inds]) 
    
    def getDupes(self,):
        """Return a tuple of text file locations and their startSeshes that have been identified as duplicates, ordered by StartSesh"""
        # Remove the text files that have the same start time as another     
        startSeshes = []
        for i in range(len(lines)):
            startSeshes.append(lines[i][0][self.timeCol])
        
        def equalToAnother(elem):
            return (startSeshes.count(elem) > 1)
            
        def NOTequalToAnother(elem):
            return (startSeshes.count(elem) == 1)  
        
        # Indices of all text files that are duplicates of another and those that are unique
        equalStartInd=map(equalToAnother,startSeshes)
        notEqualStartInd = map(NOTequalToAnother, startSeshes)
        
        # Retrieve text file names and start times that have duplicates
        textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
        startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
        
    
    
    def importTextsToDict(self,txtList):
        """
        Return a dictionary that has each path of each text file as the key to a matrix that contains all the lines of each text file - duplicates removed, ordered by textFile startseshes
        """
        workingDir = self.workingDir
        txtList = self.getAllTextLocs(workingDir)
        # Remove all the paths that are subdirectories of the ignore folders
        for i in range(len(self.foldersToIgnore)):
            txtList=[x for x in txtList if not (self.foldersToIgnore[i] in x)]
        
        # Lines contains the lines from each text file where lines[i] contains all the lines of the i'th text file
        ListofMat=self.importTextsToListofMat(txtList)           
        lines = zip(*ListofMat)[0]
        textFileLoc = zip(*ListofMat)[1]         
        
        ###
        
        # Remove the text files that have the same start time as another     
        startSeshes = []
        for i in range(len(lines)):
            startSeshes.append(lines[i][0][self.timeCol])
        
        def equalToAnother(elem):
            return (startSeshes.count(elem) > 1)
            
        def NOTequalToAnother(elem):
            return (startSeshes.count(elem) == 1)  
        
        # Indices of all text files that are duplicates of another and those that are unique
        equalStartInd=map(equalToAnother,startSeshes)
        notEqualStartInd = map(NOTequalToAnother, startSeshes)
        
        # Retrieve text file names and start times that have duplicates
        textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
        startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
        
        # Remove the text files that have the same start time as another     
        startSeshes = []
        for i in range(len(lines)):
            startSeshes.append(lines[i][0][self.timeCol])
        
        def equalToAnother(elem):
            return (startSeshes.count(elem) > 1)
            
        def NOTequalToAnother(elem):
            return (startSeshes.count(elem) == 1)  
        
        # Indices of all text files that are duplicates of another and those that are unique
        equalStartInd=map(equalToAnother,startSeshes)
        notEqualStartInd = map(NOTequalToAnother, startSeshes)
        
        # Retrieve text file names and start times that have duplicates
        textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
        startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
        
        # Sort these text files by start time  
        textFileEquals = self.sort_X_BasedOn_Y_BeingSorted(textFileEquals,startTimeEquals)
        startTimeEquals = self.sort_X_BasedOn_Y_BeingSorted(startTimeEquals,startTimeEquals)
        
        textFileEqualsOnlyOne = [] # you are the only one baby!
        startTimeEqualsOnlyOne = []
        # Create a list that only contains one (any one) of the textFiles that have a duplicate
        for i in range(len(startTimeEquals)):
            if i != range(len(startTimeEquals))[-1]:
                if startTimeEquals[i] != startTimeEquals[i+1]:
                    startTimeEqualsOnlyOne.append(startTimeEquals[i])
                    textFileEqualsOnlyOne.append(textFileEquals[i])
            else:
                    startTimeEqualsOnlyOne.append(startTimeEquals[i])
                    textFileEqualsOnlyOne.append(textFileEquals[i])
        
        # Remove all the text files that have a duplicate (another text file with identical startSesh) 
        # notEqualStartInd - indices of all text files that have unique startSeshes
        lines = np.asarray(lines)[np.asarray(notEqualStartInd)]
        lines = lines.tolist()
        textFileLoc = np.asarray(textFileLoc)[np.asarray(notEqualStartInd)]
        textFileLoc = textFileLoc.tolist()
        startSeshes = np.asarray(startSeshes)[np.asarray(notEqualStartInd)]
        startSeshes = startSeshes.tolist()
            
        # Right, and now add only one of each of the duplicates back to 'lines'
        #[linesOneDup,textFileLocOneDup]=importTextsToListofMat(textFileEqualsOnlyOne) 
        ListofMat=self.importTextsToListofMat(textFileEqualsOnlyOne)           
        linesOneDup = zip(*ListofMat)[0]
        textFileLocOneDup = zip(*ListofMat)[1]
        
        for linesToAdd in linesOneDup:
            lines.append(linesToAdd)
        for locToAdd in textFileLocOneDup:
            textFileLoc.append(locToAdd)  
        
        # Sort the text file contents and names by startSeshes
        textFileLoc = self.sort_X_BasedOn_Y_BeingSorted(textFileLoc,startSeshes)
        lines = self.sort_X_BasedOn_Y_BeingSorted(lines,startSeshes)
        
        # Add these two to a dictionary
        textDict = collections.OrderedDict(zip(textFileLoc, lines))                           
        return textDict
        
    def getCol(self,listOfLists,colNum):
        """return desired column from list of lists as a list"""
        #print(colNum)
        #print(listOfLists)
        print("getCol "+str(len(listOfLists)))
        print("getCol "+str(listOfLists[0]))
        return list(np.asarray(listOfLists)[:,colNum])
    
    def convertToUsefulDate(self,DateList): 
        """returns a list of dates converted to date objects"""                                                                                                                                                                                                
        DateList_pr = DateList[:]
        # Convert dates to date objects that are useable
        for i in range(len(DateList_pr)):
            DateList_pr[i]=(datetime.strptime(DateList[i], '%Y-%m-%d %H:%M:%S.%f'))   
        return DateList_pr                                                                                                                                                                                                     
    
    def eAnd(self,*args):
        return [all(tuple) for tuple in zip(*args)]
    

    def setBins(self,binTime):
        """    
        Bin list of all sorted lines into per binTime lists
        For your convenience: there are 86400 seconds in a day
        Returns: BinnedList: np.array([[a],[b]...]) where the first line in a,b... is binTime seconds before the last
        """  
        linesSorted = self.linesSorted
        columnOfTimes = self.getCol(linesSorted,self.timeCol)
        columnOfTimes = [ float(x) for x in columnOfTimes]
        columnOfTimes = np.array(columnOfTimes)
        linesSorted = np.array(linesSorted)
        
        binnedLines = []
        startInd = columnOfTimes[0]
        endInd = startInd + binTime
        
        while endInd <= columnOfTimes[len(columnOfTimes)-1]:
            theBin = linesSorted[np.array(self.eAnd(columnOfTimes>=startInd,columnOfTimes<endInd))]
            #theBin=theBin.tolist()
            binnedLines.append(theBin)
            startInd = endInd
            endInd = endInd + binTime
            print('bin created from ' + str(startInd) + ' to ' + str(endInd))
            
        self.binnedLines = binnedLines
        
    def getBins():
        if self.binnedLines == None:
            assert(1==0,'binnedLines have not been set')
        return self.binnedLines
            
    def getCol_binnedLines(self,colNum):        
        """return list of lists that would be the binned lists of a particular column"""
        if self.binnedLines == None:
            assert(1==0,'binnedLines have not been set')
        binnedLines_col = []
        flag = 0
        for lines in self.binnedLines:
            print("getCol_binnedLines "+str(flag))
            if len(lines) > 0:
                binnedLines_col.append(self.getCol(lines,colNum))
            else:
                print('getCol_binnedLines - NOTHING APPENDED')
            flag = flag +1
        return binnedLines_col
    
    def getBinnedRows_tag(self,chosenTags):
        """return list of lists that are all binned lines that are by a mouse in tags """
        if self.binnedLines == None:
            assert(1==0,'binnedLines have not been set')
        binnedLines_tags = []
        
        for lines in self.binnedLines:
            theBin = []
            for line in lines:
                if int(line[self.tagCol]) in chosenTags:
                    theBin.append(line)
            binnedLines_tags.append(theBin)
        return binnedLines_tags
    
    def getFreqList_binned(self,item,colNum):
        """return list of list that is the count of the occurence of 'item' in each list (in column colNum) in binnedList """
        if self.binnedLines == None:
            assert(1==0,'binnedLines have not been set')
        freqs = []
        
        chosenCol = self.getCol_binnedLines(self.binnedLines,colNum)
        for its in chosenCol:
            freqs.append(its.count(item)) 
        return freqs
            
    def findFreqsForEach(self,item,colNum,chosenTags):
        """return list of list that is the counts for each mouse for each bin for 'item'"""
        if self.binnedLines == None:
            assert(1==0,'binnedLines have not been set')
        freqsForEach = []
        for lines in self.binnedLines:
            freqsForBin = []
            for tag in chosenTags:
                tagRowsBin = self.getBinnedRows_tag([lines],[tag])
                print("findFreqsForEach "+str(len( tagRowsBin))) #should not be 62
                if len( tagRowsBin[0]) == 0:
                    print('WE GOT HERE!!!')
                    freqsForBin.append(0)
                else: 
                    freqsForBin.append(self.getFreqList_binned(tagRowsBin,item,colNum)[0])
            freqsForEach.append(freqsForBin)
        return freqsForEach
 
workingDir = "T:/AutoHeadFix/"
foldersToIgnore = ["Old and or nasty data goes here"]      
test = PreprocessTextfiles(workingDir,foldersToIgnore)
