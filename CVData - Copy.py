import pandas as pd
import matplotlib.pyplot as plt
from Front import Front
import os
from pathlib import Path
import numpy  as np
class CVData:
    def __init__(self,directorydata=""):
        print()


    def getimeisfromtxt(self,imeistxt=r"evo_images_CSV\Front_grade_B_imeis.txt"):
        file = open(imeistxt, "r")
        content = file.read()
        imeilist = content.splitlines()
        #remove duplicates
        imeilist = list(set(imeilist))
        #remove space
        imeilist = [imei.strip() for imei in imeilist]
        file.close()
        return imeilist

    def getimeifolders(self,imeistxt=r"evo_images_CSV\Front_grade_B_imeis.txt"):
        imeis = self.getimeisfromtxt(imeistxt)
        #get all dirs under data root dir
        datadirectory = Path(r"evo_images_CSV\data")
        alldris = [dir for dir in datadirectory.iterdir()]
        subdirs = [dir  for imei in imeis for dir in alldris if imei in dir.name]

        # Sort directories by last modified time
        sorteddirectories = sorted(subdirs, key=lambda x: os.path.getmtime(x),reverse=True)
        sorteddirectories = [str(dir) for dir in sorteddirectories] #convert from WindowsPAth to str
        #remove multiple runs. keep latest
        pdseriessorteddirectories = pd.Series(sorteddirectories)
        imeisubdirscountdict = {imei: int(pdseriessorteddirectories.str.contains(imei).sum()) for imei in imeis}
        for imei, count in imeisubdirscountdict.items():
            if count > 1:
                sorteddirectories.remove(f"{datadirectory}\\{imei}")
                for j in range(count-2):
                    sorteddirectories.remove(f"{datadirectory}\\{imei} - {j}")
        return sorteddirectories


####D1 crack not read because it has a weird length, ask toshika.
    def mergingfrontdata(self,imeistxt=r"evo_images_CSV\Front_grade_B_imeis.txt",mergedfilename=r"evo_images_CSV\merged_front_data.csv"):
        #get dirs list out depending on imeis in imeistxt
        imeifolderslist  =  self.getimeifolders(imeistxt)
        #create list of Fronts from the given imeis
        fronts = []
        for imeifolder in imeifolderslist:
            #create fronts. creates also csv new in __init__
            fronts.append(Front(csvfile=f"{imeifolder}\\Front.csv",imagepath=f"{imeifolder}\\Display.jpg"))

        dfmerged = pd.DataFrame()
        #append data to a new CSV file by region D1..D9. add a column "imei"
        for front in fronts:
            imeifrompath=str(Path(front.csvfile).parent).split('\\')[-1]
            front.dfcsvdata.insert(0,column="imei",value=imeifrompath)
            # # add grade B column
            front.dfcsvdata.insert(1, column="grade", value='B')
            # add grade B column
            # front.dfcsvdata.insert(1, column="grade", value='B')
            #adding D1...D9
            dfmerged = pd.concat([dfmerged,front.dfcsvdata.iloc[:9]],ignore_index=True)

        for indexfromd10toenddf,_ in fronts[0].dfcsvdata.iloc[9:].iterrows():
            #D10...to end
            newdf = pd.DataFrame([front.dfcsvdata.iloc[indexfromd10toenddf] for front in fronts])
            dfmerged = pd.concat([dfmerged, newdf],ignore_index=True)
        #save to csv
        dfmerged.to_csv(mergedfilename,index=False, header=True)

    def plotfrontmergeddata(self,mergedfilename=r"evo_images_CSV\merged_front_data.csv"):
        dfmergeddatagardeB = pd.read_csv(mergedfilename)
        d1d9regions = [f"D{i}" for i in range(1,10)]
        dfd1d9data = pd.DataFrame([row for _,row in dfmergeddatagardeB.iterrows() if row['region'].strip() in d1d9regions]).reset_index(drop=True)
        areanames = [ f"a{i}" for i in range(1,11) ]
        dfd1d9dataflattned = pd.melt(frame=dfd1d9data,id_vars=['imei','grade','region'] ,value_vars=areanames, var_name='areas', value_name='values')
        #replace zeros with nan to not plot them
        dfd1d9dataflattnednonzeroes =  pd.DataFrame([row for _,row in dfd1d9dataflattned.iterrows() if row['values'] > 0]).reset_index(drop=True)
        # get ranges
        idxmin = dfd1d9dataflattnednonzeroes['values'].idxmin()
        idxmax = dfd1d9dataflattnednonzeroes['values'].idxmax()
        print(f"upperlimit Grade B :\n{dfd1d9dataflattnednonzeroes.iloc[idxmax]}")
        print(f"lowerlimit Grade B :\n{dfd1d9dataflattnednonzeroes.iloc[idxmin]}")

        #plot
        dfd1d9dataflattnednonzeroes.plot(kind="scatter",x='values',y='grade',grid=True,legend=True,c='blue',s=50)
        plt.grid(True)
        plt.show()













