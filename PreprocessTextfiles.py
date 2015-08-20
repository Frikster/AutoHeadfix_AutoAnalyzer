"""Class holding all attributes related to preprocessing textFiles"""

class PreprocessTextfiles:     
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
    
    def __init__(self, workingDir, foldersToIgnore):
        self.workingDir = workingDir
        self.foldersToIgnore = foldersToIgnore 
    
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
    
    # Return a dictionary that has each path of each text file as the key to a matrix that contains all the lines of each text file - duplicates removed, ordered by textFile startseshes
def importTextsToDict(workingDir):
    txtList = getAllTextLocs(workingDir)
    # Remove all the paths that are subdirectories of the ignore folders
    for i in range(len(foldersToIgnore)):
        txtList=[x for x in txtList if not (foldersToIgnore[i] in x)]
    
    # Lines contains the lines from each text file where lines[i] contains all the lines of the i'th text file
    ListofMat=importTextsToListofMat(txtList)           
    lines = zip(*ListofMat)[0]
    textFileLoc = zip(*ListofMat)[1]         
    
    # Remove the text files that have the same start time as another     
    startSeshes = []
    for i in range(len(lines)):
        startSeshes.append(lines[i][0][timeCol])
    
    def equalToAnother(elem):
        return (startSeshes.count(elem) > 1)
        
    def NOTequalToAnother(elem):
        return (startSeshes.count(elem) == 1)  
    
    # Indices of all text files that are duplicates of another and those that are unique
    equalStartInd=map(equalToAnother,startSeshes)
    notEqualStartInd = map(NOTequalToAnother, startSeshes)
    
    # Retrieve text file names and start times that have duplicates
    textFileEquals=np.asarray(textFileLoc)[np.asarray(equalStartInd)]
    startTimeEquals=np.asarray(startSeshes)[np.asarray(equalStartInd)]
    
    # Sort these text files by start time  
    textFileEquals = sort_X_BasedOn_Y_BeingSorted(textFileEquals,startTimeEquals)
    startTimeEquals = sort_X_BasedOn_Y_BeingSorted(startTimeEquals,startTimeEquals)
    
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
    textFileLoc = np.asarray(textFileLoc)[np.asarray(notEqualStartInd)]
    textFileLoc = textFileLoc.tolist()
    startSeshes = np.asarray(startSeshes)[np.asarray(notEqualStartInd)]
    startSeshes = startSeshes.tolist()
        
    # Right, and now add only one of each of the duplicates back to 'lines'
    #[linesOneDup,textFileLocOneDup]=importTextsToListofMat(textFileEqualsOnlyOne) 
    ListofMat=importTextsToListofMat(textFileEqualsOnlyOne)           
    linesOneDup = zip(*ListofMat)[0]
    textFileLocOneDup = zip(*ListofMat)[1]
    
    for linesToAdd in linesOneDup:
        lines.append(linesToAdd)
    for locToAdd in textFileLocOneDup:
        textFileLoc.append(locToAdd)  
    
    # Sort the text file contents and names by startSeshes
    textFileLoc = sort_X_BasedOn_Y_BeingSorted(textFileLoc,startSeshes)
    lines = sort_X_BasedOn_Y_BeingSorted(lines,startSeshes)
    
    # Add these two to a dictionary
    textDict = collections.OrderedDict(zip(textFileLoc, lines))                           
    return textDict