"""Plot line graphs of each mouse's entry and headFix 
Author: Dirk
Last edited: 2015-08-13

args:
    workingDir (str): Full path of the directory that contains all textFiles to be analyzed
    foldersToIgnore ([str]): List of folders that are ignored. Only the folders name is required, not each one's full path

Typical example:
workingDir = T:/AutoHeadFix/
foldersToIgnore = ["Old and or nasty data goes here"]
"""
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
import collections
import itertools

import time
from bokeh.plotting import figure, output_server, cursession, show

workingDir = "T:/AutoHeadFix/"
foldersToIgnore = ["Old and or nasty data goes here"]
outputLoc = "C:\\Users\\user\\Downloads\\"

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
    
global binTime
binTime = 86400

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
              

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#def returnDictItemsInList(dictionary):
#    itemList = []
#    for i in range(len(dictionary.items())):
#        itemList.extend(dictionary.items()[i][1]) 
#    return itemList
#
#def returnDictKeysInList(dictionary):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
#    keyList = []
#    for i in range(len(dictionary.keys())):
#        keyList.extend(dictionary.keys()[i][0])
#    return keyList 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    
                            
# Retrieve all the data for all the plots and make dictionary (what did you expect?) 
# Returns: {textFileLocList : [lines,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr]}
# textDict = dict(zip(textFileLoc, lines)) 
def retrieveDataForTags(tags,textDict):
    #headFixRatesList = []
    #entryRatesList = []
    #endMinusStartListList = []
    #startTimesListList = []
    #startDateList_prList = []
    #headFixFreqList = []
    #entryFreqList = []
    #textFileLocListList = []
    
    textStatsDict_Tags = {}
    
    for tag in tags:
        #[textFileLocList,linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr]
        textStatsDict=badAssFunk(tag,textDict)        
        textStatsDict_Tags[tag]= textStatsDict  
    return (textStatsDict_Tags)   
   
          #####  
        #headFixRatesList.append(headFixRates)
        #entryRatesList.append(entryRates)
        #endMinusStartListList.append(endMinusStartList)
        #startTimesListList.append(startTimesList)
        #startDateList_prList.append(startDateList_pr)
        #headFixFreqList.append(headFixFreq)
        #entryFreqList.append(entryFreq)
        #textFileLocListList.append(textFileLocList)
   
    #assert(len(headFixRatesList)==len(entryRatesList)==len(endMinusStartListList)==len(startTimesListList)==len(startDateList_prList))   
    


#class textStatsDict(object):
#    """
#    Defines a struct where tag(s) are the keys to stats available for those/that tag(s)
#    
#    
#    
#    """
#     def _init_(self,tags,textDict):
#         self.tags = tags 
#         textStatsDict_Tags = retrieveDataForTags(tags,textDict)
#         self.textFileLocList =
#         self.linesList =
#         self.headFixFreq =
#         self.entryFreq =
#         self.headFixRates =
#         self.entryRates =
#         self.endMinusStartList =
#         self.startTimesList =
#         self.startDateList_pr =
#         
#
#
#   # textDictItems = zip(linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr)
#  #  textStatsDict = dict(zip(textFileLocList,textDictItems )) 
#
#    def getHeadFixRatesList:
#        return None
#    
#    def entryRatesList:
#        return None
#        
#    def endMinusStartListList:
#        return None                
#    
#    def startTimesListList:
#        return None    
#    
#    def startDateList_prList:
#        return None            
#
#    def headFixFreqList:
#        return None    
#            
#    def entryFreqList:
#        return None     
#           
#    def textFileLocListList:
#        return None     
#           
#    def getHeadFixRatesList:
#        return None      

#############

#[headFixRatesList,entryRatesList,endMinusStartListList,startTimesListList,startDateList_prList,headFixFreqList,entryFreqList,textFileLocListList]=retrieveDataForTags(tags,textDict)
###############
        

                                                            

# lines[0][0] = ['0000000000', '1434396227.79582', '2015-06-15 12:23:47.795820', 'SeshStart']
# lines[len(lines)-1][0] = ['0000000000', '1435789022.894986', '2015-07-01 15:17:02.894986', 'SeshStart']
# lines[52][0] = ['0000000000', '1437257248.318938', '2015-07-18 15:07:28.321582', 'SeshStart']




