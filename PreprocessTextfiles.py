"""Class holding all attributes related to preprocessing textFiles"""

import os
import csv
import numpy as np
import collections
from datetime import datetime
import itertools
import csv

class PreprocessTextfiles:     
    # Column numbers
    TAG_COL = 0
    TIME_COL = 1
    DATE_COL = 2
    ACTION_COL = 3   
    
    # string constants that define textFile
    seshStart_str = 'SeshStart'
    seshEnd_str = 'SeshEnd'   
    seshStartTag_str = '0000000000'
    seshEndTag_str = '0000000000'  
    
    def __init__(self, working_dir, folders_to_ignore,output_dir=''):
        self.working_dir = working_dir
        self.folders_to_ignore = folders_to_ignore 
        
        self.binned_lines = None
        self.texts_not_imported = None
        
        self.txt_list = self.get_all_text_locs(working_dir)
        self.all_lines = self.get_all_lines_no_dupes(self.txt_list)
        
        zipped = self.import_texts_to_list_of_mat(self.txt_list)
        self.texts_imported = zip(*zipped)[1]
        
        # Sort the lines
        times = self.get_col(self.all_lines,self.TIME_COL)
        self.all_lines = self.sort_X_BasedOn_Y_BeingSorted(self.all_lines,times) 
          
        # if an output_dir was specified, output a csv to it
        if output_dir != '':
            self.output_all_lines_to_csv(output_dir)
        else:
            self.output_all_lines_to_csv('Result.csv')
            
        #self.textDict =self.importTextsToDict(self.txtList)
        
        #self.lines_sorted = []
        #for i in range(len(self.textDict.items())):
        #    self.linesSorted.extend(self.textDict.items()[i][1]) 
   
    def output_all_lines_to_csv(self,output_dir):
        """ouput all lines imported to a single csv"""
        with open(output_dir+"all_lines.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(self.all_lines)
            
    def sort_X_BasedOn_Y_BeingSorted(self,X,Y):
        """Sorts X based on the result from Y being sorted"""
        X = np.array(X)
        Y = np.array(Y)
        inds = Y.argsort()
        return(X[inds]) 
        
    def get_col(self,list_of_lists,col_num):
        """return desired column from list of lists as a list"""
        return list(np.asarray(list_of_lists)[:,col_num])    
       
    def get_all_text_locs(self,working_dir):
        """Get a list of all text files in the given folder (including subdirectories)"""
        txt_list = []
        for root, dirs, files in os.walk(working_dir):
            for file in files:
                if file.endswith(".txt"):
                    print(os.path.join(root, file))
                    txt_list.append(os.path.join(root, file))
                    
         # Remove all the paths that are subdirectories of the ignore folders
        for i in range(len(self.folders_to_ignore)):
            txt_list=[x for x in txt_list if not (self.folders_to_ignore[i] in x)]
        
        return txt_list
    
    def import_texts_to_list_of_mat(self,txtList):
        """Import viable text_files to a list of matrices
            Returns:
            [(lines_list,text_file_loc)] (tuple)
            lines: The lines of the textfile as a 2D list
            text_file_loc: The path of each textFile that was imported.      
        """    
        lines_list = []  
        text_file_loc=[]
        texts_not_imported=[]
        # Append them all into one matrix (the ones with the appropriate number of columns)
        for i in range(len(txtList)):
            text_file = txtList[i]
            try:
                with open(text_file) as f:
                    reader = csv.reader(f, delimiter="\t")
                    new_lines = list(reader)
                print(str(len(new_lines))+" - "+text_file)
                # Only consider textFile with more than 2 rows and that have 'SeshStart' in first line                                                                                               
                if len(new_lines) > 2 and new_lines[0][self.ACTION_COL]==self.seshStart_str:
                    # Add a row for textFiles missing a SeshEnd          
                    if new_lines[-1][self.ACTION_COL] != self.seshEnd_str: 
                        new_lines.append(new_lines[-1][:])
                        new_lines[-1][self.ACTION_COL] = self.seshEnd_str
                        new_lines[-1][self.TAG_COL] = self.seshEndTag_str
                    lines_list.append(new_lines)
                    text_file_loc.append(txtList[i])
                else:
                    print("Text file does not have enough rows - "+text_file)
                    texts_not_imported.append(text_file)
            except BaseException:
                print("Text file does not have enough columns - "+text_file)
                texts_not_imported.append(text_file)
        self.texts_not_imported = texts_not_imported
        return(zip(lines_list,text_file_loc))
        
    def get_all_lines_no_dupes(self,txt_list):
        """Returns a list of lists that contains all lines from all text files in txt_list with duplicates removed"""
        list_of_Mat = self.import_texts_to_list_of_mat(txt_list)
        lines_list = zip(*list_of_Mat)[0]
        lines_list = list(itertools.chain.from_iterable(lines_list))
        lines_list = [list(x) for x in set(tuple(x) for x in lines_list)] 
        return lines_list
        
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
            print('bin created from ' + str(start_ind) + ' to ' + str(end_ind))
          
        self.binned_lines = binned_lines
        
    def get_col_binned_lines(self,col_num):        
        """return list of lists that would be the binned lists of a particular column"""
        if self.binned_lines == None:
            assert(1==0,'binned_lines have not been set')
        binned_lines_col = []
        for lines_list in self.binned_lines:
            if len(lines_list) > 0:
                binned_lines_col.append(self.get_col(lines_list,col_num))
        return binned_lines_col
              
    def get_binned_rows_tag(self,chosen_tags):
        """return list of lists that are all binned lines that are by a mouse in tags """
        if self.binned_lines == None:
            assert(1==0,'binned_lines have not been set')
        binned_lines_tags = []
        
        for lines_list in self.binned_lines:
            the_bin = []
            for line in lines_list:
                if int(line[self.TAG_COL]) in chosen_tags:
                    the_bin.append(line)
            binned_lines_tags.append(the_bin)
        return binned_lines_tags
        
    def get_freq_list_binned(self,item,col_num):
        """return list of list that is the count of the occurence of 'item' in each list (in column col_num) in binned_lines"""
        if self.binned_lines == None:
            assert(1==0,'binned_lines have not been set')
        freqs = []
        
        chosen_col = self.get_col_binned_lines(self.binned_lines,col_num)
        for its in chosen_col:
            freqs.append(its.count(item)) 
        return freqs
 
    def find_freqs_for_each(self,item,col_num,chosen_tags):
        """return list of list that is the counts for each mouse for each bin for item in col_num"""
        if self.binned_lines == None:
            assert(1==0,'binned_lines have not been set')
        freqs_for_each = []
        for lines_list in self.binned_lines:
            freqs_for_bin = []
            for tag in chosen_tags:
                tag_rows_bin = self.get_binned_rows_tag([lines_list],[tag])
                if len( tag_rows_bin[0]) == 0:
                    freqs_for_bin.append(0)
                else: 
                    freqs_for_bin.append(self.get_freq_list_binned(tag_rows_bin,item,col_num)[0])
            freqs_for_each.append(freqs_for_bin)
        return freqs_for_each
 
#workingDir = "T:/AutoHeadFix/"
#foldersToIgnore = ["Old and or nasty data goes here"]   
#output_dir = "C:/Users/user/Documents/Dirk/Bokeh/AutoHeadfix_AutoAnalyzer/Ignored/" 
#test = PreprocessTextfiles(workingDir,foldersToIgnore,output_dir)
        
        
        

    
#    def setDuplicates(self,lines_list,textFileLoc):
#        """Return a tuple of text file locations and their startSeshes that have been identified as duplicates,
#        ordered by StartSesh"""
#        # Remove the text files that have the same start time as another     
#        startSeshes = []
#        for i in range(len(lines_list)):
#            startSeshes.append(lines_list[i][0][self.timeCol])
#        
#        def equalToAnother(elem):
#            return (startSeshes.count(elem) > 1)
#            
#        def NOTequalToAnother(elem):
#            return (startSeshes.count(elem) == 1)  
#        
#        # Indices of all text files that are duplicates of another and those that are unique
#        equalStartInd=map(equalToAnother,startSeshes)
#        notEqualStartInd = map(NOTequalToAnother, startSeshes)
#        
#        # Retrieve text file names and start times that have duplicates
#        textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
#        startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
#        
#        # Sort these text files by start time  
#        textFileEquals = self.sort_X_BasedOn_Y_BeingSorted(textFileEquals,startTimeEquals)
#        startTimeEquals = self.sort_X_BasedOn_Y_BeingSorted(startTimeEquals,startTimeEquals)
#        
#        self.duplicates = zip(textFileEquals,startTimeEquals)
#        
#    def setDuplicatesThatWereKept(self):
#        if self.duplicates == None:
#            assert(1==0,'No duplicates have been set')
#        textFileEquals = zip(*self.duplicates)[0]
#        startTimeEquals = zip(*self.duplicates)[1]
#        
#        textFileEqualsOnlyOne = [] # you are the only one baby!
#        startTimeEqualsOnlyOne = []
#        # Create a list that only contains one (any one) of the textFiles that have a duplicate
#        for i in range(len(startTimeEquals)):
#            if i != range(len(startTimeEquals))[-1]:
#                if startTimeEquals[i] != startTimeEquals[i+1]:
#                    startTimeEqualsOnlyOne.append(startTimeEquals[i])
#                    textFileEqualsOnlyOne.append(textFileEquals[i])
#            else:
#                    startTimeEqualsOnlyOne.append(startTimeEquals[i])
#                    textFileEqualsOnlyOne.append(textFileEquals[i])
#                    
#        self.duplicatesKept = zip(textFileEqualsOnlyOne,startTimeEqualsOnlyOne)
#    
#    
#    def importTextsToDict(self,txtList):
#        """
#        Return a dictionary that has each path of each text file as the key to a matrix that contains all the lines_list of each text file 
#        - duplicates removed, ordered by textFile startseshes
#        """
#        workingDir = self.workingDir
#        txtList = self.getAllTextLocs(workingDir)
#        # Remove all the paths that are subdirectories of the ignore folders
#        for i in range(len(self.foldersToIgnore)):
#            txtList=[x for x in txtList if not (self.foldersToIgnore[i] in x)]
#        
#        # lines_list contains the lines_list from each text file where lines_list[i] contains all the lines_list of the i'th text file
#        ListofMat=self.importTextsToListofMat(txtList)           
#        lines_list = zip(*ListofMat)[0]
#        textFileLoc = zip(*ListofMat)[1]         
#        
#        if self.duplicates == None:
#            self.setDuplicates(lines_list,textFileLoc)
#            self.setDuplicatesThatWereKept()
#        
#        ######
#        ## Remove the text files that have the same start time as another     
#        #startSeshes = []
#        #for i in range(len(lines_list)):
#        #    startSeshes.append(lines_list[i][0][self.timeCol])
#        #
#        #def equalToAnother(elem):
#        #    return (startSeshes.count(elem) > 1)
#        #    
#        #def NOTequalToAnother(elem):
#        #    return (startSeshes.count(elem) == 1)  
#        #
#        ## Indices of all text files that are duplicates of another and those that are unique
#        #equalStartInd=map(equalToAnother,startSeshes)
#        #notEqualStartInd = map(NOTequalToAnother, startSeshes)
#        #
#        ## Retrieve text file names and start times that have duplicates
#        #textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
#        #startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
#        #
#        #
#        ## Sort these text files by start time  
#        #textFileEquals = self.sort_X_BasedOn_Y_BeingSorted(textFileEquals,startTimeEquals)
#        #startTimeEquals = self.sort_X_BasedOn_Y_BeingSorted(startTimeEquals,startTimeEquals)
#        ######
#        
#        #textFileEqualsOnlyOne = [] # you are the only one baby!
#        #startTimeEqualsOnlyOne = []
#        ## Create a list that only contains one (any one) of the textFiles that have a duplicate
#        #for i in range(len(startTimeEquals)):
#        #    if i != range(len(startTimeEquals))[-1]:
#        #        if startTimeEquals[i] != startTimeEquals[i+1]:
#        #            startTimeEqualsOnlyOne.append(startTimeEquals[i])
#        #            textFileEqualsOnlyOne.append(textFileEquals[i])
#        #    else:
#        #            startTimeEqualsOnlyOne.append(startTimeEquals[i])
#        #            textFileEqualsOnlyOne.append(textFileEquals[i])
#
#        
#        #notEqualStartInd = map(NOTequalToAnother, startSeshes)
#
#        
#        ###
#        # Remove all the text files that have a duplicate (another text file with identical startSesh) 
#        # notEqualStartInd - indices of all text files that have unique startSeshes
#        #lines_list = np.asarray(lines_list)[np.asarray(notEqualStartInd)]
#        #lines_list = lines_list.tolist()
#        #textFileLoc = np.asarray(textFileLoc)[np.asarray(notEqualStartInd)]
#        #textFileLoc = textFileLoc.tolist()
#        #startSeshes = np.asarray(startSeshes)[np.asarray(notEqualStartInd)]
#        #startSeshes = startSeshes.tolist()
#        ###
#        
#        # Remove all the text files that have a duplicate (another text file with identical startSesh) 
#        textFileEquals = zip(*self.duplicates)[0]
#        startTimeEquals = zip(*self.duplicates)[1]        
#        lines_list = [line for line in lines_list if line[0][self.timeCol] in startTimeEquals]
#        textFileLoc = [textF for textF in textFileLoc if textF in textFileEquals]
#        
#        assert(len(lines_list)==len(textFileLoc))
#        
#         
#        # Right, and now add only one of each of the duplicates back to 'lines_list'
#        #[linesOneDup,textFileLocOneDup]=importTextsToListofMat(textFileEqualsOnlyOne) 
#        textFileEqualsOnlyOne = zip(*self.duplicatesKept)[0]
#        ListofMat=self.importTextsToListofMat(textFileEqualsOnlyOne)           
#        linesOneDup = zip(*ListofMat)[0]
#        textFileLocOneDup = zip(*ListofMat)[1]
#        
#        for linesToAdd in linesOneDup:
#            lines_list.append(linesToAdd)
#        for locToAdd in textFileLocOneDup:
#            textFileLoc.append(locToAdd)  
#        
#        # Sort the text file contents and names by startSeshes
#        startSeshes = []
#        for i in range(len(lines_list)):
#            startSeshes.append(lines_list[i][0][self.timeCol])
#        textFileLoc = self.sort_X_BasedOn_Y_BeingSorted(textFileLoc,startSeshes)
#        lines_list = self.sort_X_BasedOn_Y_BeingSorted(lines_list,startSeshes)
#        
#        # Add these two to a dictionary
#        textDict = collections.OrderedDict(zip(textFileLoc, lines_list))                           
#        return textDict
        

    
    #def convertToUsefulDate(self,DateList): 
    #    """returns a list of dates converted to date objects"""                                                                                                                                                                                                
    #    DateList_pr = DateList[:]
    #    # Convert dates to date objects that are useable
    #    for i in range(len(DateList_pr)):
    #        DateList_pr[i]=(datetime.strptime(DateList[i], '%Y-%m-%d %H:%M:%S.%f'))   
    #    return DateList_pr                                                                                                                                                                                                     
    

                    

    

    

            

