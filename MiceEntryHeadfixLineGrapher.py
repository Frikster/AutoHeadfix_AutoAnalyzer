# Plot line graphs of each mouse's entry and headFix 
# Author: Dirk
# Last edited: 2015-08-13

### INPUT ###
# Change workingDir to the folder containing all the text files you want analyzed
# Code will locate all text files in all subdirectories in the path provided

import os
import filecmp
import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re
import csv
#import statistics #Only with Python 3
from datetime import datetime


import time
from bokeh.plotting import figure, output_server, cursession, show


"""
args:
    workingDir (str): Full path of the directory that contains all textFiles to be analyzed
    foldersToIgnore ([str]): List of folders that are ignored. Only the folders name is required, not each one's full path

Typical example:
workingDir = T:/AutoHeadFix/
foldersToIgnore = ["Old and or nasty data goes here"]
"""
# TODO: use user-input
#workingDir = raw_input("Please type in the working directory: ")
#foldersToIgnore = raw_input("Please type in a list of folders to ignore: ")
workingDir = "T:/AutoHeadFix/"
foldersToIgnore = ["Old and or nasty data goes here"]
outputLoc = "C:\\Users\\user\\Downloads\\"

#def init():
    #"""
    #    Initialize globals
    #"""
# Column numbers
global tagCol
tagCol = 0
global timeCol
timeCol = 1
global dateCol 
dateCol = 2
global actionCol
actionCol = 3   

# string constants that define textFile
global seshStart_str
seshStart_str = 'SeshStart'
global seshEnd_str
seshEnd_str = 'SeshEnd'

global seshStartTag_str
seshStartTag_str = '0000000000'
global seshEndTag_str
seshEndTag_str = '0000000000' 

global miceGroups    
miceGroups = {
    'EL':[2015050115,1312000377,1312000159,1302000245,1312000300],
    'EP': [1302000139,2015050202,1412000238],
    'AB': [1312000592,1312000573,1312000090]
}
global tags
tags = []
for i in range(len(miceGroups.items())):
    tags.extend(miceGroups.items()[i][1])
#init()

    
def getAllTextLocs(workingDir):
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
  
def importTextsToListofMat(txtList):
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
            if len(newLines) > 2 and newLines[0][actionCol]==seshStart_str:
                # Add a row for textFiles missing a SeshEnd          
                if newLines[-1][actionCol] != seshEnd_str: 
                    newLines.append(newLines[-1][:])
                    newLines[-1][actionCol] = seshEnd_str
                    newLines[-1][tagCol] = seshEndTag_str
                lines.append(newLines)
                textFileLoc.append(txtList[i])
            else:
                print("Text file does not have enough rows - "+textFile)
        except BaseException:
            print("Text file does not have enough columns - "+textFile)
    return(zip(lines,textFileLoc))
                                                                 
def dupes(textDirs):
    """
    returns [(leDupe1,leDupe2)]
        leDupe1: text file that has the same content as corresponding text file leDupe2
    """ 
    leDupe1 = []
    leDupe2 = [] 
    for textDir1 in textDirs:
        for textDir2 in textDirs:
            if filecmp.cmp(textDir1, textDir2, shallow=False):   
                leDupe1.append(textDir1)
                leDupe2.append(textDir2)
    return(zip(leDupe1,leDupe2))                                                                                                              
                                                                                                                                    
def equalStarts(textDirs):
    """
    returns [(leDupe1,leDupe2)]
        leDupe1: text file that has the same startSesh as corresponding text file leDupe2
    """ 
    leDupe1 = []
    leDupe2 = [] 
    for textDir1 in textDirs:
        for textDir2 in textDirs:      
            with open(textDir1) as f:
                reader = csv.reader(f, delimiter="\t")
                txtLines1 = list(reader)
                
            with open(textDir2) as f:
                reader = csv.reader(f, delimiter="\t")
                txtLines2 = list(reader)
                