#
#genPlots(headFixRatesList,entryRatesList,startTimesListList,startDateList_prList)  
##genPlots(headFixFreqList,entryFreqList,startTimesListList,startDateList_prList)                                                                                                                                                                                                                
#                                                                                                                                                                                                                                                                                                                                          
## for each group find midpoint for each rate and stddev for error bars  
#
########## OVER HERE YOU ARE ONLY PICKING ONE GROUP -> ALTER FOR LATER
#
#
##miceGroups = {
##    'EL+EP':[2015050115,1312000377,1312000159,1302000245,1312000300,1302000139,2015050202,1412000238],
##    'EL':[2015050115,1312000377,1312000159,1302000245,1312000300],
##    'EP': [1302000139,2015050202,1412000238],
##    'AB': [1312000592,1312000573,1312000090]
##}

# Get col from dict
def getEffinCol(colNo,tag,textStatsDict_Tags):
    textStatsDict_Tags_Vals=[list(i) for i in textStatsDict_Tags[tag].values()]
    colList=[]
    for i in range(len(textStatsDict_Tags_Vals)):
        colList.append(textStatsDict_Tags_Vals[i][colNo])
    return colList

def getEffinCols(colNo,k,textStatsDict_Tags):
    colListofLists=[]
    for mouse in miceGroups[k]:
        colListofLists.append(getEffinCol(colNo,mouse,textStatsDict_Tags))
    return colListofLists
    

    
    
    
# Generate Plots
#def genPlots(headFixRatesList,entryRatesList,startTimesListList,startDateList_prList):
#    for i in range(len(headFixRatesList)):  
#        # TODO: FIX THAT THIS ONLY WORKS IF PLOTTING ALL TAGS
#        tag = tags[i]                       
#        #fig = plt.figure()
#        fig,ax = plt.subplots()
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
#        #Save each fig to outputLoc
#        plt.savefig(outputLoc+"Mouse "+str(tag)+".png", bbox_inches='tight')
#        
#    plt.show()


#######################################
# ALL THESE ASSUME X-AXIS IS date-time    
#######################################  
# Gen plots                             
def gen2PlotsForEachMouse(x1,y1,x2,y2,ylab,xlab,legend1,legend2,mouseGroup,title="Mouse ",outLoc=outputLoc):
    for i in range(len(x1)):  
        tag = miceGroups[mouseGroup][i]
        
        y1[i] = sort_X_BasedOn_Y_BeingSorted(y1[i],x1[i])
        y2[i] = sort_X_BasedOn_Y_BeingSorted(y2[i],x2[i])
        x1[i] = sort_X_BasedOn_Y_BeingSorted(x1[i],x1[i])
        x2[i] = sort_X_BasedOn_Y_BeingSorted(x2[i],x2[i])        
                                                                             
        #fig = plt.figure()
        fig,ax = plt.subplots()
        ax.plot(x1[i],y1[i],x2[i],y2[i])  
        green_line = mpatches.Patch(color='green',label=legend2)
        blue_line = mpatches.Patch(color='blue', label=legend1) 
        ax.legend(handles=[green_line,blue_line])  
        fig.autofmt_xdate()
        
        plt.title(title+str(tag))
        plt.ylabel(ylab)
        plt.xlabel(xlab)
        
        #Save each fig to outputLoc
        plt.savefig(outLoc+title+str(tag)+" "+ylab+".png", bbox_inches='tight')       
    plt.show()  
 
def genPlotsErrorBars(x,y,yerror,tit,ylab,xlab,outLoc=outputLoc):
    y = sort_X_BasedOn_Y_BeingSorted(y,x)
    x = sort_X_BasedOn_Y_BeingSorted(x,x)
    
    fig,ax = plt.subplots()
    plt.errorbar(x,y,yerr=yerror) 
    plt.title(tit)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    fig.autofmt_xdate()
    plt.savefig(outLoc+tit+" "+ylab+".png", bbox_inches='tight')   
    
