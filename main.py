from Side import Side
from CVDataAnalysisi import AllPhonesSidesCVData



# # #init
a = AllPhonesSidesCVData()
# #
# # #get manual grades from csv to txt
a.createimeistxtfromcsv()
#
# # #merge data
a.mergeeachsidetoitscsvfile()
a.mergeelsdstocsvfile()
#
# #plot
# # a.plotareaallsidesmergeddata()
# # a.plotlightdeepscracthescountsallsidesbygrade()
#
# #save annotated images (flush manually)
a.saveannotatedimagesbygrade()
#
a.plotimage(imagename = "Housing_C_359646709836321 - 1.jpg")






# print(a.H1H18REGIONS)





