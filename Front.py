import pandas as pd
import re
import utils
import cv2
import matplotlib.pyplot as plt


class Front:
    def __init__(self,dfcsvdata=[],csvfile= r"evo_images_CSV\Front.csv",imagepath = r"evo_images_CSV\Display.jpg"):
        self.csvfile =csvfile
        self.imagepath = imagepath
        self.csvfilenew = self.correctcsv()
        self.dfcsvdata = pd.read_csv(self.csvfilenew, on_bad_lines='warn')




    def correctcsv(self):
        # Open the file in read mode
        with open(self.csvfile, 'r') as file:
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
                row = c +','
            else:
                row += c +','
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
        correctedCSVName = self.csvfile.replace("Front.csv", "Front_new.csv")
        text =   "".join(rows)
        with open(correctedCSVName, mode='w') as file:
            file.write(text)
        return correctedCSVName
    def annotateFront(self,scale=4):
        image = cv2.imread(self.imagepath)
        image_copy = image.copy()
        annotatedimagename = self.imagepath.replace("Display.jpg", "Display_annotated.jpg")

        for index, row in self.dfcsvdata.iloc[:9].iterrows():
            print(f"index:{index},--- {row["region"]}")
            boxes = [(row[f"a{i}"],row[f"x{i}"],row[f"y{i}"]) for i in range(1,8) if row[f"a{i}"] > 0 ]
            for bx in boxes:
                a,x,y = bx
                utils.AnnotateOnImage(image_copy,top_left=(x/scale,y/scale),area=a)

        cv2.imwrite(annotatedimagename, image_copy)
    def displayannotatedfront(self):
        self.annotateFront()
        # Display the image in a window
        # Convert the image from BGR (OpenCV's default) to RGB (Matplotlib's default)
        annotatedimagename = r"evo_images_CSV\Display_annotated.jpg"
        imageannotated = cv2.imread(annotatedimagename)
        image_rgb = cv2.cvtColor(imageannotated, cv2.COLOR_BGR2RGB)
        # Plot the image using Matplotlib
        plt.imshow(image_rgb)
        plt.show()










