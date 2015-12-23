"""Plot line graphs of each mouse's entry and headFix 

Typical example:
workingDir = T:/AutoHeadFix/
foldersToIgnore = ["Old and or nasty data goes here"]
"""

# Change working directory to where this module is before doing anything else
import os, sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
import cfg
from PreprocessTextfiles import PreprocessTextfiles
from Mouse import Mouse
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import pickle
import csv
import sys

# pickle_name (str): the name of a pickle file that contains preprocessed textFiles, placed in the same directory as this script
pickle_name = raw_input("What is the name of your pickle, good sir? Save it in the folder where this is being run from."
                        " If your pickle isn't pickled we shall now pick it ") + '.p'
# "C:\\Users\\user\\Documents\\Dirk\\Bokeh\\AutoHeadfix_AutoAnalyzer\\Output\\current_dat.p"

# Try to load saved preprocessed text files if they are on hand
try:
    current_dat = pickle.load(open(pickle_name, "rb" ))
except BaseException:
    print("No Pickle. Preprocessing textfiles from " + cfg.DIR_WITH_TEXTFILES + " instead")
    current_dat = PreprocessTextfiles()
    pickle.dump(current_dat, open(pickle_name, "wb" ))

    # TODO: Also save current_dat.all_lines to binary
    # load from the file
    # mat = current_dat.all_lines
    # outputfile = os.getcwd()+'\\'+pickle_name
    #
    # # create a binary file
    # binfile = file(outputfile, 'wb')
    # # and write out two integers with the row and column dimension
    # header = struct.pack('2I', mat.shape[0], mat.shape[1])
    # binfile.write(header)
    # # then loop over columns and write each
    # for i in range(mat.shape[1]):
    #     data = struct.pack('%id' % mat.shape[0], *mat[:, i])
    #     binfile.write(data)
    # binfile.close()

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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def genplot_error_bars(x, y, yerror, tit, ylab, xlab, out_loc = cfg.OUTPUT_LOC):
    """Plots x vs y with yerror for error bars, tit as title ylab, xlab as labels for axis and outputs
    graph to out_loc."""
    fig = plt.figure()
    plt.errorbar(x, y, yerr=yerror)
    plt.title(tit)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.show()
    plt.savefig(out_loc+tit+" "+ylab+".png", bbox_inches='tight')   
    