# Dis funktion does it all yo
# Input: Just give me the tag of the mouse dawg, I'll get the dirt on her
# Returns: [headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr,headFixFreq,entryFreq]
# headFixRates = list of number of headfixes per hour
# entryRates = list of entries of headfixes per hour
# endMinusStartList = list of durations for each session
# startTimesList = list of starting times for each session examined
# startDateList_pr = list of starting dates for each session examined
# headFixFreq = list of numer of headfixes
# entryFreq = list of numer of entries
def badAssFunk(tag,lines):  
    headFixRatesList = []
    entryRates = []
    endMinusStartList = []
    startTimesList = []
    startDateList_pr = []   
    headFixFreq = []
    entryFreq = []
    # Not returned
    startDateList = []
    
    for singleTextLines in lines: 
        # Retrieve column of tags
        columnOfTags=np.asarray(singleTextLines)[:,tagCol]
        columnOfTags = [ int(x) for x in columnOfTags ]
    
        if tag in  columnOfTags:   
            # Find end - start
            startTime = singleTextLines[0][timeCol]
            startTimesList.append(startTime[:])
            endTime = singleTextLines[-1][timeCol]
            # Convert to hours
            endMinusStart = float(endTime)/3600 - float(startTime)/3600
            
            # Get all the lines in the current text file associated with the current tag
            chosenLinesThisFile=np.asarray(singleTextLines)[np.transpose(columnOfTags)==tag]        
            
            times=chosenLinesThisFile[:,timeCol].astype(np.float)
            actions=chosenLinesThisFile[:,actionCol] 
            # Replace "reward0" with "headfix"
            for j in xrange(0,np.size(actions)):
                actions[j] = re.sub('reward0', 'headfix', actions[j])
            #Collapse rewards into a single variable  
            for j in xrange(0,np.size(actions)):
                actions[j] = re.sub('reward.', 'reward', actions[j]) 
            #Remove all actions other than headfix and entry      
            times=times[np.logical_or(actions=='entry',actions=='headfix')]
            actions=actions[np.logical_or(actions=='entry',actions=='headfix')]    
            assert(times.size ==  actions.size),("There are either more times than actions or more actions than times for mouse: "+str(i))
            
            # Retrieve counts of each tracked variable
            headFixFreq.append(actions.tolist().count('headfix')) 
            entryFreq.append(actions.tolist().count('entry')) 
            endMinusStartList.append(endMinusStart)
            # Add the startDate
            startDateList.append(singleTextLines[0][dateCol])
        
    for i in range(len(endMinusStartList)):
        headFixFreq[i] = headFixFreq[i]/endMinusStartList[i]
        entryFreq[i] = entryFreq[i] /endMinusStartList[i]
     
    # Sort it
    headFixRates = np.array(headFixFreq)
    entryRates = np.array(entryFreq)    
    startTimesList = np.array(startTimesList) 
    startDateList = np.array(startDateList)  
    
    inds = startTimesList.argsort()

    headFixRates = headFixRates[inds] 
    entryRates = entryRates[inds]
    startDateList = startDateList[inds]
    
    startDateList_pr = startDateList.tolist()[:]
    # Convert dates to date objects
    for i in range(len(startDateList_pr)):
        startDateList_pr[i]=(datetime.strptime(startDateList[i], '%Y-%m-%d %H:%M:%S.%f'))        
    return([headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr,headFixFreq,entryFreq])
    
# Retrieve all the data for all the plots and make list of lists (what did you expect?) 
def retrieveDataForTags(tags,lines):
    headFixRatesList = []
    entryRatesList = []
    endMinusStartListList = []
    startTimesListList = []
    startDateList_prList = []
    
    for tag in tags:
        [headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr,headFixFreq,entryFreq]=badAssFunk(tag,lines)
        headFixRatesList.append(headFixRates)
        entryRatesList.append(entryRates)
        endMinusStartListList.append(endMinusStartList)
        startTimesListList.append(startTimesList)
        startDateList_prList.append(startDateList_pr)
   
    assert(len(headFixRatesList)==len(entryRatesList)==len(endMinusStartListList)==len(startTimesListList)==len(startDateList_prList))   
    return ([headFixRatesList,entryRatesList,endMinusStartListList,startTimesListList,startDateList_prList])

