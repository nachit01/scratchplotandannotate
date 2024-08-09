import GradesAnalysis
from Side import Side
from CVDataAnalysisi import AllPhonesSidesCVData
from GradesAnalysis import Grade
import os


# # # #init
# a = AllPhonesSidesCVData()
# # #
# # # #get manual grades from csv to txt
# a.createimeistxtfromcsv()
# #
# # # #merge data
# a.mergeeachsidetoitscsvfile()
# a.mergeelsdstocsvfile()
# #
# # #save annotated images (flush manually)
# a.saveannotatedimagesbygrade()
# #
# # #plot
# # a.plotareaallsidesmergeddata()
# # a.plotlightdeepscracthescountsallsidesbygrade()
# #
# # # a.plotimage(imagename = "Housing_C_359646709836321 - 1.jpg")


######################
#######--GRADES--#########
grades = Grade()
#read grade files
grades.readallgradesvalues()
#plot
# grades.pltogradesbyside()
#insert manual into evo grade csv
grades.evovsmanualgradescsv()
#mismatch
grades.plotmismatches()



# print(a.H1H18REGIONS)