def gen2PlotsErrorBars(x1,y1,x2,y2,yerror1,yerror2,legend1,legend2,tit,ylab,xlab,outLoc=outputLoc):
    
    y1 = sort_X_BasedOn_Y_BeingSorted(y1,x1)
    y2 = sort_X_BasedOn_Y_BeingSorted(y2,x2)
    x1 = sort_X_BasedOn_Y_BeingSorted(x1,x1)
    x2 = sort_X_BasedOn_Y_BeingSorted(x2,x2)
    
    #headfixRateAvgs = sort_X_BasedOn_Y_BeingSorted(headfixRateAvgs,startDatesGr) 
    #entryRateAvgs = sort_X_BasedOn_Y_BeingSorted(entryRateAvgs,startDatesGr) 
    #startDatesGr = sort_X_BasedOn_Y_BeingSorted(startDatesGr,startDatesGr)      
    fig,ax = plt.subplots()
    plt.errorbar(x1,y1,yerr=yerror1)
    plt.errorbar(x2,y2,yerr=yerror2)  
    green_line = mpatches.Patch(color='green', label=legend2)
    blue_line = mpatches.Patch(color='blue', label=legend1) 
    plt.legend(handles=[green_line,blue_line])  
    plt.title(tit)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    fig.autofmt_xdate()
    plt.savefig(outputLoc+tit+" "+ylab+".png", bbox_inches='tight')


def mainBIN_EL():
    yDist_hf=findFreqsForEach(FbinnedLines,'reward0',actionCol,miceGroups['EL'])
    yDist_entry=findFreqsForEach(FbinnedLines,'entry',actionCol,miceGroups['EL'])
    
    yerror_hf=map(pstdev,yDist_hf)
    y_hf = map(mean,yDist_hf)
    yerror_entry=map(pstdev,yDist_entry)
    y_entry = map(mean,yDist_entry)
    x = range(len(yDist_hf))
    assert(len(yDist_hf)==len(yDist_entry))
    
    ylab = 'Average Frequency'
    xlab = 'Day'
    
    gen2PlotsErrorBars(x,y_hf,x,y_entry,yerror_hf,yerror_entry,'Headfixing','Entries','EL Average Daily Frequency of Actions',ylab,xlab,outLoc=outputLoc)
    genPlotsErrorBars(x,y_hf,yerror_hf,'EL Average Daily Headfix Frequency',ylab,xlab,outLoc=outputLoc)
    genPlotsErrorBars(x,y_entry,yerror_entry,'EL Average Daily Entry Frequency',ylab,xlab,outLoc=outputLoc)

def mainBIN_ALL():
    yDist_hf=findFreqsForEach(FbinnedLines,'reward0',actionCol,tags)
    yDist_entry=findFreqsForEach(FbinnedLines,'entry',actionCol,tags)
    
    yerror_hf=map(pstdev,yDist_hf)
    y_hf = map(mean,yDist_hf)
    yerror_entry=map(pstdev,yDist_entry)
    y_entry = map(mean,yDist_entry)
    x = range(len(yDist_hf))
    assert(len(yDist_hf)==len(yDist_entry))
    
    ylab = 'Average Frequency'
    xlab = 'Day'
    
    gen2PlotsErrorBars(x,y_hf,x,y_entry,yerror_hf,yerror_entry,'Headfixing','Entries','Average Daily Frequency of Actions for All Mice over all data to August 13',ylab,xlab,outLoc=outputLoc)
    genPlotsErrorBars(x,y_hf,yerror_hf,'Average Daily Headfix Frequency for All Mice',ylab,xlab,outLoc=outputLoc)
    genPlotsErrorBars(x,y_entry,yerror_entry,'Average Daily Entry Frequency for All Mice',ylab,xlab,outLoc=outputLoc)   
    
def DONTDELETEYET():
    # Debugging:
    
    tagRowsBin = getRows_tag([FbinnedLines[0]],[tags[0]])
    #findFreq(tagRowsBin,'reward0',actionCol)[0]
    chosenCol = getCol_binnedLines(tagRowsBin,actionCol)
    #binnedLines_col.append(getCol(lines,actionCol))
    
    
    EL_binned=getRows_tag(FbinnedLines,miceGroups['EL'])
    
    #EL_binnedTags = getCol_binnedLines(EL_binned,tagCol)
    #EL_binnedTimes = getCol_binnedLines(EL_binned,timeCol)
    #EL_binnedDates = getCol_binnedLines(EL_binned,dateCol)
    #EL_binnedActions = getCol_binnedLines(EL_binned,actionCol)
    y = findFreq(EL_binned,'reward0',actionCol)
    
    y = findFreq(EL_binned,'entry',actionCol)