def gen2plots_error_bars(x1, y1, x2, y2, yerror1, yerror2, legend1, legend2, tit, ylab, xlab, out_loc=cfg.OUTPUT_LOC):
    """Plots x1 vs y1 and x2 vs y2 on same axis with yerror1 and 2 for error bars,
    tit as title ylab, xlab as labels for axis, legends1 and 2 to describe the two plots
    and outputs graph to out_loc."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    # TODO: uncomment errorbars
    ax.errorbar(x1, y1, yerr=yerror1, ecolor='r')
    p1 = ax.plot(x1, y1, color='r', label=legend1, linewidth=2.0)
    ax2.errorbar(x2, y2, yerr=yerror2, ecolor='g')
    p2 = ax2.plot(x2, y2, color='g', label=legend2, linewidth=2.0)

    # Legend
    l1 = ax.legend(loc=2, fontsize=25)
    l2 = ax2.legend(loc=0, fontsize=25)
    l1.legendHandles[0].set_linewidth(30.0)
    l2.legendHandles[0].set_linewidth(30.0)
    #l1.legendHandles.set_linewidth(2.0)
    #l2.legendHandles.set_linewidth(2.0)

    # set the linewidth of each legend object
    # for legobj in leg.legendHandles:
    #     legobj.set_linewidth(2.0)

    # X and y labels
    ax.set_xlabel(xlab, fontsize=30)
    # TODO: Resolve whether to keep ylab and xlab
    # ax.set_ylabel(ylab+' '+legend1)
    # ax2.set_ylabel(ylab+' '+legend2)
    ax.set_ylabel(legend1, fontsize=30)
    ax2.set_ylabel(legend2, fontsize=30)

    # Ticks 'n spines
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    ax2.tick_params(axis='y', labelsize=30)
    ax.tick_params('both', length=20, width=2, which='major', top='off')
    ax2.tick_params('both', length=20, width=2, which='major', top='off')
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # TODO: Pick ylim and xlim
    ax.set_ylim(min(y1), max(y1))
    ax2.set_ylim(min(y2), max(y2))
    ax.set_xlim(min(x1)-1, max(x1)+1)
    #ax.set_ylim(min(min(y1),min(y2)), max(max(y1),max(y2)))
    #ax2.set_ylim(min(min(y1),min(y2)), max(max(y1),max(y2)))

    # TODO: Delete these comments if not needed
    # green_line = mpatches.Patch(color='green', label=legend2)
    # blue_line = mpatches.Patch(color='blue', label=legend1)
    # plt.legend(handles=[green_line,blue_line])
    # TODO: Readd title
    #plt.title(tit)
    #plt.ylabel(ylab)
    #plt.xlabel(xlab)
    plt.show()
    plt.savefig(cfg.OUTPUT_LOC+tit+" "+ylab+".png", bbox_inches='tight')

def plot_results_for_tags(chosen_tags, out_loc, k):
    """ chosen_tags [int]: tags of mice for which plots are to be made
    out_loc (str): location where plots will be saved to file
    Plots 3 plots, 1 for average headfix frequency, 1 for entries and 
    another with both on the same axis. All with error bars for a specified group   
    """
    yDist_hf = current_dat.find_freqs_for_each(cfg.HEADFIX_STR, cfg.ACTION_COL, chosen_tags)
    yDist_entry = current_dat.find_freqs_for_each(cfg.ENTRY_STR, cfg.ACTION_COL, chosen_tags)

    yerror_hf = map(pstdev, yDist_hf)
    y_hf = map(mean, yDist_hf)
    yerror_entry = map(pstdev, yDist_entry)

    print(yDist_entry)
    print(yerror_entry)

    # TODO: choose SEM or SD
    yerror_hf = map(stats.sem, yDist_hf)
    yerror_entry = map(stats.sem, yDist_entry)
    print(yerror_entry)

    y_entry = map(mean, yDist_entry)
    x = [i+1 for i in range(len(yDist_hf))]
    assert(len(yDist_hf) == len(yDist_entry))
    
    ylab = 'Average Frequency'
    xlab = 'day'
    legend1 = 'head-fixes/mouse/day'
    legend2 = 'entries/mouse/day'
    
    gen2plots_error_bars(x, y_hf, x, y_entry, yerror_hf, yerror_entry, legend1, legend2, k+' Average Daily Frequency of Actions', ylab, xlab, out_loc=cfg.OUTPUT_LOC)
    # TODO: Uncomment
    #genplot_error_bars(x,y_hf,yerror_hf,k+' Average Daily Headfix Frequency',ylab,xlab,out_loc=cfg.OUTPUT_LOC)
    #genplot_error_bars(x,y_entry,yerror_entry,k+' Average Daily Entry Frequency',ylab,xlab,out_loc=cfg.OUTPUT_LOC)


def plot_time_between_actions_for_tag(chosen_tag,out_loc,actionA,actionB,current_dat,bin_time):  
    """Plots the amount of time spent between actionA and actionB for a mouse for each bin"""  
    m = Mouse(chosen_tag,cfg.MICE_GROUPS,current_dat,bin_time)
      
    y = m.time_between_actions_list(actionA,actionB)
    x = [i+1 for i in range(len(y))]
    yerror = 0
    tit = str(chosen_tag) + ' - ' + actionA +' - '+actionB
    xlab= 'Day'
    ylab = 'Total time spent inbetween actions in 24 hours'

    genplot_error_bars(x,y,yerror,tit,ylab,xlab)


def hists_that_tim_likes_for_bokeh(action1,action2,bin_no,cut_off=None):
    """Plots histrograms of intervals between action1 and action2 for each mouse 
    with bin_no bins and doesn't display any values above cut_off
    returns the interval times and the interval times above the cut_off"""
    timesbetweens = []
    timesbetweens_cutoff = []
    
    for tag in cfg.TAGS:
        fig, ax = plt.subplots()
        m = Mouse(tag,cfg.MICE_GROUPS,current_dat,cfg.BIN_TIME)
        timesbetween = m.get_between_actions_dist(action1,action2)
        # Get those too far right
        timesbetween_cutoff = [i for i in timesbetween if i >= cut_off]
        # Get rid of the ones too far to the right
        if cut_off != None:
            timesbetween = [i for i in timesbetween if i < cut_off]
        timesbetweens.append(timesbetween)
        timesbetweens_cutoff.append(timesbetween_cutoff)
       
        hist, bins = np.histogram(timesbetween, bins=bin_no)
        tit = str(tag) + ' - '+action1 + ' to ' + action2
        xlab = 'Time between headfixes'
        plt.title(tit, fontsize=28)
        plt.ylabel('Frequency', fontsize=28)
        plt.xlabel(xlab, fontsize=28)
        width = 0.5 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()
        plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

        fig, ax = plt.subplots()
                
        hist, bins = np.histogram(timesbetween_cutoff, bins=bin_no)
        tit = str(tag) + ' - ' + action1 + ' to '+action2 + ' after cutoff'
        xlab = 'Time spent in chamber'
        plt.title(tit)
        plt.ylabel('Frequency')
        plt.xlabel(xlab)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()
        plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')
        
    return [timesbetweens, timesbetweens_cutoff]

def hists_for_selected_mice_matrix_maker(action1, action2, selected_mice):
    """
    :return: a list of lists that contains the intervals between action1 and 2, the start times and the textfile source
    each time point, with a header all ready to be saved to csv
    """
    timesbetweens = []
    interval_start_dates_all = []
    interval_end_dates_all = []
    interval_start_times_all = []
    interval_end_times_all = []
    interval_start_textfiles_all = []
    interval_end_textfiles_all = []

    # Get data for all selected mice and add to lists
    for tag in selected_mice:
        m = Mouse(tag, cfg.MICE_GROUPS, current_dat, cfg.BIN_TIME)
        [timesbetween, interval_start_dates, interval_end_dates, interval_start_times, interval_end_times,
                interval_start_textfiles, interval_end_textfiles] = m.get_between_actions_dist(action1, action2)
        interval_tag = len(timesbetween)*[tag]

        timesbetweens = timesbetweens + timesbetween
        # Concatenate additional info
        interval_start_dates_all = interval_start_dates_all + interval_start_dates
        interval_end_dates_all = interval_end_dates_all + interval_end_dates
        interval_start_times_all = interval_start_times_all + interval_start_times
        interval_end_times_all = interval_end_times_all + interval_end_times
        interval_start_textfiles_all = interval_start_textfiles_all + interval_start_textfiles
        interval_end_textfiles_all = interval_end_textfiles_all + interval_end_textfiles

        # Smash these all into one list of lists
        timesbetweens_matrix = [timesbetweens, interval_start_dates_all, interval_end_dates_all,
                                interval_start_times_all, interval_end_times_all,
                                interval_start_textfiles_all, interval_end_textfiles_all]
        # Transpose that sucker
        timesbetweens_matrix = np.asarray(timesbetweens_matrix).T.tolist()
        # Add a header
        header = ["timesbetween", "interval_start_dates", "interval_end_dates", "interval_start_times",
                  "interval_end_times", "interval_start_textfiles", "interval_end_textfiles"]
        timesbetweens_matrix = [header] + timesbetweens_matrix
        return timesbetweens_matrix

def get_col(list_of_lists,col_num):
        """return desired column from list of lists as a list"""
        return list(np.asarray(list_of_lists)[:][ col_num])

def get_cut_off_subset(timesbetweens_matrix, cut_off):
    return [row[0] for row in timesbetweens_matrix if type(row[0]) is not str and row[0] < cut_off]

def hists_for_selected_mice(action1, action2, bin_no, selected_mice, cut_off = None):
    """Plots histrograms of intervals between action1 and action2 for selected mice
    with bin_no bins and doesn't display any values above cut_off
    returns the interval times and the interval times above the cut_off"""
    timesbetweens_matrix = hists_for_selected_mice_matrix_maker(action1, action2, selected_mice)
    if cut_off != None:
      timesbetweens_cutoff_matrix = get_cut_off_subset(timesbetweens_matrix, cut_off)

    # Retrieve interval times. Remove header
    timesbetweens = timesbetweens_matrix[1:]
    timesbetweens_cutoff = timesbetweens_matrix[1:]
    timesbetweens = [float(x[0]) for x in timesbetweens]
    timesbetweens_cutoff = [float(x[0]) for x in timesbetweens_cutoff]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    hist, bins = np.histogram(timesbetweens, bins=bin_no)

    tit = str(selected_mice)+' - '+action1+ ' to '+action2
    xlab = 'time between head-fixes (s)'
    # TODO: Readd title
    plt.title(tit)
    plt.ylabel('N', fontsize=40)
    plt.xlabel(xlab, fontsize=40)
    ax.tick_params(axis='x', labelsize=40)
    ax.tick_params(axis='y', labelsize=40)

    # TODO: decide whether to keep this
    ##
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    def adjustFigAspect(fig, aspect=1):
        '''
        Adjust the subplot parameters so that the figure has the correct
        aspect ratio.
        '''
        xsize,ysize = fig.get_size_inches()
        minsize = min(xsize,ysize)
        xlim = .4*minsize/xsize
        ylim = .4*minsize/ysize
        if aspect < 1:
            xlim *= aspect
        else:
            ylim /= aspect
        fig.subplots_adjust(left=.5-xlim,
                            right=.5+xlim,
                            bottom=.5-ylim,
                            top=.5+ylim)
    adjustFigAspect(fig, aspect=1)
    ##

    width = 0.5 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
    fig.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

    fig, ax = plt.subplots()

    hist, bins = np.histogram(timesbetweens_cutoff, bins=bin_no)
    tit = str(selected_mice)+' - '+action1+ ' to '+action2 + ' after cutoff'
    xlab = 'Time spent in chamber'
    plt.title(tit)
    plt.ylabel('Frequency')
    plt.xlabel(xlab)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
    plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

    return [timesbetweens, timesbetweens_cutoff]


# TODO LATER: get all the stats on all the mice and save csv, use mouse class (because fuck you Canopy for crashing and not autosaving)    
def global_stats():
    
    #for k in cfg.MICE_GROUPS.keys():
    #    #for tags in cfg.MICE_GROUPS[k]:
    #        freqs_hf = 0
    #        freqs_ent = 0
    #        for tag in tags:
    #            freqs_hf_new=current_dat.find_freqs_for_each(cfg.HEADFIX_STR,cfg.ACTION_COL,[tag])
    #            freqs_ent_new=current_dat.find_freqs_for_each(cfg.ENTRY_STR,cfg.ACTION_COL,[tag])
    #            freqs_hf = freqs_hf + freqs_hf_new
    #            freqs_ent = freqs_ent + freqs_ent_new  
    #        print("Total Heafixes made by "+str(k)+": "+str(sum(freqs_hf)))
    #        print("Total Entries made by "+str(k)+": "+str(sum(freqs_ent)))
    #        print("Average Daily Heafixes made by "+str(k)+": "+str(sum(freqs_hf)/len(freqs_hf)))
    #        print("Average Daily Entries made by "+str(k)+": "+str(sum(freqs_ent)/len(freqs_ent)))
    #        print("Average Daily Heafixes per Mouse made by "+str(k)+": "+str(sum(freqs_hf)/len(freqs_hf)))
    #        print("Average Daily Entries per Mouse made by "+str(k)+": "+str(sum(freqs_ent)/len(freqs_ent)))
    for k in cfg.MICE_GROUPS.keys():
        freqs_hf=current_dat.find_freqs_for_each(cfg.HEADFIX_STR,cfg.ACTION_COL,cfg.MICE_GROUPS[k])
        freqs_ent=current_dat.find_freqs_for_each(cfg.ENTRY_STR,cfg.ACTION_COL,cfg.MICE_GROUPS[k])
        print("Total Heafixes made by "+str(k)+": "+str(sum(freqs_hf)))
        print("Total Entries made by "+str(k)+": "+str(sum(freqs_ent)))
        print("Average Daily Heafixes made by "+str(k)+": "+str(sum(freqs_hf)/len(freqs_hf)))
        print("Average Daily Entries made by "+str(k)+": "+str(sum(freqs_ent)/len(freqs_ent)))
        
        avg_daily_hf=sum(freqs_hf)/len(freqs_hf)
        avg_daily_ent =sum(freqs_ent)/len(freqs_ent)
        
        print("Average Daily Heafixes per Mouse made by "+str(k)+": "+str(avg_daily_hf/len(cfg.MICE_GROUPS[k])))
        print("Average Daily Entries per Mouse made by "+str(k)+": "+str(avg_daily_ent/len(cfg.MICE_GROUPS[k])))
    
    
    for tag in cfg.TAGS:
        freqs_hf=current_dat.find_freqs_for_each(cfg.HEADFIX_STR,cfg.ACTION_COL,[tag])
        freqs_ent=current_dat.find_freqs_for_each(cfg.ENTRY_STR,cfg.ACTION_COL,[tag])
        print("Total Heafixes made by "+str(tag)+": "+str(sum(freqs_hf)))
        print("Total Entries made by "+str(tag)+": "+str(sum(freqs_ent)))
        print("Average Daily Heafixes made by "+str(tag)+": "+str(sum(freqs_hf)/len(freqs_hf)))
        print("Average Daily Entries made by "+str(tag)+": "+str(sum(freqs_ent)/len(freqs_ent)))
        

def output_csv(arr, tit):
    """ouput arr to a single csv"""
    with open(cfg.OUTPUT_LOC+"\\"+tit+'.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(arr)


#### UNCOMMENT TO GET GRAPHS ###
#for tag in cfg.TAGS:
#   plot_time_between_actions_for_tag(tag,cfg.OUTPUT_LOC,'entry','exit',current_dat,cfg.BIN_TIME)
#   plot_time_between_actions_for_tag(tag,cfg.OUTPUT_LOC,'reward0','check+',current_dat,cfg.BIN_TIME)

#for k in cfg.MICE_GROUPS.keys():
#   plot_results_for_tags(cfg.MICE_GROUPS[k],cfg.OUTPUT_LOC,k)

#plot_results_for_tags(cfg.TAGS, cfg.OUTPUT_LOC, 'All Mice')

#[timesbetweens,timesbetweens_cutoff] = hists_that_tim_likes_for_bokeh('entry','exit',20,600)
#[timesbetweens, timesbetweens_cutoff] = hists_that_tim_likes_for_bokeh('reward0','check+',20,600)

hists_for_selected_mice('entry', 'exit', 20, cfg.TAGS, 600)
[timesbetweens, timesbetweens_cutoff] = hists_for_selected_mice('reward0', 'check+', 20, cfg.TAGS, 600)

entry_interval_matrix = hists_for_selected_mice_matrix_maker('entry', 'exit', cfg.TAGS)
entry_interval_matrix_cutoff = get_cut_off_subset(entry_interval_matrix, 600)
headfix_interval_matrix = hists_for_selected_mice_matrix_maker('reward0', 'check+', cfg.TAGS)
headfix_interval_matrix_cutoff = get_cut_off_subset(headfix_interval_matrix, 600)

output_csv(entry_interval_matrix, "Times between entry and exit for 52 days for all mice")
output_csv(entry_interval_matrix_cutoff, "Times between entry and exit for 52 days for all mice with 600 second cutoff")
output_csv(headfix_interval_matrix, "Times between reward0 and check+ for 52 days for all mice")
output_csv(headfix_interval_matrix_cutoff, "Times between reward0 and check+ for 52 days for all mice with 600 second cutoff")

#dist_hf = current_dat.find_freqs_for_each(cfg.HEADFIX_STR, cfg.ACTION_COL, cfg.TAGS)
#########


# totes_for_all = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
# for i in range(len(totes_for_all)):
#     for das_bin in dist_hf:
#         totes_for_all[i] = totes_for_all[i] + das_bin[i]
#
# print(totes_for_all)
# print(pstdev(totes_for_all))
#
# print(map(pstdev, dist_hf))
# print(map(stats.sem, dist_hf))

#print(pstdev([sum(i) for i in dist_hf]))
#print(stats.sem([sum(i) for i in dist_hf]))

#print(sum([sum(i) for i in dist_hf]))
#print(len(timesbetweens)+len(timesbetweens_cutoff))

# current_dat
# 6485
# 6562

# current_dat_new



# for i in range(len(cfg.TAGS)):
#     fig, ax = plt.subplots()
#
#     hist, bins = np.histogram(timesbetweens_cutoff[i], bins=20)
#     tit = str(cfg.TAGS[i])+' - '+'entry'+ ' to '+'exit' + ' after cutoff'
#     xlab = 'Time spent in chamber'
#     plt.title(tit)
#     plt.ylabel('Frequency')
#     plt.xlabel(xlab)
#     width = 0.7 * (bins[1] - bins[0])
#     center = (bins[:-1] + bins[1:]) / 2
#     plt.bar(center, hist, align='center', width=width)
#     plt.show()
#     plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

# global_stats()



def hist_raw_count(action, mice, tit, xlab,ylab):
    """Plots a histrogram that is the raw count of action for each bin in the PreprocessTextfiles obj for mice"""
    # binned_rows = current_dat.binned_lines
    binned_rows = current_dat.get_binned_rows_tag(current_dat.binned_lines, mice)
    print(binned_rows)
    act_bins = current_dat.get_col_binned_lines(binned_rows, cfg.ACTION_COL)
    count_act_bins = [a_bin.count(action) for a_bin in act_bins]
    # time_bins = current_dat.get_col_binned_lines(binned_rows, cfg.DATE_COL)

    bin_starts = current_dat.bin_start_dates
    bin_starts = Mouse.convert_to_date_obj(bin_starts)
    print(len(count_act_bins))
    print(len(bin_starts))


    # TODO: See if any of the following can be used
    ##
    # # output_csv([time_bins], 'Please work or I kill you')
    # for li in time_bins:
    #     print('start -- '+str(li[0]))
    #     print('end -- '+str(li[len(li)-1]))
    # ##
    #
    # # Get the first time in each bin
    # first_times = [time_bin[0] for time_bin in time_bins]
    # output_csv([first_times, count_act_bins, act_bins], 'EL hist_raw_count reward0')
    #
    # print(len(current_dat.binned_lines))
    # print(len(first_times))
    # print(bin_starts)
    # print(first_times)
    # print(count_act_bins)
    # assert(len(first_times) == len(count_act_bins))
    # #assert(len(bin_starts) == len(count_act_bins))
    #
    # ##
    # # first_times = [mktime(datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f").timetuple()) for i in first_times]
    # ##
    #
    # # TODO: delete above, reinstate function call?
    #first_times = Mouse.convert_to_date_obj(first_times)


    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(tit)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    # TODO: delete xticks
    # plt.xticks(first_times, first_times_ticks)
    # TODO: decide whether to include these four lines
    ##
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ##
    # TODO: Figure out how to make the width equal to whatever the binning is
    #plt.bar(first_times, count_act_bins, width=0.01)
    plt.bar(bin_starts, count_act_bins, width=0.01)
    fig.autofmt_xdate()
    plt.show(block=False)
    plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

    return([bin_starts,count_act_bins])


# TODO: MOVE THESE CALLS!

# for tag in cfg.TAGS:
#     [bin_starts, count_act_bins] = hist_raw_count('reward0', [tag], 'Insert Title', 'time (h)', 'head-fixes/h/cage')
#     output_csv([bin_starts,count_act_bins], 'Headfixes per hour for mouse '+str(tag))
#
# for key in cfg.MICE_GROUPS.keys():
#     [bin_starts, count_act_bins] = hist_raw_count('reward0', cfg.MICE_GROUPS[key], 'Insert Title', 'time (h)', 'head-fixes/h/cage')
#     output_csv([bin_starts,count_act_bins], 'Headfixes per hour for group '+str(key))

#[bin_starts, count_act_bins] = hist_raw_count('reward0', cfg.MICE_GROUPS['EP'], 'Insert Title', 'time (h)', 'head-fixes/h/cage')
#output_csv([bin_starts,count_act_bins], 'BlairAnalysis-EP Headfixes per hour')




#print(current_dat.texts_imported)


# TODO: Figure out why the hell you have two of this function
def gen2plots_error_bars(x1, y1, x2, y2, yerror1, yerror2, legend1, legend2, tit, ylab, xlab, out_loc=cfg.OUTPUT_LOC):
    """Plots x1 vs y1 and x2 vs y2 on same axis with yerror1 and 2 for error bars,
    tit as title ylab, xlab as labels for axis, legends1 and 2 to describe the two plots
    and outputs graph to out_loc."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    # TODO: uncomment errorbars
    #ax.errorbar(x1, y1, yerr=yerror1, ecolor='b')
    ax.plot(x1, y1, color='b', label=legend1, linewidth=2.0)
    #ax2.errorbar(x2, y2, yerr=yerror2, ecolor='g')
    ax2.plot(x2, y2, color='g', label=legend2, linewidth=2.0)

    ax.legend(loc=2, fontsize=25)
    ax2.legend(loc=0, fontsize=25)
    ax.set_xlabel(xlab, fontsize=25)
    # TODO: Resolve whether to keep ylab and xlab
    #ax.set_ylabel(ylab+' '+legend1)
    #ax2.set_ylabel(ylab+' '+legend2)
    ax.set_ylabel(legend1, fontsize=25)
    ax2.set_ylabel(legend2, fontsize=25)

    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax2.tick_params(axis='y', labelsize=25)

    ax.tick_params('both', length=20, width=2, which='major')
    ax2.tick_params('both', length=20, width=2, which='major')
    #ax2.tick_params('both', length=10, width=1, which='minor')

    #ax.set_ylim(-25, 250)
    #ax2.set_ylim(-25, 250)

    ax.set_ylim(min(y1), max(y1))
    ax2.set_ylim(min(y2), max(y2))
    ax.set_xlim(min(x1)-1, max(x1)+1)

    #ax.set_ylim(min(min(y1),min(y2)), max(max(y1),max(y2)))
    #ax2.set_ylim(min(min(y1),min(y2)), max(max(y1),max(y2)))

    # green_line = mpatches.Patch(color='green', label=legend2)
    # blue_line = mpatches.Patch(color='blue', label=legend1)
    # plt.legend(handles=[green_line,blue_line])
    plt.title(tit)
    #plt.ylabel(ylab)
    #plt.xlabel(xlab)
    plt.show()
    plt.savefig(cfg.OUTPUT_LOC+tit+" "+ylab+".png", bbox_inches='tight')


