import pandas as pd
import re
import utils
import cv2
import matplotlib.pyplot as plt
from pathlib import Path




class Side:
    DATAFOLDERNAME = r"data"
    AREASCOLUMNSNAMES = [f"a{i}" for i in range(1, 11)]

    def __init__(self,sidename=None,rootpath=r"evo_images_CSV",sideimei=None,sidecsvfile= r"Front.csv",sideimagename = r"Display.jpg",sideregiongroup=None,manualgrade="B"):
        self.sidename = sidename
        self.sideregiongroup = sideregiongroup
        self.sidecsvfilename =sidecsvfile
        self.sideimagename = sideimagename
        self.siderootpath = Path(".").cwd() / rootpath
        self.sideimei = sideimei
        self.sidecsvfilenew = f"{self.sidecsvfilename[:-4]}_new{self.sidecsvfilename[-4:]}"
        self.sideannotatedimagename = f"{self.sideimagename[:-4]}_annotated{self.sideimagename[-4:]}"
        self.sidecurrentimeifolder = self.siderootpath / Side.DATAFOLDERNAME / self.sideimei
        self.correctcsv()
        # TODO if rerion is left right or top or bottom, get only L... R.... T... B... otherwise annotate Left will take values of
        # TODO right when annotating
        # TODO filter for Lx Rx
        self.dfsidecsvdata = pd.read_csv( self.sidecurrentimeifolder/ self.sidecsvfilenew, on_bad_lines='warn')
        self.dfsidecsvdata.insert(0, column="imei", value=self.sideimei)
        # # add grade B column
        self.dfsidecsvdata.insert(1, column="grade", value=manualgrade)
        self.manualgrade = manualgrade

    def correctcsv(self):
        # Open the file in read mode
        with open(self.sidecurrentimeifolder / self.sidecsvfilename, 'r') as file:
            # Read the entire content of the file
            content = file.read()

        cells_raw = re.split(r'[,\n]', content)
        #remove first ans last cell
        cells = cells_raw[1:-3]
        #remove empty cells
        cleaned_cells = [c for c in cells if (c!="")]
        #creating rows
        rows_delimiters =["Scratch","Shape","Crack"]
        rows=[]
        row = ""
        for i,c in enumerate(cleaned_cells):
            if c in rows_delimiters:
                if i > 2:
                    rows.append(row)
                row = ""
                row = c.strip() +','
            else:
                row += c.strip() +','
        #append last row of the loop
        rows.append(row)

        # add header for csv file
        header = ["type,","region,",] + ['a' + str(i)+',' for i in range(1, 11)]
        for i in range(1,11):
            header.append(f"x{i},")
            header.append(f"y{i},")
        rows.insert(0,"".join(header))

        #replace , by \n at the end of each row for csv format
        for i in range(len(rows)):
            if len(rows[i]) > 0:
                rows[i] = rows[i][:-1] + '\n'
        #save as corrected csv
        correctedcsvpath = self.sidecurrentimeifolder / self.sidecsvfilenew
        text =   "".join(rows)
        with open(str(correctedcsvpath), mode='w') as file:
            file.write(text)



    def annotateside(self,scale=4):
        imagepath = self.sidecurrentimeifolder / self.sideimagename
        annotatedimagename = self.sidecurrentimeifolder / self.sideannotatedimagename
        #read image
        image = cv2.imread(imagepath)
        image_copy = image.copy()

        #filter data by its side's region
        dfsideregions = self.dfsidecsvdata[ (self.dfsidecsvdata['region'].isin(self.sideregiongroup))]

        for index, row in dfsideregions.iterrows():
            boxes = [(row[f"a{i}"],row[f"x{i}"],row[f"y{i}"]) for i in range(1,8) if row[f"a{i}"] > 0 ]
            for bx in boxes:
                a,x,y = bx
                utils.AnnotateOnImage(image_copy,top_left=(x/scale,y/scale),area=a)
        cv2.imwrite(self.sidecurrentimeifolder / self.sideannotatedimagename, image_copy)

    def showannotatedside(self):
        self.annotateside()
        imageannotated = cv2.imread(self.sidecurrentimeifolder / self.sideannotatedimagename)
        image_rgb = cv2.cvtColor(imageannotated, cv2.COLOR_BGR2RGB)
        # Plot the image using Matplotlib
        plt.imshow(image_rgb)
        plt.show()











