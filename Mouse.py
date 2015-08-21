"""Class holding all attributes related to a single mouse"""
from PreprocessTextfiles import PreprocessTextfiles
import numpy as np
from datetime import datetime
import re

class Mouse:  
    # Column numbers
    TAG_COL = 0
    TIME_COL = 1
    DATE_COL = 2
    ACTION_COL = 3 
    
    def __init__(tag,mice_groups,current_dat):   
        self.tag = int(tag)
        self.mice_groups = mice_groups
        self.group = self.findgroup(tag)
        
        self.all_lines = current_dat.all_lines
        self.all_lines = [L for L in self.all_lines if int(self.all_lines[self.TAG_COL])==self.tag]
        
        
    def get_col(self,list_of_lists,col_num):
        """return desired column from list of lists as a list"""
        return list(np.asarray(list_of_lists)[:,col_num])
            
    def findgroup(self,tag):
        """Return the group a tag belongs to"""  
        for key in self.mice_groups.keys():
            if tag in self.mice_groups[key]:
                return key                   
    
    def time_between(self,actionA,actionB,lines):
        """Returns the total time between actionA and actionB in lines"""
        total = 0
        #cond1 = line[self.ACTION_COL]==actionA and line[self.TAG_COL]==self.tag
        #cond2 = line[self.ACTION_COL]==actionB and line[self.TAG_COL]==self.tag
        
        relevantlines=[L for L in lines if L[self.ACTION_COL]==actionA or L[self.ACTION_COL]==actionB]
                
        # If the first line is actionB, add the time from the beginning of lines
        if relevantlines[0][self.ACTION_COL] == actionB:
            total = total + (float(relevantlines[0][self.TIME_COL])-float(lines[0][self.TIME_COL]))
            relevantlines.pop(0)

        # If the last line is actionA, add the time from that point to the end
        if  relevantlines[len(relevantlines)-1][self.ACTION_COL] == actionA:
            total = total + (float(lines[len(lines)-1][self.TIME_COL])-float(relevantlines[len(relevantlines)-1][self.TIME_COL]))
            relevantlines.pop(-1)
        
        # Get all the relevantlines that have each action
        relevantlines_actionA = [line for line in relevantlines if line[self.ACTION_COL]==actionA]
        relevantlines_actionB = [line for line in relevantlines if line[self.ACTION_COL]==actionB]
        
        timesbetween = [b-a for a,b in zip(relevantlines_actionA,relevantlines_actionB)]
        return sum(timesbetween)+total
            

    def time_between_actions_list(self,actionA,actionB,binned_lines):
        """Returns the time spent between actionA and B by this mouse for each bin""" 
        bin_chamber_time = []
        for lines in binned_lines:
            bin_chamber_time.append(self.time_between(actionA,actionB,lines)) 
        return bin_chamber_time  
    




    #def time_between_rewards(binned_lines):
    #    """Returns the time between headfixes for this mouse for each bin""" 
    #    return None