# Generate Plots
def genPlots(headFixRatesList,entryRatesList,startTimesListList,startDateList_prList):
    for i in range(len(headFixRatesList)):  
        # TODO: FIX THAT THIS ONLY WORKS IF PLOTTING ALL TAGS
        tag = tags[i]                       
        #fig = plt.figure()
        fig,ax = plt.subplots()
        ax.plot(startDateList_prList[i],headFixRatesList[i],startDateList_prList[i],entryRatesList[i])  
        green_line = mpatches.Patch(color='green', label='Entries')
        blue_line = mpatches.Patch(color='blue', label='Headfixes') 
        ax.legend(handles=[green_line,blue_line])  
        fig.autofmt_xdate()
        
        plt.title("Mouse "+str(tag))
        plt.ylabel("Rate (per hour)")
        plt.xlabel("Date")
        
        #Save each fig to outputLoc
        plt.savefig(outputLoc+"Mouse "+str(tag)+".png", bbox_inches='tight')
        
    plt.show()
                        
txtList = getAllTextLocs(workingDir)
# Remove all the paths that are subdirectories of the ignore folders
for i in range(len(foldersToIgnore)):
    txtList=[x for x in txtList if not (foldersToIgnore[i] in x)]

# Lines containts the lines from each text file where lines[i] contains all the lines of the i'th text file
ListofMat=importTextsToListofMat(txtList)           
lines = zip(*ListofMat)[0]
textFileLoc = zip(*ListofMat)[1]        
 
# Remove the text files that have the same start time as another     
equalStartTest = []
for i in range(len(lines)):
    equalStartTest.append(lines[i][0][timeCol])

def equalToAnother(elem):
    return (equalStartTest.count(elem) > 1)
    
def NOTequalToAnother(elem):
    return (equalStartTest.count(elem) == 1)  

# Indices of all text files that are duplicates of another and those that are unique
equalStartInd=map(equalToAnother,equalStartTest)
notEqualStartInd = map(NOTequalToAnother, equalStartTest)

# Retrieve text file names that and start times that have duplicates
textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
startTimeEquals=np.asarray(equalStartTest)[np.asarray(equalStartInd)]

# Sort these text files by start time
inds = startTimeEquals.argsort()
textFileEquals = textFileEquals[inds] 
startTimeEquals = startTimeEquals[inds]

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

# Get a list of all textFiles that are unique

# Right, and now add only one of each of the duplicates back to 'lines'
#[linesOneDup,textFileLocOneDup]=importTextsToListofMat(textFileEqualsOnlyOne) 
ListofMat=importTextsToListofMat(textFileEqualsOnlyOne)           
linesOneDup = zip(*ListofMat)[0]
textFileLocOneDup = zip(*ListofMat)[1]

for linesToAdd in linesOneDup:
    lines.append(linesToAdd)
                                                         
[headFixRatesList,entryRatesList,endMinusStartListList,startTimesListList,startDateList_prList]=retrieveDataForTags(tags,lines)

########### BOKEH
# prepare output to server
output_server("MiceRateLine")

p = figure(plot_width=400, plot_height=400)

p.line(startDateList_prList[1],headFixRatesList[1],name='Headfix Rate')
p.line(startDateList_prList[1],entryRatesList[1],name='Entry Rate')

show(p)
############

genPlots(headFixRatesList,entryRatesList,startTimesListList,startDateList_prList)                                                                                                          
                                                                                                                                                                                                                                                                                                                                          
# for each group find midpoint for each rate and stddev for error bars  

######### OVER HERE YOU ARE ONLY PICKING ONE GROUP -> ALTER FOR LATER


miceGroups = {
    'EL+EP':[2015050115,1312000377,1312000159,1302000245,1312000300,1302000139,2015050202,1412000238],
    'EL':[2015050115,1312000377,1312000159,1302000245,1312000300],
    'EP': [1302000139,2015050202,1412000238],
    'AB': [1312000592,1312000573,1312000090]
}



