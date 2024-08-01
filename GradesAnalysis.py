from pathlib import Path

import mplcursors
import pandas as pd
import matplotlib.pyplot as plt
from  CVDataAnalysisi import AllPhonesSidesCVData

class Grade:

    IGNORE = ['EVO3 Grade Data:','COMMUNICATIONS TEST DESIGN INC.']

    HEADER = ['SCANNED ID','MODEL','COLOR','Front Value','Front Grade',
              'Back Value','Back Grade','Left Value','Left Grade','Right Value','Right Grade',
              'Top Value','Top Grade','Bottom Value','Bottom Grade','Final Value','Final Grade']

    EVOVSMANUALCSVNAME = Path().cwd() / "evo_images_CSV" / "evo_vs_manual.csv"

    def __init__(self,rootdatapath=r"evo_images_CSV",gradesdtatfoldername="data_grades",mergedfilename=r"merged_grades_data.csv"):
        self.rootdatapath = Path(".").cwd() / rootdatapath
        self.mergedgradesname = rootdatapath + r"\\" + mergedfilename
        self.datagradespath = self.rootdatapath / gradesdtatfoldername
        self.dfdatagrades = pd.DataFrame()

    def readallgradesvalues(self):
        # Get a list of all .txt files in the directory
        txt_files = self.datagradespath.glob('*.txt')
        # Read all .txt files into a list of DataFrames
        dfs = []
        for txt_file in txt_files:
            df = pd.read_csv(txt_file, delimiter='\t')  # Adjust delimiter as needed
            dfs.append(df)

        # Optionally, concatenate all DataFrames into a single DataFrame
        all_data = pd.concat(dfs, ignore_index=True)
        all_data.columns=['data']
        #clean

        print(all_data['data'])
        dfcleaned = all_data[~all_data['data'].isin(self.IGNORE)]

        #format into table
        # Create dictionary with keys and default value None
        rowdict = {}
        dfgrades = pd.DataFrame(columns = self.HEADER)
        for idx,row in dfcleaned.iterrows():
            key,value = row[0].split(':')
            key= key.strip()
            value = value.strip()
            if key == self.HEADER[0] and idx != 1:
                newrowdf = pd.DataFrame([rowdict])
                dfgrades = pd.concat([dfgrades, newrowdf], ignore_index=True)
                rowdict={} #start new row

            rowdict[key] = value
        self.dfdatagrades = dfgrades
        self.dfdatagrades.to_csv(self.mergedgradesname,index=False)

    def pltogradesbyside(self,sides=None):
        if sides == None:
            sides = AllPhonesSidesCVData.SIDES
        # fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        # read all grades merged data for side
        dfmergeddatagarde = pd.read_csv(self.mergedgradesname)
        for side in sides:
            valuecolumn = side.capitalize() + " Grade"
            gradecolumn = side.capitalize() + " Value"
            #plot
            ax = dfmergeddatagarde.plot(kind="scatter",x=gradecolumn,y= valuecolumn,grid=True,legend=True,c='blue',s=50)
            plt.title(f"Side Grade Values:{side}")
            # Add interactive cursors
            self.addinteractivehovertoplot(df=dfmergeddatagarde,ax=ax,colimei="SCANNED ID", colvalues=valuecolumn,
                                           colgrade=gradecolumn)
        plt.grid(True)
        plt.show()


    def addinteractivehovertoplot(slef,df,ax,colimei, colvalues,colgrade):
        # Add interactive cursors
        cursor = mplcursors.cursor(ax, hover=True)

        # Define a function to handle the annotation for each plot
        def create_on_add(df, colimei, colgrade, colvalues):
            def on_add(sel):
                sel.annotation.set(text=f'imei:{df[colimei].iloc[sel.target.index]}\n'
                                        f'grade:{df[colgrade].iloc[sel.target.index]}\n'
                                        f'value:{df[colvalues].iloc[sel.target.index]}')
                sel.annotation.get_bbox_patch().set(fc="white")

            return on_add

        cursor.connect("add", create_on_add(df, colimei, colgrade, colvalues))

    def evovsmanualgradescsv(self):
        dfevograding = pd.read_csv(self.mergedgradesname)
        dfmanuallygrade = pd.read_csv(Path(".").cwd() / "evo_images_CSV" /"imeis_grades_txt_files"
                                      / AllPhonesSidesCVData.PATHMANUALLYGRADEDCSV)
        dfevovsmnual = dfevograding

        for side in AllPhonesSidesCVData.SIDES:
            columntoinsertafter = side.capitalize() + " Grade"
            position = dfevovsmnual.columns.get_loc(columntoinsertafter) + 1
            # Initialize an empty list to store the results
            values = []

            # Iterate over each value in df1['col1']
            for value in dfevograding[Grade.HEADER[0]]:
                # Check if the value exists in df2['col2']
                match = dfmanuallygrade[dfmanuallygrade['imei'] == value]
                if not match.empty:
                    # Retrieve the value from df2['col3']
                    values.append(match[side].iloc[0])
                else:
                    # If no match found, append None or a default value
                    values.append(None)

            dfevovsmnual.insert(loc=position,column=side+" manual",value=values)
            dfevovsmnual.to_csv(Grade.EVOVSMANUALCSVNAME,index=False, header=True)


    def plotmismatches(self):

        sides = AllPhonesSidesCVData.SIDES
            # fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            # read all grades merged data for side
        dfevovsman = pd.read_csv(Grade.EVOVSMANUALCSVNAME)


        for side in sides:
            gradeevo = side.capitalize() + " Grade"
            valuecolumn = side.capitalize() + " Value"
            grademan = side + " manual"

            #get only mismatches
            filt = (dfevovsman[gradeevo] != dfevovsman[grademan])
            print(dfevovsman[grademan].iloc[1])
            print(dfevovsman[gradeevo].iloc[1])
            sidemismatch = dfevovsman[filt]

            # plot
            ax = sidemismatch.plot(kind="scatter", x=valuecolumn, y= gradeevo, grid=True, legend=True, c='blue',
                                        s=50)
            plt.title(f"Side Grade Mismatch:{side}")

            # Add interactive cursors
            self.addinteractivemismatch(df=sidemismatch, ax=ax, colimei="SCANNED ID", colvalues=valuecolumn,
                                           colgrade=gradeevo,colmangrade = grademan)
        plt.grid(True)
        plt.show()


    def addinteractivemismatch(slef,df,ax,colimei, colvalues,colgrade,colmangrade):
        # Add interactive cursors
        cursor = mplcursors.cursor(ax, hover=True)

        # Define a function to handle the annotation for each plot
        def create_on_add(df, colimei, colgrade, colvalues,colmangrade):
            def on_add(sel):
                sel.annotation.set(text=f'imei:{df[colimei].iloc[sel.target.index]}\n'
                                        f'mangrade:{df[colmangrade].iloc[sel.target.index]}\n'
                                        f'evograde:{df[colgrade].iloc[sel.target.index]}\n'
                                        f'value:{df[colvalues].iloc[sel.target.index]}')
                sel.annotation.get_bbox_patch().set(fc="white")

            return on_add

        cursor.connect("add", create_on_add(df, colimei, colgrade, colvalues,colmangrade))



