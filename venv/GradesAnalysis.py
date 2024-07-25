from pathlib import Path
import pandas as pd

class Grade:
    def __init__(self,rootdatapath=r"evo_images_CSV",,gradesdtatfoldername="data_grades",mergedfilename=r"merged_grades_data.csv"):
        self.rootdatapath = Path(".").cwd() / rootdatapath
        self.mergedgradesname = rootdatapath + r"\\" + mergedfilename
        self.datagradespath = self.rootdatapath / gradesdtatfoldername
        self.dfdatagrades = pd.DataFrame()

    def readallgradesvalues(self):
