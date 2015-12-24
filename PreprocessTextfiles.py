"""Class holding all attributes related to preprocessing textFiles"""

# Change working directory to where this module is before doing anything else
import os, sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import cfg
import os
import numpy as np
from datetime import datetime
import itertools
import csv
import copy

class PreprocessTextfiles:
    def __init__(self, absolute_start_time, absolute_end_time):
        self.absolute_start_time = datetime.strptime(absolute_start_time, '%Y-%m-%d %H:%M:%S')
        self.absolute_end_time = datetime.strptime(absolute_end_time, '%Y-%m-%d %H:%M:%S')
        # texts_not_imported gets its value at the end of the import_texts_to_list_of_mat function
        # Yes it is set to the same thing very inefficiently three times since the function is called
        # three times and it clearly will change to the last run of the function if any run is different
        # TODO: fix this inefficiency and poor design
        self.texts_not_imported = None
        self.txt_list = self.get_all_text_locs()

        # First get all the lines between the two times with only exact duplicates removed (same line in same text file)
        self.all_lines = self.import_texts_to_list_of_mat(self.txt_list)
        self.all_lines = list(itertools.chain.from_iterable(self.all_lines))
        # Sort the lines
        times = self.get_col(self.all_lines, cfg.TIME_COL)
        self.all_lines = self.sort_X_BasedOn_Y_BeingSorted(self.all_lines, times)

        # Make a list of all the text files we took data from
        self.texts_imported = self.get_col(self.all_lines, cfg.TEXT_LOC_COL)
        self.texts_imported = list(set(self.texts_imported))

        # Now do it again but remove all the duplicates
        self.all_lines_no_dupes = self.get_all_lines_no_dupes(self.txt_list)
        # Sort the lines
        times = self.get_col(self.all_lines_no_dupes, cfg.TIME_COL)
        self.all_lines_no_dupes = self.sort_X_BasedOn_Y_BeingSorted(self.all_lines_no_dupes, times)

        # if an output_dir was specified, output a csv to it
        self.output_all_lines_to_csv("all_lines", self.all_lines)
        self.output_all_lines_to_csv("all_lines_no_dupes",self.all_lines_no_dupes)
   
    def output_all_lines_to_csv(self, title, lines):
        """ouput all lines imported to a single csv"""
        with open(cfg.OUTPUT_LOC+"\\"+title+".csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames = [cfg.TAG_COL_NAME, cfg.TIME_COL_NAME, cfg.DATE_COL_NAME,
                                                     cfg.ACTION_COL_NAME, cfg.TEXT_LOC_COL_NAME], delimiter=',')
            writer.writeheader()
            writer = csv.writer(f)
            writer.writerows(lines)
            
    def sort_X_BasedOn_Y_BeingSorted(self, X, Y):
        """Sorts X based on the result from Y being sorted"""
        X = np.array(X)
        Y = np.array(Y)
        inds = Y.argsort()
        return(X[inds]) 
        
    def get_col(self,list_of_lists,col_num):
        """return desired column from list of lists as a list"""
        print(list_of_lists)
        print(np.asarray(list_of_lists))
        return list(np.asarray(list_of_lists)[:,col_num])    
       
    def get_all_text_locs(self):
        """Get a list of all text files in the given folder (including subdirectories)"""
        txt_list = []
        for root, dirs, files in os.walk(cfg.DIR_WITH_TEXTFILES):
            for file in files:
                if file.endswith(".txt"):
                    print(os.path.join(root, file))
                    txt_list.append(os.path.join(root, file))
                    
         # Remove all the paths that are subdirectories of the ignore folders
        for i in range(len(cfg.FOLDERS_TO_IGNORE)):
            txt_list=[x for x in txt_list if not (cfg.FOLDERS_TO_IGNORE[i] in x)]
        
        return txt_list
        
    def import_texts_to_list_of_mat(self, txtList):
        """ Import viable text_files to a list of matrices
            Returns a list of lists where each list is a textFile. A line column is added
            to each line specifying where the text file is that this line came from
        """    
        lines_list = []  
        text_file_loc = []
        texts_not_imported_col_condition = []
        texts_not_imported_row_condition = []
        texts_not_imported_absolute_start_condition = []

        # Add a column that records where each line is from (directory location)
        text_file_loc_each_line = []

        # Append them all into one matrix (the ones with the appropriate number of columns)
        for i in range(len(txtList)):
            text_file = txtList[i]
            try:
                with open(text_file) as f:
                    reader = csv.reader(f, delimiter="\t")
                    new_lines = list(reader)
                print(str(len(new_lines))+" - "+text_file)
                # Don't consider textfiles before specified time
                text_start_date = datetime.strptime(new_lines[0][cfg.DATE_COL], '%Y-%m-%d %H:%M:%S.%f')
                # TODO: Figure textFile selection criteria out
                text_end_date = datetime.strptime(new_lines[len(new_lines)-1][cfg.DATE_COL], '%Y-%m-%d %H:%M:%S.%f')
                if self.absolute_end_time > text_start_date > self.absolute_start_time:
                    # Only consider textFile with more than 2 rows and that have 'SeshStart' in first line                                                                                               
                    if len(new_lines) > 2 and new_lines[0][cfg.ACTION_COL] == cfg.seshStart_str:
                        # Add a row for textFiles missing a SeshEnd          
                        if new_lines[-1][cfg.ACTION_COL] != cfg.seshEnd_str:
                            new_lines.append(new_lines[-1][:])
                            new_lines[-1][cfg.ACTION_COL] = cfg.seshEnd_str
                            new_lines[-1][cfg.TAG_COL] = cfg.seshEndTag_str
                        for line_ind in range(len(new_lines)):
                            text_file_loc_each_line.append(txtList[i])
                            new_lines[line_ind] = new_lines[line_ind] + [txtList[i]]

                        lines_list.append(new_lines)
                        text_file_loc.append(txtList[i])
                    else:
                        print("Text file does not have enough rows - "+text_file)
                        texts_not_imported_row_condition.append(text_file)
                else:
                    print("Text file was taken too early - "+text_file)
                    texts_not_imported_absolute_start_condition.append(text_file)
            except BaseException:
                print("Text file does not have enough columns - "+text_file)
                texts_not_imported_col_condition.append(text_file)
        self.texts_not_imported = [texts_not_imported_col_condition,texts_not_imported_row_condition, texts_not_imported_absolute_start_condition]
        
        # Sort the text file contents and names by startSeshes
        startSeshes = []
        for i in range(len(lines_list)):
            startSeshes.append(lines_list[i][0][cfg.TIME_COL])
        print(startSeshes[0:5])
        print(text_file_loc[0:5])
        print(lines_list[0:5])
        text_file_loc = self.sort_X_BasedOn_Y_BeingSorted(text_file_loc, startSeshes)
        lines_list = self.sort_X_BasedOn_Y_BeingSorted(lines_list, startSeshes)
        print(text_file_loc[0:5])
        print(lines_list[0:5])    
        return(lines_list)
        
    def get_all_lines_no_dupes(self, txt_list):
        """Returns a list of lists that contains all lines from all text files in txt_list with duplicates removed"""
        lines_list = self.import_texts_to_list_of_mat(txt_list)
        lines_list = list(itertools.chain.from_iterable(lines_list))

        # Delete the column containing textFile locations so that duplicates can be properly removed
        # Create a copy
        lines_list_copy = copy.deepcopy(lines_list)
        for x in lines_list_copy:
          del x[cfg.TEXT_LOC_COL]
        lines_list_copy = [list(x) for x in set(tuple(x) for x in lines_list_copy)]
        # The copy now contains all the unique lines without the textFile locs

        # Re-ad the textFile locs to the copy
        for line_copy_ind in range(len(lines_list_copy)):
            for line_ind in range(len(lines_list)):
                if lines_list_copy[line_copy_ind][cfg.TIME_COL] == lines_list[line_ind][cfg.TIME_COL] and \
                        len(lines_list_copy[line_copy_ind]) == 4:
                    lines_list_copy[line_copy_ind].append(lines_list[line_ind][cfg.TEXT_LOC_COL])
        lines_list = lines_list_copy

        return lines_list
        
    def eAnd(self, *args):
        """Returns a list that is the element-wise 'and' operation along each index of each list in args"""
        return [all(tuple) for tuple in zip(*args)]   

    # def set_bins(self):
    #     """
    #     Bin list of all sorted lines_list into per binTime lists
    #     For your convenience: there are 86400 seconds in a day
    #     Returns: BinnedList: np.array([[a],[b]...]) where the first line in a,b... is binTime seconds before the last
    #     """
    #     all_lines = self.all_lines
    #     column_of_times = self.get_col(all_lines, cfg.TIME_COL)
    #     column_of_times = [float(x) for x in column_of_times]
    #     column_of_times = np.array(column_of_times)
    #     all_lines = np.array(all_lines)
    #
    #     binned_lines = []
    #     # TODO: Make sure changing this didn't fuck up the BINS
    #     # start_ind = column_of_times[0]
    #     start_ind = time.mktime(cfg.ABSOLUTE_START_TIME.timetuple())
    #     end_ind = start_ind + cfg.BIN_TIME
    #
    #     bins_start_end = []
    #     bin_start_dates = []
    #     bin_end_dates = []
    #
    #     while end_ind <= column_of_times[len(column_of_times)-1]:
    #         the_bin = all_lines[np.array(self.eAnd(column_of_times >= start_ind, column_of_times < end_ind))]
    #         binned_lines.append(the_bin)
    #         start_ind = end_ind
    #         end_ind = end_ind + cfg.BIN_TIME
    #
    #         def seconds_to_date(seconds):
    #             try:
    #                 date = time.strftime('%Y-%m-%d %H:%M:%S.%f', time.localtime(seconds))
    #             except Exception:
    #                 try:
    #                     date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))
    #                 except Exception:
    #                     print('DATE FORMAT INCOMPREHENSIBLE. Date ignored. Bins fucked up')
    #                     assert(1 == 0)
    #                     date = 0
    #             return date
    #
    #         start_ind_date = seconds_to_date(start_ind)
    #         end_ind_date = seconds_to_date(end_ind)
    #         bins_start_end = bins_start_end + [[start_ind_date, end_ind_date]]
    #         bin_start_dates = bin_start_dates + [start_ind_date]
    #         bin_end_dates = bin_end_dates + [end_ind_date]
    #
    #
    #         print('bin created from ' + str(start_ind_date) + ' to ' + str(end_ind_date))
    #     self.binned_lines = binned_lines
    #     self.bins_start_end = bins_start_end
    #     self.bin_start_dates = bin_start_dates
    #     self.bin_end_dates = bin_end_dates

        
