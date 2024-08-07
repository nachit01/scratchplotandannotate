import pandas as pd
import matplotlib.pyplot as plt
from Front import Front
import os
from pathlib import Path
import shutil
import numpy  as np
class FrontCVData:
    def __init__(self,rootdatapath=r"evo_images_CSV",imeistxtgardesdict=None,mergedfilename=r"merged_front_data.csv",grades=["A","B","C","D"]):
        self.rootdatapath = rootdatapath
        if imeistxtgardesdict is None:
            self.imeistxtgardesdict = {'A': rootdatapath+r"\imeis_grades_txt_files\Front_grade_A_imeis.txt",
                                       'B': rootdatapath+r"\imeis_grades_txt_files\Front_grade_B_imeis.txt",
                                       'C': rootdatapath+r"\imeis_grades_txt_files\Front_grade_C_imeis.txt",
                                       'D': rootdatapath+r"\imeis_grades_txt_files\Front_grade_D_imeis.txt"
                                      }
        else:
            self.imeistxtgardesdict = imeistxtgardesdict
        self.mergedfilename = rootdatapath+r"\\" +mergedfilename
        self.grades = grades

    def getimeisfromtxt(self, grade="B"):
        file = open(self.imeistxtgardesdict[grade], "r")
        content = file.read()
        imeilist = content.splitlines()
        #remove duplicates
        imeilist = list(set(imeilist))
        #remove space
        imeilist = set([imei.strip() for imei in imeilist])
        file.close()
        return list(imeilist)

    def getimeifolders(self,grade = "B") -> list[str]:
        imeis = self.getimeisfromtxt(grade)
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
    def mergefrontdataonegrade(self,grade="B",):
        dfmerged = pd.DataFrame()
        #get dirs list out depending on imeis in imeistxt
        imeifolderslist  =  self.getimeifolders(grade)
        #create list of Fronts from the given imeis
        fronts = []
        for imeifolder in imeifolderslist:
            #create fronts. creates also csv new in __init__
            front = Front(csvfile=f"{imeifolder}\\Front.csv",imagepath=f"{imeifolder}\\Display.jpg")
            front.annotateFront()
            fronts.append(front)


        #append data to a new CSV file by region D1..D9. add a column "imei"
        for front in fronts:
            imeifrompath=str(Path(front.csvfile).parent).split('\\')[-1]
            front.dfcsvdata.insert(0,column="imei",value=imeifrompath)
            # # add grade B column
            front.dfcsvdata.insert(1, column="grade", value=grade)
            # add grade B column
            #adding D1...D9
            dfmerged = pd.concat([dfmerged,front.dfcsvdata.iloc[:9]],ignore_index=True)

        for indexfromd10toenddf,_ in fronts[0].dfcsvdata.iloc[9:].iterrows():
            #D10...to end
            newdf = pd.DataFrame([front.dfcsvdata.iloc[indexfromd10toenddf] for front in fronts])
            dfmerged = pd.concat([dfmerged, newdf],ignore_index=True)
        return  dfmerged

    def mergefrontdataallgivengrades(self,mergedfilename=r"evo_images_CSV\merged_front_data.csv"):
        dfmerged = pd.DataFrame()
        #merge all given grades into one DataFrame
        for grade in self.grades:
            dfmerged  = pd.concat([dfmerged,self.mergefrontdataonegrade(grade)],ignore_index=True)
        dfmerged.to_csv(self.mergedfilename,index=False, header=True)


    def plotfrontmergeddata(self,mergedfilename=r"evo_images_CSV\merged_front_data.csv"):
        #region names
        d1d9regions = [f"D{i}" for i in range(1,10)]
        #areas names
        areanames = [f"a{i}" for i in range(1, 11)]

        #read all grades merged data
        dfmergeddatagardeB = pd.read_csv(mergedfilename)

        #get only D1..D9 data
        dfd1d9data = pd.DataFrame([row for _,row in dfmergeddatagardeB.iterrows() if row['region'].strip() in d1d9regions]).reset_index(drop=True)
        #flatten
        dfd1d9dataflattned = pd.melt(frame=dfd1d9data,id_vars=['imei','grade','region'] ,value_vars=areanames, var_name='areas', value_name='values')
        #replace zeros with nan to not plot them
        dfd1d9dataflattnednonzeroes =  pd.DataFrame([row for _,row in dfd1d9dataflattned.iterrows() if row['values'] > 0]).reset_index(drop=True)

        # get ranges
        dfgradeB = pd.DataFrame([row for i,row in dfd1d9dataflattnednonzeroes.iterrows() if row['grade'] == 'B'])
        # dfgradeC =
        idxmin = dfd1d9dataflattnednonzeroes['values'].idxmin()
        idxmax = dfd1d9dataflattnednonzeroes['values'].idxmax()
        print(f"upperlimit Grade :\n{dfd1d9dataflattnednonzeroes.iloc[idxmax]}")
        print(f"lowerlimit Grade :\n{dfd1d9dataflattnednonzeroes.iloc[idxmin]}")

        #plot
        dfd1d9dataflattnednonzeroes.plot(kind="scatter",x='values',y='grade',grid=True,legend=True,c='blue',s=50)
        plt.title("Evo3 Grading Classification")
        # Set x and y axis limits
        plt.xlim(0, 15000)  # Set limits for x-axis

        plt.grid(True)
        plt.show()


    def saveannotatedimagesbygrade(self,grade="B"):
        gradeimeis = self.getimeisfromtxt(grade)
        pathsbygradedirs = self.getimeifolders(grade)
        pathannotatedimagesbygrade = Path(self.rootdatapath+f"/all_annotated_images/{grade}")
        #create saving folders by grade
        pathannotatedimagesbygrade.mkdir(parents=True,exist_ok=True)

        annotatedimagedefaultname = "Display_annotated.jpg"
        for dir in pathsbygradedirs:
            imagename = str(Path(dir).name + "Display_annotated.jpg")
            source = dir + f"/{annotatedimagedefaultname}"
            destination= str(pathannotatedimagesbygrade) + f"/ - {imagename}"
            shutil.copy2(source,destination)

    def saveallannotatedimagesbygrade(self):
        for grade in self.grades:
            self.saveannotatedimagesbygrade(grade=grade)















