import pandas as pd
import matplotlib.pyplot as plt
from Front import Front
import os
from pathlib import Path
import shutil
import numpy  as np
from Side import Side
import mplcursors

class AllPhonesSidesCVData:
    GRADES = ["A","B","C","D"]
    SIDES = ['front','back','left','right','top','bottom']
    CSVFILENAMESBYSIDE ={"front":"Front.csv","back":"Back.csv","left":"long.csv","right":"long.csv","top":"Short.csv","bottom":"Short.csv"}
    IMAGESFILENAMESBYSIDE ={"front":"Display.jpg","back":"Housing.jpg","left":"Left.jpg","right":"Right.jpg","top":"Top.jpg","bottom":"Bottom.jpg"}

    D1D9REGIONS = [f"D{i}" for i in range(1, 10)]  # front
    H1H9REGIONS = [f"H{i}" for i in range(1, 10)]  # back
    L1L7REGIONS = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7 Left SIM']  # left
    R1R5REGIONS = [f"R{i}" for i in range(1, 6)]  # right
    T1R4REGIONS = [f"T{i}" for i in range(1, 5)]  # top
    B1B3REGIONS = [f"B{i}" for i in range(1, 4)]  # bottom
    REGIONGROUPSDICT ={"front":D1D9REGIONS,"back":H1H9REGIONS,"left":L1L7REGIONS,"right":R1R5REGIONS,"top":T1R4REGIONS,
                       "bottom":B1B3REGIONS}
    PATHALLANNOTATEDIMAGES = Path(r"all_annotated_images")
    PATHMANUALLYGRADEDCSV = Path(r"manually_graded_phones.csv")

    def __init__(self,rootdatapath=r"evo_images_CSV",imeistxtgardesdict=None,mergedfilename=r"merged_front_data.csv",grades=None):
        self.rootdatapath = Path(".").cwd() / rootdatapath
        self.mergedfilename = rootdatapath+r"\\" +mergedfilename
        self.grades = AllPhonesSidesCVData.GRADES if grades == None else grades
        self.txtmanualgradingfiles = self.rootdatapath / r"imeis_grades_txt_files"
        self.allsidesdict={"front":[],"back":[],"left":[],"right":[],"top":[],
                       "bottom":[]}
        self.wheretosavemergedsidesdict ={"front":self.rootdatapath / "front_all_phones_merged.csv",
                                          "back":self.rootdatapath / "back_all_phones_merged.csv",
                                          "left":self.rootdatapath / "left_all_phones_merged.csv",
                                          "right":self.rootdatapath / "right_all_phones_merged.csv",
                                          "top":self.rootdatapath / "top_all_phones_merged.csv",
                                            "bottom":self.rootdatapath / "bottom_all_phones_merged.csv"}

        self.wheretosavemergedsidesLSDSdict = {"front": self.rootdatapath / "lsdsmerged"/"front_all_lsds_merged.csv",
                                           "back": self.rootdatapath / "lsdsmerged"/"back_all_lsds_merged.csv",
                                           "left": self.rootdatapath / "lsdsmerged"/"left_all_lsds_merged.csv",
                                           "right": self.rootdatapath / "lsdsmerged"/"right_all_lsds_merged.csv",
                                           "top": self.rootdatapath / "lsdsmerged"/"top_all_lsds_merged.csv",
                                           "bottom": self.rootdatapath / "lsdsmerged"/"bottom_all_lsds_merged.csv"}
        self.populateallphonessides()


    def populateallphonessides(self):

        for side in AllPhonesSidesCVData.SIDES:
            for grade in AllPhonesSidesCVData.GRADES:
                bysidebygradetxtimeispath = self.txtmanualgradingfiles / side / f"{side}_grade_{grade}_imeis.txt"
                sidegradeimeislist = self.getimeisfromtxt(bysidebygradetxtimeispath)
                sidegradeimeislist = self.cleanimeilist(sidegradeimeislist)
                for imeigrade in sidegradeimeislist:
                    newside = Side(sidename=side,rootpath=self.rootdatapath,sideimei=imeigrade,
                                   sidecsvfile= AllPhonesSidesCVData.CSVFILENAMESBYSIDE[side],
                                   sideimagename = AllPhonesSidesCVData.IMAGESFILENAMESBYSIDE[side]
                                   ,sideregiongroup=AllPhonesSidesCVData.REGIONGROUPSDICT[side],manualgrade=grade)
                    self.allsidesdict[side].append(newside)


    def getimeisfromtxt(self,sidepath=None):
        file = open(sidepath, "r")
        content = file.read()
        imeilist = content.splitlines()
        #remove duplicates
        imeilist = list(set(imeilist))
        #remove space
        imeilist = set([imei.strip() for imei in imeilist])
        file.close()

        return list(imeilist)

    def cleanimeilist(self,imeis = None):
        #run over data folder. chenk multiple imei runs. keep latets
        # get all dirs under data root dir
        datadirectory = self.rootdatapath / "data"
        alldris = [dir for dir in datadirectory.iterdir()]
        subdirs = [dir for imei in imeis for dir in alldris if imei in dir.name]

        # Sort directories by last modified time
        sorteddirectories = sorted(subdirs, key=lambda x: os.path.getmtime(x), reverse=True)
        sorteddirectories = [str(dir) for dir in sorteddirectories]  # convert from WindowsPAth to str
        # remove multiple runs. keep latest
        pdseriessorteddirectories = pd.Series(sorteddirectories)
        imeisubdirscountdict = {imei: int(pdseriessorteddirectories.str.contains(imei).sum()) for imei in imeis}
        for imei, count in imeisubdirscountdict.items():
            if count > 1:
                sorteddirectories.remove(f"{datadirectory}\\{imei}")

                for j in range(count - 2):
                    sorteddirectories.remove(f"{datadirectory}\\{imei} - {j}")
        cleanedimeis = [Path(dir).name for dir in sorteddirectories ]
        return cleanedimeis

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

    def mergeeachsidetoitscsvfile(self):
        #front .....bottom side
        for sidename in AllPhonesSidesCVData.SIDES:
            df = pd.DataFrame()
            sidelist = self.allsidesdict[sidename]
            #sides in list of AllPhonesSidesCVData
            for side in sidelist:
                side.annotateside()
                df = pd.concat([df,side.dfsidecsvdata],ignore_index=True)
            df.to_csv(self.wheretosavemergedsidesdict[sidename],index=False, header=True)

    def mergeelsdstocsvfile(self):
        #front .....bottom side
        for sidename in AllPhonesSidesCVData.SIDES:
            sidelsdsdata = []
            #get all front Sides created
            sidelist = self.allsidesdict[sidename]
            #sides in list of AllPhonesSidesCVData
            for side in sidelist:
                rowdata = {
                    'imei': side.sideimei,
                    'grade': side.manualgrade,
                    'lscount': side.sidelightscratchescount,
                    'dscount': side.sidedeepscratchescount,
                }
                sidelsdsdata.append(rowdata)
            #create df
            df = pd.DataFrame(sidelsdsdata)
            df.to_csv(self.wheretosavemergedsidesLSDSdict[sidename],index=False, header=True)




    def plotareaallsidesmergeddata(self,sides=None):
        if sides == None:
            sides = AllPhonesSidesCVData.SIDES

        for side in sides:
            #read all grades merged data for side
            dfmergeddatagarde = pd.read_csv(self.wheretosavemergedsidesdict[side])
            #get side day
            sideregiondata = pd.DataFrame([row for _,row in dfmergeddatagarde.iterrows() if row['region'].strip() in
                                       AllPhonesSidesCVData.REGIONGROUPSDICT[side]]).reset_index(drop=True)

            #flatten
            sideregiondataflattned = pd.melt(frame=sideregiondata,id_vars=['imei','grade','region'] ,
                                             value_vars=Side.AREASCOLUMNSNAMES, var_name='areas', value_name='values')
            #replace zeros with nan to not plot them
            sideregiondataflattnednonzeroes =  pd.DataFrame([row for _,row in sideregiondataflattned.iterrows() if row['values'] > 0]).reset_index(drop=True)


            #plot
            ax = sideregiondataflattnednonzeroes.plot(kind="scatter",x='values',y='grade',grid=True,legend=True,c='blue',s=50)
            plt.title(f"Side:{side}")

            # Add interactive cursors
            self.addinteractivehovertoplot(df=sideregiondataflattnednonzeroes,ax=ax,colimei="imei", colregion='region'
                                           , colareas='areas', colvalues='values')
        # Set x and y axis limits
        # plt.xlim(0, 15000)  # Set limits for x-axis

        plt.grid(True)
        plt.show()


    def plotlightdeepscracthescountsallsidesbygrade(self,sides=None):
        if sides == None:
            sides = AllPhonesSidesCVData.SIDES
            # sides = ['front']
        plotboxdict={}
        for side in sides:
            #get data for each side from its CSV merged file
            #read all grades merged data for side
            dflsds = pd.read_csv(self.wheretosavemergedsidesLSDSdict[side])

            # Replace zeros with NaN
            # Replace zeros with NaN without using inplace=True
            dflsds['lscount'] = dflsds['lscount'].replace(0, None)
            dflsds['dscount'] = dflsds['dscount'].replace(0, None)

            #plot
            # x1 and x2
            x1 = dflsds['lscount']
            x2 = dflsds['dscount']
            # Categorical data for the y-axis
            y = dflsds['grade']

            # Create a DataFrame
            df = pd.DataFrame({
                'grade': y,
                'lscount': x1,
                'dscount': x2,
            })

            # Create the plot
            # fig, ax = plt.subplots()
            fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 6))

            # Scatter plot for x1 with y shifted up
            for label in df['grade'].unique():
                #plot the lscount column by deviding grade example B to B LS light scratch
                subset = df[df['grade'] == label]
                #renaming grade B  for LScount to BLS grade
                subset['grade'] = subset['grade'].map(lambda y: f'{y} LS')
                ax.scatter(subset['lscount'], subset['grade'],
                           label=f'Light scratch', marker='o', alpha=0.7,c='green')
                # Plot the boxplot on the first subplot (ax1)
                dfbox1 = subset.rename(columns = {"lscount":f'{label} LS'})
                # dfbox1.boxplot(f'{label} LS',ax=ax2)
                plotboxdict[f'{label} LS'] = dfbox1[f'{label} LS']

                #plot the lscount column by deviding grade example B to B LS light scratch
                subset2 = df[df['grade'] == label]
                subset2['grade'] = subset2['grade'].map(lambda y: f'{y} DS')

                # renaming grade B  for LScount to BLS grade
                ax.scatter(subset2['dscount'], subset2['grade'],
                           label=f'Deep Scracth', marker='x', alpha=0.7,c='red')

                # Plot the boxplot on the first subplot (ax1)
                dfbox2 = subset.rename(columns={"dscount": f'{label} DS'})
                plotboxdict[f'{label} DS'] = dfbox2[f'{label} DS']
                #ax2 params
                ax2.set_title(r'Boxplot of \textbf{Different Categories}', fontsize=14)
                ax2.set_xlabel('grade')
                ax2.set_ylabel('count')

            dfbox = pd.DataFrame(plotboxdict)
            # Replace NaN values with 0 in the entire DataFrame
            dfbox.fillna(0,inplace=True)
            aux = dfbox.mask(dfbox==0)
            dfbox.mask(dfbox==0).boxplot(ax=ax2)

            #set plot
            ax.set_xlabel('Light / Deep Scratche counts')
            ax.set_ylabel('grade')

            #remove duplocate legends
            # Get current handles and labels
            handles, labels = ax.get_legend_handles_labels()
            # Update the legend with new labels
            ax.legend(handles, labels[:2], title='type of scratches')
            plt.title(f'deep/light scratches count per grade for {side.upper()}')
            plt.tight_layout()
            # Turn on the grid
            ax.grid(True)
        cursor = mplcursors.cursor(hover=True)
        cursor.connect(
            "add", lambda sel: sel.annotation.set_text(f'X: {sel.target[0]:.2f}'))
        plt.show()


    def addinteractivehovertoplot(self,df,ax,colimei, colregion, colareas, colvalues):
        # Add interactive cursors
        cursor = mplcursors.cursor(ax, hover=True)

        # Define a function to handle the annotation for each plot
        def create_on_add(df, colimei, colregion, colareas, colvalues):
            def on_add(sel):
                sel.annotation.set(text=f'imei:{df[colimei].iloc[sel.target.index]}\n'
                                        f'region:{df[colregion].iloc[sel.target.index]}\n'
                                        f'area:{df[colareas].iloc[sel.target.index]}\n'
                                        f'value:{df[colvalues].iloc[sel.target.index]}')
                sel.annotation.get_bbox_patch().set(fc="white")

            return on_add

        cursor.connect("add", create_on_add(df, "imei", 'region', 'areas', 'values'))

    def saveannotatedimagesbygrade(self,grade="B"):
        for sidename in AllPhonesSidesCVData.SIDES:
            if len(self.allsidesdict[sidename]) == 0:
                self.populateallphonessides()
            for i,side in enumerate(self.allsidesdict[sidename]):
                source = side.sidecurrentimeifolder /  side.sideannotatedimagename
                annotatedgradeimei = f"{side.sideannotatedimagename[:-4]}_{side.sideimei}_{side.manualgrade}{side.sideannotatedimagename[-4:]}"
                destination = self.rootdatapath / AllPhonesSidesCVData.PATHALLANNOTATEDIMAGES / annotatedgradeimei
                shutil.copy2(source, destination)

    def createimeistxtfromcsv(self):
        dfmanuallygradedcsv = pd.read_csv(self.rootdatapath / r"imeis_grades_txt_files" / AllPhonesSidesCVData.PATHMANUALLYGRADEDCSV)
        for side in AllPhonesSidesCVData.SIDES:
            for grade in AllPhonesSidesCVData.GRADES:
                bysidebygradetxtimeispath = self.txtmanualgradingfiles / side / f"{side}_grade_{grade}_imeis.txt"
                sideandgradeimeislist = dfmanuallygradedcsv[(dfmanuallygradedcsv[side] == grade)]['imei']
                sideandgradeimeislist.to_csv(bysidebygradetxtimeispath,sep='\t',index=False,header=False)
