def main():
    for k in miceGroups.keys():
        #[headFixRatesList,entryRatesList,endMinusStartListList,startTimesListList,startDateList_prList,headFixFreqList,entryFreqList,textFileLocListList]    
        textStatsDict_Tags=retrieveDataForTags(miceGroups[k],textDict)
        
        linesList=getEffinCols(0,k,textStatsDict_Tags)
        
        headFixFreqList=getEffinCols(1,k,textStatsDict_Tags)
        entryFreqList=getEffinCols(2,k,textStatsDict_Tags)
        headFixRatesList=getEffinCols(3,k,textStatsDict_Tags)
        entryRatesList=getEffinCols(4,k,textStatsDict_Tags)
        endMinusStartListList=getEffinCols(5,k,textStatsDict_Tags)
        startTimesListList=getEffinCols(6,k,textStatsDict_Tags)
        startDateList_prList=getEffinCols(7,k,textStatsDict_Tags)
        
                
        # longest startDateList is the x-axis as it has no missing values
        startTimesGr=max(startTimesListList,key=len)
        startDatesGr= max(startDateList_prList,key=len)
        
        # Transpose to get for each mouse
        newHeadFixRates=np.transpose(np.array(headFixRatesList))
        newEntryRates=np.transpose(np.array(entryRatesList))
        newHeadFixFreqs=np.transpose(np.array(headFixFreqList))
        newEntryFreqs=np.transpose(np.array(entryFreqList))
        newHeadFixRates_rows=newHeadFixRates
        newEntryRates_rows=newEntryRates
        newHeadFixFreqs_rows=newHeadFixFreqs
        newEntryFreqs_rows=newEntryFreqs
        
        # compute means and yerr    
        #newHeadFixRates_rows=list(map(list,zip(*newHeadFixRates)))
        #newEntryRates_rows=list(map(list,zip(*newEntryRates)))
        headfixRateAvgs = map(mean,newHeadFixRates_rows)
        entryRateAvgs = map(mean,newEntryRates_rows)
        headfixRateErrs = map(pstdev,newHeadFixRates_rows)
        entryRatesErrs = map(pstdev,newEntryRates_rows)
        
        headfixFreqAvgs = map(mean,newHeadFixFreqs_rows)
        entryFreqAvgs = map(mean,newEntryFreqs_rows)
        headfixFreqErrs = map(pstdev,newHeadFixFreqs_rows)
        entryFreqsErrs = map(pstdev,newEntryFreqs_rows)
    
        # Sort... and find out later why this needs to be sorted 
        headfixRateAvgs = sort_X_BasedOn_Y_BeingSorted(headfixRateAvgs,startDatesGr) 
        entryRateAvgs = sort_X_BasedOn_Y_BeingSorted(entryRateAvgs,startDatesGr) 
        startDatesGr = sort_X_BasedOn_Y_BeingSorted(startDatesGr,startDatesGr)  
        
        headfixFreqAvgs = sort_X_BasedOn_Y_BeingSorted(headfixFreqAvgs,startDatesGr) 
        entryFreqAvgs = sort_X_BasedOn_Y_BeingSorted(entryFreqAvgs,startDatesGr) 
        
        #headFixRatesList = sort_X_BasedOn_Y_BeingSorted(headfixFreqAvgs,startDatesGr) 
        #entryRatesList = sort_X_BasedOn_Y_BeingSorted(entryFreqAvgs,startDatesGr) 
        
        
        # Titles
        tit1="Mouse Group "+ k + " Headfixes"
        tit2="Mouse Group "+ k + " Entries"
        tit3="Mouse Group "+ k
        
        # Get the textFiles        
        textFilesUnsorted = textStatsDict_Tags[textStatsDict_Tags.keys()[0]].keys()
        textFiles=sort_X_BasedOn_Y_BeingSorted(textFilesUnsorted,startTimesListList[0])
        
        # Save textfiles to downloads
        textFilestextName = outputLoc+tit3
        thefile = open((textFilestextName+'.txt'), 'w')

        for line in textFiles:
            thefile.write("%s\n" % line)
        
        genPlotsErrorBars(startDatesGr,headfixRateAvgs,headfixRateErrs,tit1,"Average Rate (per hour)","Date")
        genPlotsErrorBars(startDatesGr,entryRateAvgs,entryRatesErrs,tit2,"Average Rate (per hour)","Date")
        #
        genPlotsErrorBars(startDatesGr,headfixFreqAvgs,headfixFreqErrs,tit1,"Average Frequency","Date")
        genPlotsErrorBars(startDatesGr,entryFreqAvgs,entryFreqsErrs,tit2,"Average Frequency","Date")
        
        gen2PlotsErrorBars(startDatesGr,headfixRateAvgs,startDatesGr,entryRateAvgs,headfixRateErrs,entryRatesErrs,"Headfix","Entry",tit3,"Average Rate (per hour)","Date")
        gen2PlotsErrorBars(startDatesGr,headfixFreqAvgs,startDatesGr,entryFreqAvgs,headfixFreqErrs,entryFreqsErrs,"Headfix","Entry",tit3,"Average Frequency","Date")
                
        gen2PlotsForEachMouse(startDateList_prList,headFixRatesList,startDateList_prList,entryRatesList,"Average Rate (per hour)","Date","Headfix","Entry",k)
        gen2PlotsForEachMouse(startDateList_prList,headFixFreqList,startDateList_prList,entryFreqList,"Average Frequency","Date","Headfix","Entry",k)
        
        
        ############ BOKEH
        # prepare output to server
        output_server("MiceRateLine")
        
        p = figure(plot_width=400, plot_height=400)
        
        p.line(startDateList_prList[1],headFixRatesList[1],name='Headfix Rate')
        p.line(startDateList_prList[1],entryRatesList[1],name='Entry Rate')
        
        show(p)
        #############
    
            
