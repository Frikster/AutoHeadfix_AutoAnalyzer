"""Class holding all attributes related to a single mouse"""
# Change working directory to where this module is before doing anything else
import os, sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import cfg
from PreprocessTextfiles import PreprocessTextfiles

import numpy as np
from datetime import datetime
from time import mktime
import re

class Mouse:  
    # Column numbers
    TAG_COL = 0
    TIME_COL = 1
    DATE_COL = 2
    ACTION_COL = 3 
    
    def __init__(self, tag, mice_groups, current_dat, bin_time):
        self.tag = int(tag)
        self.mice_groups = mice_groups
        self.group = self.findgroup(tag)
        
        #self.all_lines = current_dat.all_lines
        self.all_lines = [L for L in current_dat.all_lines if int(L[self.TAG_COL])==int(self.tag)]
        # replace check1+ with check+
        for line in self.all_lines:
            if line[self.ACTION_COL] == 'check1+':
                line[self.ACTION_COL] = 'check+'
        
        self.binned_lines = self.set_bins(bin_time)
        
    def eAnd(self,*args):
        """Returns a list that is the element-wise 'and' operation along each index of each list in args"""
        return [all(tuple) for tuple in zip(*args)] 
        
    def set_bins(self,bin_time):
        """    
        Bin list of all sorted lines_list into per binTime lists
        For your convenience: there are 86400 seconds in a day
        Returns: BinnedList: np.array([[a],[b]...]) where the first line in a,b... is binTime seconds before the last
        """  
        all_lines = self.all_lines
        column_of_times = self.get_col(all_lines,self.TIME_COL)
        column_of_times = [ float(x) for x in column_of_times]
        column_of_times = np.array(column_of_times)
        all_lines = np.array(all_lines)
        
        binned_lines = []
        start_ind = column_of_times[0]
        end_ind = start_ind + bin_time
        
        while end_ind <= column_of_times[len(column_of_times)-1]:
            the_bin = all_lines[np.array(self.eAnd(column_of_times>=start_ind,column_of_times<end_ind))]
            binned_lines.append(the_bin)
            start_ind = end_ind
            end_ind = end_ind + bin_time
            print('Mouse '+ str(self.tag) +' bin created from ' + str(start_ind) + ' to ' + str(end_ind))
          
        return binned_lines   
        
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
        
        relevantlines=[L for L in lines if L[self.ACTION_COL]==actionA or L[self.ACTION_COL]==actionB]
        
        if len(relevantlines) >0:                
            # If the first line is actionB, add the time from the beginning of lines
            if relevantlines[0][self.ACTION_COL] == actionB:
                total = total + (float(relevantlines[0][self.TIME_COL])-float(lines[0][self.TIME_COL]))
                relevantlines.pop(0)
    
            # If the last line is actionA, add the time from that point to the end
            if  relevantlines[len(relevantlines)-1][self.ACTION_COL] == actionA:
                total = total + (float(lines[len(lines)-1][self.TIME_COL])-float(relevantlines[len(relevantlines)-1][self.TIME_COL]))
                relevantlines.pop(-1)
            
            # if there is anything left continue trying to find the remaining times between
            # We are assuming ActionA and ActionB always alternate in occurence so at this point on zero or more than
            # one action can remain
            if len(relevantlines) >1:   
                # Get all the relevantlines that have each action
                relevantlines_actionA = [line for line in relevantlines if line[self.ACTION_COL]==actionA]
                relevantlines_actionB = [line for line in relevantlines if line[self.ACTION_COL]==actionB]
                
                if len(relevantlines_actionA)==0 or len(relevantlines_actionA)==0:
                    print(relevantlines_actionA)
                    print(relevantlines_actionB) 

                # Get the two columns of times
                actionA_times = self.get_col(relevantlines_actionA,self.TIME_COL)
                actionB_times = self.get_col(relevantlines_actionB,self.TIME_COL)
            
                timesbetween = [float(b)-float(a) for a,b in zip(actionA_times,actionB_times)]
                total = sum(timesbetween) + total
        return total
            

    def time_between_actions_list(self,actionA,actionB):
        """Returns the time spent between actionA and B by this mouse for each bin""" 
        bin_chamber_time = []
        for lines in self.binned_lines:
            bin_chamber_time.append(self.time_between(actionA,actionB,lines)) 
        return bin_chamber_time  
    

    def get_between_actions_dist(self,actionA,actionB):
        """Returns a list that contains each time interval between actionA and actionB for this mouse"""
        relevantlines=[L for L in self.all_lines if L[self.ACTION_COL]==actionA or L[self.ACTION_COL]==actionB]
        
        #Drop the first and last line since the first one will typically be check+ and the last one reward0
        if(relevantlines[0][self.ACTION_COL]==actionB):
            print(relevantlines[0])
            relevantlines.pop(0)
        if(relevantlines[len(relevantlines)-1][self.ACTION_COL]==actionA):
            print(relevantlines[-1])
            relevantlines.pop(-1)
        
        print(relevantlines[0])
        print(relevantlines[-1])
        assert(relevantlines[0][cfg.ACTION_COL] == actionA)
        assert(relevantlines[len(relevantlines)-1][cfg.ACTION_COL] == actionB)
                  
        # Get all the relevantlines that have each action
        relevantlines_actionA = [line for line in relevantlines if line[self.ACTION_COL]==actionA]
        relevantlines_actionB = [line for line in relevantlines if line[self.ACTION_COL]==actionB]
        
        assert(len(relevantlines_actionA)==len(relevantlines_actionA))

        # Get the two columns of times
        actionA_times = self.get_col(relevantlines_actionA, self.TIME_COL)
        actionB_times = self.get_col(relevantlines_actionB, self.TIME_COL)
    
        timesbetween = [float(b)-float(a) for a,b in zip(actionA_times,actionB_times)]

        # Obtain additional info on each interval (start time, end time, textfile loc)
        # Get all the relevantlines that have each action
        relevantlines_start_dates = [line[cfg.DATE_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionA]
        relevantlines_end_dates = [line[cfg.DATE_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionB]
        relevantlines_start_times = [line[cfg.TIME_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionA]
        relevantlines_end_times = [line[cfg.TIME_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionB]
        #Todo: add the source
        #relevantlines_start_textfiles = [line[cfg.TEXT_LOC_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionA]
        #relevantlines_end_textfiles = [line[cfg.TEXT_LOC_COL] for line in relevantlines if line[cfg.ACTION_COL] == actionB]

        assert(len(relevantlines_start_dates) == len(relevantlines_end_dates) ==
               len(relevantlines_start_times) == len(relevantlines_end_times))

               #len(relevantlines_start_textfiles) == len(relevantlines_end_textfiles) == len(relevantlines_actionA))

        return [timesbetween, relevantlines_start_dates, relevantlines_end_dates,
                relevantlines_start_times, relevantlines_end_times]
                #relevantlines_start_textfiles, relevantlines_end_textfiles]
        
    @staticmethod
    def convert_to_date_obj(date_list):
        """Convert dates to date objects """
        # TODO: See if this is needed
        # date_list_pr = [mktime(datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f').timetuple()) for i in date_list]
        date_list_pr = date_list[:]
        for i in range(len(date_list)):
            try:
                # TODO: Why are you converting these fuckers to seconds and not following the function comment?
                #date_list_pr[i] = mktime(datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S.%f').timetuple())
                date_list_pr[i] = (datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S.%f'))
            except Exception:
                try:
                    #date_list_pr[i] = mktime(datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S').timetuple())
                    date_list_pr[i] = (datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S'))
                except Exception:
                    print(date_list[i])
        return date_list_pr


        
        




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
