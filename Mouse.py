"""Class holding all attributes related to a single mouse"""

import numpy as np
from datetime import datetime
import re

class Mouse:  
    def __init__(self,miceGroups,tag):   
        self.tag = tag
        self.miceGroups = miceGroups
            
    def findGroup(self,tag):
        """Return the group a tag belongs to"""  
        for key in self.miceGroups.keys():
            if tag in self.miceGroups[key]:
                return key                   

    def badAssFunk(self,tag,textDict):
        """
        (I was happy with this function after I built it in a few hours as the following old docs clearly show)
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
        """
                    
        textFileLoc = textDict.keys()
        lines = textDict.items()
        
        headFixRates = []
        entryRates = []
        endMinusStartList = []
        startTimesList = []
        startDateList_pr = []   
        headFixFreq = []
        entryFreq = []
        textFileLocList = []
        linesList = []
        # Not returned
        startDateList = []
                
        for singleTextLoc in textFileLoc: 
            # Retrieve column of tags
            singleTextLines = textDict[singleTextLoc]
            
            columnOfTags=np.asarray(singleTextLines)[:,self.tagCol]
            columnOfTags = [ int(x) for x in columnOfTags ]
            
            signal = False
            otherTagsinGroup=self.miceGroups[self.findGroup(tag)]
            for otherTag in otherTagsinGroup:
                if otherTag in columnOfTags:
                    signal = True
            
            if tag not in columnOfTags and signal:
                headFixFreq.append(0)
                entryFreq.append(0)
                
                textFileLocList.append(singleTextLoc)
                linesList.append(singleTextLines)
                # Find end - start
                startTime = singleTextLines[0][self.timeCol]
                startTimesList.append(startTime[:])
                endTime = singleTextLines[-1][self.timeCol]
                
                # Add the startDate
                startDateList.append(singleTextLines[0][self.dateCol]) 
                
                # Convert to hours
                endMinusStart = float(endTime)/3600 - float(startTime)/3600
                endMinusStartList.append(endMinusStart)
                assert(len(textFileLocList)==len(linesList)==len(endMinusStartList)==len(startTimesList)==len(headFixFreq)==len(entryFreq)==len(startTimesList)) 
            
        
            if tag in columnOfTags: 
                textFileLocList.append(singleTextLoc)
                linesList.append(singleTextLines)
                    
                # Find end - start
                startTime = singleTextLines[0][self.timeCol]
                startTimesList.append(startTime[:])
                endTime = singleTextLines[-1][self.timeCol]
                # Convert to hours
                endMinusStart = float(endTime)/3600 - float(startTime)/3600
                endMinusStartList.append(endMinusStart)
                
                # Get all the lines in the current text file associated with the current tag
                chosenLinesThisFile=np.asarray(singleTextLines)[np.transpose(columnOfTags)==tag] 
                
                times=chosenLinesThisFile[:,self.timeCol].astype(np.float)
                actions=chosenLinesThisFile[:,self.actionCol] 
                # Replace "reward0" with "headfix"
                for j in xrange(0,np.size(actions)):
                    actions[j] = re.sub('reward0', 'headfix', actions[j])
                #Collapse rewards into a single variable  
                for j in xrange(0,np.size(actions)):
                    actions[j] = re.sub('reward.', 'reward', actions[j]) 
                #Remove all actions other than headfix and entry      
                times=times[np.logical_or(actions=='entry',actions=='headfix')]
                actions=actions[np.logical_or(actions=='entry',actions=='headfix')]    
                assert(times.size ==  actions.size),("There are either more times than actions or more actions than times for mouse: "+str(tag))
                
                # Retrieve counts of each tracked variable
                headFixFreq.append(actions.tolist().count('headfix')) 
                entryFreq.append(actions.tolist().count('entry')) 
                # Add the startDate
                startDateList.append(singleTextLines[0][self.dateCol])           
                if len(actions.tolist())==0:
                    headFixFreq.append(0)
                    entryFreq.append(0) 
        
            
        for i in range(len(endMinusStartList)):
            headFixRate = headFixFreq[i]/endMinusStartList[i]
            headFixRates.append(headFixRate)
            entryRate = entryFreq[i] /endMinusStartList[i]
            entryRates.append(entryRate)
            
        # Sort it (assumed sorted
    #    headFixRates = np.array(headFixFreq)
    #    entryRates = np.array(entryFreq)    
    #    startTimesList = np.array(startTimesList) 
    #    startDateList = np.array(startDateList)
    #    textFileLocList = np.array(textFileLocList)  
    #    
    #    inds = startTimesList.argsort()
    #
    #    headFixRates = headFixRates[inds] 
    #    entryRates = entryRates[inds]
    #    startDateList = startDateList[inds]
    #    textFileLocList = textFileLocList[inds]    
    
    
        startDateList_pr = startDateList[:]
        # Convert dates to date objects
        for i in range(len(startDateList_pr)):
            startDateList_pr[i]=(datetime.strptime(startDateList[i], '%Y-%m-%d %H:%M:%S.%f'))  
            
        # Each textFile must have 2 rates, 2 freqs, 2 dates, end-start  
        assert(len(textFileLocList)==len(linesList)==len(headFixRates)==len(entryRates)==len(endMinusStartList)==len(startTimesList)==len(startDateList_pr)==len(headFixFreq)==len(entryFreq)==len(startDateList)) 
        
        #[linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr]
        
        textKeys = ['lines','headFixFreq','entryFreq','headFixRates','entryRates','endMinusStart','startTimes','startDateList_pr']
        textDictItems = zip(linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr)
        textStatsDict = dict(zip(textFileLocList,textDictItems ))
        
        # Todo: Give the items a name
        #statsDict =    
        #textStatsDict = dict(zip(textFileLocList,textDictItems ))    
        return(textStatsDict)  
