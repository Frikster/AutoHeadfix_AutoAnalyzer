""" Define globals used by everyone.

args:
    working_dir (str): Full path of the directory that contains all textFiles to be analyzed
    folders_to_ignore ([str]): List of folders that are ignored. Only the folders name is required, not each one's full path
    output_loc (str): where any analysis is outputted to
    bin_time (int): the time in seconds of bins for the graph (86400 = seconds in a day)
    """
from datetime import datetime

# Column Numbers
TAG_COL = 0
TIME_COL = 1
DATE_COL = 2
ACTION_COL = 3

MICE_GROUPS = {
    'EL':[2015050115,1312000377,1312000159,1302000245,1312000300],
    'EP': [1302000139,2015050202,1412000238],
    'AB': [1312000592,1312000573,1312000090]
}
TAGS = []
for i in range(len(MICE_GROUPS.items())):
    TAGS.extend(MICE_GROUPS.items()[i][1])

DIR_WITH_TEXTFILES = "T:/AutoHeadFix/"
FOLDERS_TO_IGNORE = ["Old and or nasty data goes here"]
OUTPUT_LOC = "C:\\Users\\user\\Downloads\\"
# BIN_TIME = 86400
BIN_TIME = 3600

# This says headfixing has occurred
HEADFIX_STR='reward0'
ENTRY_STR='entry'


# Define the time from when we start looking at textfiles
#ABSOLUTE_START_TIME = "2015-06-13 01:00:00.000000"
ABSOLUTE_START_TIME = "2015-06-13 01:00:00.000000"
ABSOLUTE_START_TIME = datetime.strptime(ABSOLUTE_START_TIME, '%Y-%m-%d %H:%M:%S.%f')