#def hist(x):
#    """Plots histrograms of x"""
#    timesbetweens = []
#    timesbetweens_cutoff = []
#    
#    for tag in cfg.TAGS:
#        fig, ax = plt.subplots()
#        m = Mouse(tag,cfg.MICE_GROUPS,current_dat,cfg.BIN_TIME)
#        timesbetween = m.get_between_actions_dist(action1,action2) 
#        timesbetweens.append(timesbetween)
#        # Get those too far right
#        timesbetween_cutoff = [i for i in timesbetween if i >= cut_off]
#        timesbetweens_cutoff.append(timesbetween_cutoff)
#        # Get rid of the ones too far to the right
#        timesbetween = [i for i in timesbetween if i < cut_off]
#
#        
#        hist, bins = np.histogram(timesbetween, bins=bin_no)
#        tit = str(tag)+' - '+action1+ ' to '+action1
#        xlab = 'Time between headfixes'
#        plt.title(tit)
#        plt.ylabel('Frequency')
#        plt.xlabel(xlab)
#        width = 0.5 * (bins[1] - bins[0])
#        center = (bins[:-1] + bins[1:]) / 2
#        plt.bar(center, hist, align='center', width=width)
#        plt.show()
#        plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')
        


                   
# def bokeh():
#     # output to static HTML file
#     output_file("hists_that_tim_likes.html", title="line plot example")
#
#     # create a new plot with a title and axis labels
#     p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
#
#     # add a line renderer with legend and line thickness
#     #hist = Histogram(x, y, legend="Temp.", line_width=2)
#
#     # show the results
#     show(hist)