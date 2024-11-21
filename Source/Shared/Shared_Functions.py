from Libraries import *

def getCurrrentDir():
    current_directory = Path.cwd()
    return current_directory
    
def getPrarentDir():
    current_directory = Path.cwd()
    return current_directory.parent

def getGranDir():
    current_directory = Path.cwd()
    return current_directory.parent.parent

def getDataFrame(source_path):
    return pd.read_csv(source_path)