#        gen2PlotsForEachMouse(startDateList_prList,headFixRatesList,startDateList_prList,entryRatesList,"Average Rate (per hour)","Date","Headfix","Entry")
#              
#        gen2PlotsForEachMouse(x1,y1,x2,y2,ylab,xlab,legend1,legend2,title="Mouse ",outLoc=outputLoc,)
#        
#        genPlotsForEachMouse(x,y,ylab,xlab,title="Mouse ",outLoc=outputLoc,)
#    
#        
#        
#        
#        
#
#        
#        genPlot(x,y,title,xlab,ylab,)
#        
#        fig,ax = plt.subplots()
#        plt.errorbar(startDatesGr,headfixRateAvgs,yerr=headfixRateErrs) 
#        plt.title(tit1)
#        plt.ylabel("Average Rate (per hour)")
#        plt.xlabel("Date")
#        fig.autofmt_xdate()
#        plt.savefig(outputLoc+tit1+".png", bbox_inches='tight')
#        
#        fig,ax = plt.subplots()
#        plt.errorbar(startDatesGr,entryRateAvgs,yerr=entryRatesErrs,color='g') 
#        plt.title(tit2)
#        plt.ylabel("Average Rate (per hour)")
#        plt.xlabel("Date") 
#        fig.autofmt_xdate()
#        plt.savefig(outputLoc+tit2+".png", bbox_inches='tight')
#    
#        fig,ax = plt.subplots()
#        plt.errorbar(startDatesGr,headfixRateAvgs,yerr=headfixRateErrs)
#        plt.errorbar(startDatesGr,entryRateAvgs,yerr=entryRatesErrs)  
#        green_line = mpatches.Patch(color='green', label='Entries')
#        blue_line = mpatches.Patch(color='blue', label='Headfixes') 
#        plt.legend(handles=[green_line,blue_line])  
#        plt.title(tit3)
#        plt.ylabel("Average Rate (per hour)")
#        plt.xlabel("Date")
#        fig.autofmt_xdate()
#        plt.savefig(outputLoc+tit3+".png", bbox_inches='tight')


    
        
            
                
                    
# Generate Plots
#def genPlots(headFixRatesList,entryRatesList,startTimesListList,startDateList_prList):
#    for i in range(len(headFixRatesList)):  
#        # TODO: FIX THAT THIS ONLY WORKS IF PLOTTING ALL TAGS
#        tag = tags[i]                       
#        #fig = plt.figure()
#        fig,ax = plt.subplots()
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
#        #Save each fig to outputLoc
#        plt.savefig(outputLoc+"Mouse "+str(tag)+".png", bbox_inches='tight')
#        
#    plt.show()                        
                            
                                
                                    
                                        
                                            
                                                
                                                    
                                                        
                                                            
                                                                
                                                                        
    # Example for stack overflow porblems
    
    #x=[1,2,3,4,5,6,7,8,9]
    #y=[[1,2,4,5,6,9],[1,1,1,1,1,1]]
    #
    #[for i in y[1] if y[0]]
    # Output should be: [1,1,0,1,1,1,0,0,1]
    
