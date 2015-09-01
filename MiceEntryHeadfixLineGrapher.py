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
import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle
import os
import csv
# Bokeh
import time
from bokeh.plotting import figure, output_file, output_server, cursession, show

# pickle_name (str): the name of a pickle file that contains preprocessed textFiles, placed in the same directory as this script 
##pickle_name=raw_input("What is the name of your pickle, good sir? Save it in the folder where this is being run from")
##    "C:\\Users\\user\\Documents\\Dirk\\Bokeh\\AutoHeadfix_AutoAnalyzer\\Output\\current_dat.p"
pickle_name = "current_dat"      
pickle_name = pickle_name+'.p'
    
# Try to load saved preprocessed text files if they are on hand
try:
    current_dat=pickle.load(open( pickle_name, "rb" ))
except BaseException:
    print("No Pickle. Preprocessing textfiles from working_dir instead")
    current_dat = PreprocessTextfiles()
    pickle.dump(current_dat, open(pickle_name, "wb" ) )
    
current_dat.set_bins()

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
    #ax.errorbar(x1, y1, yerr=yerror1, ecolor='b')
    p1 = ax.plot(x1, y1, color='b', label=legend1, linewidth=2.0)
    #ax2.errorbar(x2, y2, yerr=yerror2, ecolor='g')
    p2 = ax2.plot(x2, y2, color='g', label=legend2, linewidth=2.0)

    # Legend
    l1 = ax.legend(loc=2, fontsize=25)
    l2 = ax2.legend(loc=0, fontsize=25)
    l1.legendHandles[0].set_linewidth(20.0)
    l2.legendHandles[0].set_linewidth(20.0)
    #l1.legendHandles.set_linewidth(2.0)
    #l2.legendHandles.set_linewidth(2.0)

    # set the linewidth of each legend object
    # for legobj in leg.legendHandles:
    #     legobj.set_linewidth(2.0)

    # X and y labels
    ax.set_xlabel(xlab, fontsize=25)
    # TODO: Resolve whether to keep ylab and xlab
    # ax.set_ylabel(ylab+' '+legend1)
    # ax2.set_ylabel(ylab+' '+legend2)
    ax.set_ylabel(legend1, fontsize=25)
    ax2.set_ylabel(legend2, fontsize=25)

    # Ticks 'n spines
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax2.tick_params(axis='y', labelsize=25)
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

def plot_results_for_tags(chosen_tags,out_loc,k):
    """ chosen_tags [int]: tags of mice for which plots are to be made
    out_loc (str): location where plots will be saved to file
    Plots 3 plots, 1 for average headfix frequency, 1 for entries and 
    another with both on the same axis. All with error bars for a specified group   
    """
    yDist_hf=current_dat.find_freqs_for_each(cfg.HEADFIX_STR,cfg.ACTION_COL,chosen_tags)
    yDist_entry=current_dat.find_freqs_for_each(cfg.ENTRY_STR,cfg.ACTION_COL,chosen_tags)
    
    yerror_hf=map(pstdev,yDist_hf)
    y_hf = map(mean,yDist_hf)
    yerror_entry=map(pstdev,yDist_entry)
    y_entry = map(mean,yDist_entry)
    x = [i+1 for i in range(len(yDist_hf))]
    assert(len(yDist_hf)==len(yDist_entry))
    
    ylab = 'Average Frequency'
    xlab = 'Day'
    legend1 = 'Headfix/Mouse/Day'
    legend2 = 'Entry/Mouse/Day'
    
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
        tit = str(tag)+' - '+action1+ ' to '+action2
        xlab = 'Time between headfixes'
        plt.title(tit)
        plt.ylabel('Frequency')
        plt.xlabel(xlab)
        width = 0.5 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()
        plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')
        
        fig, ax = plt.subplots()
                
        hist, bins = np.histogram(timesbetween_cutoff, bins=bin_no)
        tit = str(tag)+' - '+action1+ ' to '+action2 + ' after cutoff'
        xlab = 'Time spent in chamber'
        plt.title(tit)
        plt.ylabel('Frequency')
        plt.xlabel(xlab)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()
        plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')
        
    return [timesbetweens,timesbetweens_cutoff]                                   

def hists_for_selected_mice(action1,action2,bin_no,selected_mice,cut_off=None):
    """Plots histrograms of intervals between action1 and action2 for selected mice
    with bin_no bins and doesn't display any values above cut_off
    returns the interval times and the interval times above the cut_off"""
    timesbetweens = []
    timesbetweens_cutoff = []

    # Get data for all selected mice and add to lists
    for tag in selected_mice:
        fig, ax = plt.subplots()
        m = Mouse(tag,cfg.MICE_GROUPS,current_dat,cfg.BIN_TIME)
        timesbetween = m.get_between_actions_dist(action1,action2)
        # Get those too far right
        timesbetween_cutoff = [i for i in timesbetween if i >= cut_off]
        # Get rid of the ones too far to the right
        if cut_off != None:
            timesbetween = [i for i in timesbetween if i < cut_off]
        timesbetweens =timesbetweens+(timesbetween)
        timesbetweens_cutoff = timesbetweens_cutoff+(timesbetween_cutoff)


    hist, bins = np.histogram(timesbetweens, bins=bin_no)
    tit = str(selected_mice)+' - '+action1+ ' to '+action2
    xlab = 'Time between headfixes'
    plt.title(tit)
    plt.ylabel('Frequency')
    plt.xlabel(xlab)
    width = 0.5 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
    plt.savefig(cfg.OUTPUT_LOC+tit+" "+xlab+".png", bbox_inches='tight')

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

    return [timesbetweens,timesbetweens_cutoff]


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
        


#### UNCOMMENT TO GET GRAPHS ###
#for tag in cfg.TAGS:
#    plot_time_between_actions_for_tag(tag,cfg.OUTPUT_LOC,'entry','exit',current_dat,cfg.BIN_TIME)
#    plot_time_between_actions_for_tag(tag,cfg.OUTPUT_LOC,'reward0','check+',current_dat,cfg.BIN_TIME)

#for k in cfg.MICE_GROUPS.keys():
#    plot_results_for_tags(cfg.MICE_GROUPS[k],cfg.OUTPUT_LOC,k)
#
#plot_results_for_tags(cfg.TAGS,cfg.OUTPUT_LOC,'All Mice')

#[timesbetweens,timesbetweens_cutoff] = hists_that_tim_likes_for_bokeh('entry','exit',20,600)
#[timesbetweens,timesbetweens_cutoff] = hists_that_tim_likes_for_bokeh('reward0','check+',20,600)

#hists_for_selected_mice('entry', 'exit', 20, cfg.TAGS, 600)
[timesbetweens,timesbetweens_cutoff] = hists_for_selected_mice('reward0', 'check+', 20, cfg.TAGS, 600)


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

#global_stats()



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