###################################        
        
        
    # def get_col_binned_lines(self, binned_lines, col_num):
    #     """return list of lists that would be the binned lists of a particular column"""
    #     if self.binned_lines == None:
    #         assert(1 == 0, 'binned_lines have not been set')
    #     binned_lines_col = []
    #     for lines_list in binned_lines:
    #         if len(lines_list) > 0:
    #             binned_lines_col.append(self.get_col(lines_list,col_num))
    #         else:
    #             binned_lines_col.append(lines_list)
    #     return binned_lines_col
    #
    # def get_binned_rows_tag(self, binned_lines, chosen_tags):
    #     """return list of lists that are all binned lines that are by a mouse in tags """
    #     if self.binned_lines == None:
    #         assert(1 == 0, 'binned_lines have not been set')
    #     binned_lines_tags = []
    #
    #     for lines_list in binned_lines:
    #         the_bin = []
    #         for line in lines_list:
    #             if int(line[cfg.TAG_COL]) in chosen_tags:
    #                 the_bin.append(line)
    #         binned_lines_tags.append(the_bin)
    #     return binned_lines_tags
    #
    # def get_freq_list_binned(self, binned_lines, item, col_num):
    #     """return list of list that is the count of the occurence of 'item' in each list (in column col_num) in binned_lines"""
    #     if self.binned_lines == None:
    #         assert(1 == 0, 'binned_lines have not been set')
    #     freqs = []
    #
    #     chosen_col = self.get_col_binned_lines(binned_lines, col_num)
    #     for its in chosen_col:
    #         freqs.append(its.count(item))
    #     return freqs
    #
    # def find_freqs_for_each(self,item,col_num,chosen_tags):
    #     """return list of list that is the counts for each mouse for each bin for item in col_num"""
    #     if self.binned_lines == None:
    #         assert(1 == 0, 'binned_lines have not been set')
    #     freqs_for_each = []
    #     for lines_list in self.binned_lines:
    #         freqs_for_bin = []
    #         for tag in chosen_tags:
    #             tag_rows_bin = self.get_binned_rows_tag([lines_list],[tag])
    #             if len( tag_rows_bin[0]) == 0:
    #                 freqs_for_bin.append(0)
    #             else:
    #                 freqs_for_bin.append(self.get_freq_list_binned(tag_rows_bin,item,col_num)[0])
    #         freqs_for_each.append(freqs_for_bin)
    #     return freqs_for_each

        
        
        

    


    

    

            