#    newHeadFixRates = []
#    newEntryRates = []
#    newTextFileLocs = []
#    # Create lists of appropriate length of zeros
#    for hfr in headFixRatesList:
#        newHeadFixRates.append([0]*(len(startTimesGr)))
#        newEntryRates.append([0]*(len(startTimesGr)))
#        newTextFileLocs.append(['']*(len(startTimesGr)))
#    
#    
#    # next fill in values in correct locations
#    for i in range(len(newHeadFixRates)):  
#        for rowNum in range(len(newHeadFixRates[i])): 
#            if startTimesGr[rowNum] in startTimesListList[i]:
#                prevRowno = np.where(startTimesListList[i]==startTimesGr[rowNum])[0]#[0]
#                newHeadFixRates[i][rowNum] = headFixRatesList[i][prevRowno]
#                newEntryRates[i][rowNum] = entryRatesList[i][prevRowno] 
#                #newTextFileLocs[i][rowNum] =  textFileLocListList[i][ prevRowno]        
#    
#                               
#                                                                    
#    # compute means and yerr    
#    newHeadFixRates_rows=list(map(list,zip(*newHeadFixRates)))
#    newEntryRates_rows=list(map(list,zip(*newEntryRates)))
#    headfixRateAvgs = map(mean,newHeadFixRates_rows)
#    entryRateAvgs = map(mean,newEntryRates_rows)
#    headfixRateErrs = map(pstdev,newHeadFixRates_rows)
#    entryRatesErrs = map(pstdev,newEntryRates_rows)
#        
#    # Titles
#    tit1="Mouse Group "+ k + " Headfixes"
#    tit2="Mouse Group "+ k + " Entries"
#    tit3="Mouse Group "+ k
#    
#    fig,ax = plt.subplots()
#    plt.errorbar(startDatesGr,headfixRateAvgs,yerr=headfixRateErrs) 
#    plt.title(tit1)
#    plt.ylabel("Average Rate (per hour)")
#    plt.xlabel("Date")
#    fig.autofmt_xdate()
#    plt.savefig(outputLoc+tit1+".png", bbox_inches='tight')
#    fig,ax = plt.subplots()
#    plt.errorbar(startDatesGr,entryRateAvgs,yerr=entryRatesErrs,color='g') 
#    plt.title(tit2)
#    plt.ylabel("Average Rate (per hour)")
#    plt.xlabel("Date") 
#    fig.autofmt_xdate()
#    plt.savefig(outputLoc+tit2+".png", bbox_inches='tight')
#
#    fig,ax = plt.subplots()
#    plt.errorbar(startDatesGr,headfixRateAvgs,yerr=headfixRateErrs)
#    plt.errorbar(startDatesGr,entryRateAvgs,yerr=entryRatesErrs)  
#    green_line = mpatches.Patch(color='green', label='Entries')
#    blue_line = mpatches.Patch(color='blue', label='Headfixes') 
#    plt.legend(handles=[green_line,blue_line])  
#    plt.title(tit3)
#    plt.ylabel("Average Rate (per hour)")
#    plt.xlabel("Date")
#    fig.autofmt_xdate()
#    plt.savefig(outputLoc+tit3+".png", bbox_inches='tight')

                                                                                                                                                                    
                                                                                                                                                                                                
 
#def dupes(textDirs):
#    """
#    returns [(leDupe1,leDupe2)]
#        leDupe1: text file that has the same content as corresponding text file leDupe2
#    """ 
#    leDupe1 = []
#    leDupe2 = [] 
#    for textDir1 in textDirs:
#        for textDir2 in textDirs:
#            if filecmp.cmp(textDir1, textDir2, shallow=False):   
#                leDupe1.append(textDir1)
#                leDupe2.append(textDir2)
#    return(zip(leDupe1,leDupe2))                                                                                                              
#                                                                                                                                    
#def equalStarts(textDirs):
#    """
#    returns [(leDupe1,leDupe2)]
#        leDupe1: text file that has the same startSesh as corresponding text file leDupe2
#    """ 
#    leDupe1 = []
#    leDupe2 = [] 
#    for textDir1 in textDirs:
#        for textDir2 in textDirs:      
#            with open(textDir1) as f:
#                reader = csv.reader(f, delimiter="\t")
#                txtLines1 = list(reader)
#                
#            with open(textDir2) as f:
#                reader = csv.reader(f, delimiter="\t")
#                txtLines2 = list(reader)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
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