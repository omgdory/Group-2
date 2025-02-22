#CS 472 
#NSHE ID: 5004634201     Franklin La Rosa Diaz
def checkFile():
    while True:
        try:
            fname = input("Enter the file name: \n")
            iFile = open(fname)
        except IOError:
            print("File not accessible. Try again.\n")
            continue
        else:
            iFile.close()
            print("File accepted. Loading...\n")
            return fname

def readFile(fname):
    with open(fname, 'r') as iFile:
        for line in iFile:
            singleLine = " "
            singleLine = line
            DNA_to_RNA = replaceT(singleLine)
            print(DNA_to_RNA, "\n")
    iFile.close()

def replaceT(singleLine):
    singleLine = singleLine.replace('T', 'U')
    return singleLine
   
    

#Actual Program
fname = checkFile()
readFile(fname)