from Side import Side
from CVDataAnalysisi import AllPhonesSidesCVData


# f = Front()
# f.displayannotatedfront()


# frontsdata = FrontCVData(grades=["B","C"])
# # data.mergefrontdataonegrade()
# # data.saveannotatedimagesbygrade("B")
# frontsdata.mergefrontdataallgivengrades()
# frontsdata.plotfrontmergeddata()
# frontsdata.saveallannotatedimagesbygrade()

# d1d9regions = [f"D{i}" for i in range(1, 10)]
# sd = Side(sideimei="351884703360489", sidename="Display.jpg",sideregiongroup=d1d9regions)
# sd.showannotatedside()

a = AllPhonesSidesCVData()
a.populateallphonessides()
a.mergeeachsidetoitscsvfile()
print()