for k in miceGroups.keys():
    [headFixRatesList,entryRatesList,endMinusStartListList,startTimesListList,startDateList_prList]=retrieveDataForTags(miceGroups[k],lines)
    # longest startDateList is the x-axis as it has no missing values
    startTimesGr=max(startTimesListList,key=len)
    startDatesGr= max(startDateList_prList,key=len)
    
    
    # Example for stack overflow porblems
    
    #x=[1,2,3,4,5,6,7,8,9]
    #y=[[1,2,4,5,6,9],[1,1,1,1,1,1]]
    #
    #[for i in y[1] if y[0]]
    # Output should be: [1,1,0,1,1,1,0,0,1]
    
    newHeadFixRates = []
    newEntryRates = []
    # Create lists of appropriate length of zeros
    for hfr in headFixRatesList:
        newHeadFixRates.append(np.zeros(len(startTimesGr)))
        newEntryRates.append(np.zeros(len(startTimesGr)))
    
    
    # next fill in values in correct locations
    for i in range(len(newHeadFixRates)):  
        for rowNum in range(len(newHeadFixRates[i])): 
            if startTimesGr[rowNum] in startTimesListList[i]:
                prevRowno = np.where(startTimesListList[i]==startTimesGr[rowNum])[0][0]
                newHeadFixRates[i][rowNum] = headFixRatesList[i][prevRowno]
                newEntryRates[i][rowNum] = entryRatesList[i][prevRowno]            
    
    def mean(data):
        """Return the sample arithmetic mean of data."""
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        return sum(data)/n # in Python 2 use sum(data)/float(n)
    
    def _ss(data):
        """Return sum of square deviations of sequence data."""
        c = mean(data)
        ss = sum((x-c)**2 for x in data)
        return ss 
                                
    def pstdev(data):
        """Calculates the population standard deviation."""
        n = len(data)
        if n < 2:
            raise ValueError('variance requires at least two data points')
        ss = _ss(data)
        pvar = ss/n # the population variance
        return pvar**0.5                                
                                                                    
    # compute means and yerr    
    newHeadFixRates_rows=list(map(list,zip(*newHeadFixRates)))
    newEntryRates_rows=list(map(list,zip(*newEntryRates)))
    headfixAvgs = map(mean,newHeadFixRates_rows)
    entryRatesAvgs = map(mean,newEntryRates_rows)
    headfixErrs = map(pstdev,newHeadFixRates_rows)
    entryRateserrs = map(pstdev,newEntryRates_rows)
        
    # Titles
    tit1="Mouse Group "+ k + " Headfixes"
    tit2="Mouse Group "+ k + " Entries"
    tit3="Mouse Group "+ k
    
    fig,ax = plt.subplots()
    plt.errorbar(startDatesGr,headfixAvgs,yerr=headfixErrs) 
    plt.title(tit1)
    plt.ylabel("Average Rate (per hour)")
    plt.xlabel("Date")
    fig.autofmt_xdate()
    plt.savefig(outputLoc+tit1+".png", bbox_inches='tight')
    fig,ax = plt.subplots()
    plt.errorbar(startDatesGr,entryRatesAvgs,yerr=entryRateserrs,color='g') 
    plt.title(tit2)
    plt.ylabel("Average Rate (per hour)")
    plt.xlabel("Date") 
    fig.autofmt_xdate()
    plt.savefig(outputLoc+tit2+".png", bbox_inches='tight')

    fig,ax = plt.subplots()
    plt.errorbar(startDatesGr,headfixAvgs,yerr=headfixErrs)
    plt.errorbar(startDatesGr,entryRatesAvgs,yerr=entryRateserrs)  
    green_line = mpatches.Patch(color='green', label='Entries')
    blue_line = mpatches.Patch(color='blue', label='Headfixes') 
    plt.legend(handles=[green_line,blue_line])  
    plt.title(tit3)
    plt.ylabel("Average Rate (per hour)")
    plt.xlabel("Date")
    fig.autofmt_xdate()
    plt.savefig(outputLoc+tit3+".png", bbox_inches='tight')

                                                                                                                                                                    
                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