## Todo: Make this function useful again (and less ugly)
#    def badAssFunk(self,tag,textDict):
#        """
#        (I was happy with this function after I built it in a few hours as the following old docs clearly show)
#        # Dis funktion does it all yo
#        # Input: Just give me the tag of the mouse dawg, I'll get the dirt on her
#        # Returns: [headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr,headFixFreq,entryFreq]
#        # headFixRates = list of number of headfixes per hour
#        # entryRates = list of entries of headfixes per hour
#        # endMinusStartList = list of durations for each session
#        # startTimesList = list of starting times for each session examined
#        # startDateList_pr = list of starting dates for each session examined
#        # headFixFreq = list of numer of headfixes
#        # entryFreq = list of numer of entries
#        """
#                    
#        textFileLoc = textDict.keys()
#        lines = textDict.items()
#        
#        headFixRates = []
#        entryRates = []
#        endMinusStartList = []
#        startTimesList = []
#        startDateList_pr = []   
#        headFixFreq = []
#        entryFreq = []
#        textFileLocList = []
#        linesList = []
#        # Not returned
#        startDateList = []
#                
#        for singleTextLoc in textFileLoc: 
#            # Retrieve column of tags
#            singleTextLines = textDict[singleTextLoc]
#            
#            columnOfTags=np.asarray(singleTextLines)[:,self.tagCol]
#            columnOfTags = [ int(x) for x in columnOfTags ]
#            
#            signal = False
#            otherTagsinGroup=self.miceGroups[self.findGroup(tag)]
#            for otherTag in otherTagsinGroup:
#                if otherTag in columnOfTags:
#                    signal = True
#            
#            if tag not in columnOfTags and signal:
#                headFixFreq.append(0)
#                entryFreq.append(0)
#                
#                textFileLocList.append(singleTextLoc)
#                linesList.append(singleTextLines)
#                # Find end - start
#                startTime = singleTextLines[0][self.timeCol]
#                startTimesList.append(startTime[:])
#                endTime = singleTextLines[-1][self.timeCol]
#                
#                # Add the startDate
#                startDateList.append(singleTextLines[0][self.dateCol]) 
#                
#                # Convert to hours
#                endMinusStart = float(endTime)/3600 - float(startTime)/3600
#                endMinusStartList.append(endMinusStart)
#                assert(len(textFileLocList)==len(linesList)==len(endMinusStartList)==len(startTimesList)==len(headFixFreq)==len(entryFreq)==len(startTimesList)) 
#            
#        
#            if tag in columnOfTags: 
#                textFileLocList.append(singleTextLoc)
#                linesList.append(singleTextLines)
#                    
#                # Find end - start
#                startTime = singleTextLines[0][self.timeCol]
#                startTimesList.append(startTime[:])
#                endTime = singleTextLines[-1][self.timeCol]
#                # Convert to hours
#                endMinusStart = float(endTime)/3600 - float(startTime)/3600
#                endMinusStartList.append(endMinusStart)
#                
#                # Get all the lines in the current text file associated with the current tag
#                chosenLinesThisFile=np.asarray(singleTextLines)[np.transpose(columnOfTags)==tag] 
#                
#                times=chosenLinesThisFile[:,self.timeCol].astype(np.float)
#                actions=chosenLinesThisFile[:,self.actionCol] 
#                # Replace "reward0" with "headfix"
#                for j in xrange(0,np.size(actions)):
#                    actions[j] = re.sub('reward0', 'headfix', actions[j])
#                #Collapse rewards into a single variable  
#                for j in xrange(0,np.size(actions)):
#                    actions[j] = re.sub('reward.', 'reward', actions[j]) 
#                #Remove all actions other than headfix and entry      
#                times=times[np.logical_or(actions=='entry',actions=='headfix')]
#                actions=actions[np.logical_or(actions=='entry',actions=='headfix')]    
#                assert(times.size ==  actions.size),("There are either more times than actions or more actions than times for mouse: "+str(tag))
#                
#                # Retrieve counts of each tracked variable
#                headFixFreq.append(actions.tolist().count('headfix')) 
#                entryFreq.append(actions.tolist().count('entry')) 
#                # Add the startDate
#                startDateList.append(singleTextLines[0][self.dateCol])           
#                if len(actions.tolist())==0:
#                    headFixFreq.append(0)
#                    entryFreq.append(0) 
#        
#            
#        for i in range(len(endMinusStartList)):
#            headFixRate = headFixFreq[i]/endMinusStartList[i]
#            headFixRates.append(headFixRate)
#            entryRate = entryFreq[i] /endMinusStartList[i]
#            entryRates.append(entryRate)
#            
#        # Sort it (assumed sorted
#    #    headFixRates = np.array(headFixFreq)
#    #    entryRates = np.array(entryFreq)    
#    #    startTimesList = np.array(startTimesList) 
#    #    startDateList = np.array(startDateList)
#    #    textFileLocList = np.array(textFileLocList)  
#    #    
#    #    inds = startTimesList.argsort()
#    #
#    #    headFixRates = headFixRates[inds] 
#    #    entryRates = entryRates[inds]
#    #    startDateList = startDateList[inds]
#    #    textFileLocList = textFileLocList[inds]    
#    
#    
#        startDateList_pr = startDateList[:]
#        # Convert dates to date objects
#        for i in range(len(startDateList_pr)):
#            startDateList_pr[i]=(datetime.strptime(startDateList[i], '%Y-%m-%d %H:%M:%S.%f'))  
#            
#        # Each textFile must have 2 rates, 2 freqs, 2 dates, end-start  
#        assert(len(textFileLocList)==len(linesList)==len(headFixRates)==len(entryRates)==len(endMinusStartList)==len(startTimesList)==len(startDateList_pr)==len(headFixFreq)==len(entryFreq)==len(startDateList)) 
#        
#        #[linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr]
#        
#        textKeys = ['lines','headFixFreq','entryFreq','headFixRates','entryRates','endMinusStart','startTimes','startDateList_pr']
#        textDictItems = zip(linesList,headFixFreq,entryFreq,headFixRates,entryRates,endMinusStartList,startTimesList,startDateList_pr)
#        textStatsDict = dict(zip(textFileLocList,textDictItems ))
#        
#        # Todo: Give the items a name
#        #statsDict =    
#        #textStatsDict = dict(zip(textFileLocList,textDictItems ))    
#        return(textStatsDict)  
