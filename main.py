
import cv2
import matplotlib.pyplot as plt
from Front  import Front
from pathlib import Path
import os
from FrontCVData import FrontCVData
import pandas as pd


# f = Front()
# f.displayannotatedfront()


frontsdata = FrontCVData(grades=["B","C"])
# data.mergefrontdataonegrade()
# data.saveannotatedimagesbygrade("B")
frontsdata.mergefrontdataallgivengrades()
frontsdata.plotfrontmergeddata()
frontsdata.saveallannotatedimagesbygrade()