## Add zeros for times where some mice have no action (use startTimes of mouse that did do something)
#newHeadFixRates = (headFixRatesList)
#newEntryRates = (entryRatesList)
#for i in range(len(headFixRatesList)): 
#    
#    #####   
#    lensHFR=[len(headFixRatesList[i]) for i in range(len(headFixRatesList))]
#    lensER=[len(newEntryRates[i]) for i in range(len(newEntryRates))]
#    assert(lensHFR==lensER)
#    
#    totalInsertsNeeded = (len(startTimesGr)*len(startTimesListList)) - (sum(lensER))
#    # max no of loops to make worst case insertions
#    maxLoops = reduce(lambda x,y:x*y,lensER)
#    #####
#    
#    
#    
#    
#    # start looping from the start again once an insertion is made
#    while totalInsertsNeeded > 0 and maxLoops > 0:
#        print("maxLoops:"+str(maxLoops))
#        assert(totalInsertsNeeded<maxLoops)
#        # Loops through each row of rates and times for each tag
#        rows=list(map(list,zip(*[headFixRatesList[i],entryRatesList[i],startTimesListList[i]])))
#        for rowNum in range(len(rows)):
#            # note: th index in this if statement comes from the placement of lists in variable "rows" above
#            if rows[rowNum][2]!=startTimesGr[rowNum]:
#                # Insert zero rates if a time is found that is not in startTimesGr
#                newHeadFixRates[i]=np.insert(newHeadFixRates[i],rowNum,0)
#                newEntryRatesList[i]=np.insert(newEntryRatesList[i],rowNum,0)
#                totalInsertsNeeded = totalInsertsNeeded - 1
#                print("totalInsertsNeeded"+str(totalInsertsNeeded))
#                break
#        maxLoops = maxLoops - 1
        

#for headFixRates in headFixRatesList[len(headFixRatesList)<len(startTimesGr)]:
#    for rate in headFixRates:
#        if 

    


###################### TODO: Generate subplots                                                                                                                                                                  
                                                                                                                                                                                                                                                                          
                                                                                                                    
#number_of_subplots=len(tags) 
#numRows=int(np.floor(np.sqrt(len(tags)))) 
#numCols =int(np.ceil(np.sqrt(len(tags))))
#j = 0


 # for tag in tags:
 #   #chosenLines = []
 #   headFixFreq = []
 #   entryFreq = []
 #   endMinusStartList = []
 #   startTimesList = []
 #   startDateList = []   
    
 # Attempt to make subplots                                     
 # fig, ax = plt.subplots(ncols=int(np.floor(np.sqrt(len(tags)))),nrows=int(np.ceil(np.sqrt(len(tags)))))



## Start with one
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(startDateList_prList[0],headFixRatesList[0],startDateList_prList[0],entryRatesList[0])  
#green_line = mpatches.Patch(color='green', label='Entries')
#blue_line = mpatches.Patch(color='blue', label='Headfixes') 
#ax.legend(handles=[green_line,blue_line])  
#fig.autofmt_xdate()
#
#plt.title("Mouse "+str(tag))
#plt.ylabel("Rate (per hour)")
#plt.xlabel("Date")
#
#
## add moar subplots
#for i in range(number_of_subplots):
#    if i > 0:
#        n = len(fig.axes)
#        for j in range(n):
#            fig.axes[j].change_geometry(n+1, numCols, j+1)
#        
#        # Add the new
#        ax = fig.add_subplot(n+1, 1, n+1)
#        ax.plot(startDateList_prList[i],headFixRatesList[i],startDateList_prList[i],entryRatesList[i])  
#        green_line = mpatches.Patch(color='green', label='Entries')
#        blue_line = mpatches.Patch(color='blue', label='Headfixes') 
#        ax.legend(handles=[green_line,blue_line])  
#        fig.autofmt_xdate()
#
#        plt.title("Mouse "+str(tag))
#        plt.ylabel("Rate (per hour)")
#        plt.xlabel("Date")
#        
#        plt.show() 



     
#import math
#
#import matplotlib.pyplot as plt
#from matplotlib import gridspec
#
#def do_plot(ax):
#    ax.plot([1,2,3], [4,5,6], 'k.')
#
#
#N = 11
#cols = 3
#rows = math.ceil(N / cols)
#
#gs = gridspec.GridSpec(rows, cols)
#fig = plt.figure()
#for n in range(N):
#    ax = fig.add_subplot(gs[n])
#    do_plot(ax)
#
#fig.tight_layout() 