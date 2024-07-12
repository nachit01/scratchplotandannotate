from Side import Side

class Phone:
    D1D9REGIONS = [f"D{i}" for i in range(1, 10)]#front
    H1H9REGIONS = [f"H{i}" for i in range(1, 10)]#back
    L1L7REGIONS = [[f"L{i}" for i in range(1, 7)] , "L7 Left SIM"] # left
    R1R5REGIONS = [f"R{i}" for i in range(1, 6)] # right
    T1R4REGIONS = [f"T{i}" for i in range(1, 5)] # top
    B1B3REGIONS = [f"T{i}" for i in range(1, 4)] # bottom
    def __init__(self,imei = None,rootpath=r"evo_images_CSV"):
        self.imei = imei
        self.front = Side(sidename="front",sideimei=imei,sidecsvfile= r"Front.csv",sideimagename = r"Display.jpg",sideregiongroup=Phone.D1D9REGIONS,rootpath=rootpath)
        self.back =  Side(sidename="back" ,sideimei=imei, sidecsvfile= r"Back.csv",sideimagename = r"Housing.jpg",sideregiongroup=Phone.H1H9REGIONS,rootpath=rootpath)
        self.left =  Side(sidename="left" ,sideimei=imei, sidecsvfile= r"Long.csv",sideimagename = r"Left.jpg",sideregiongroup=Phone.L1L7REGIONS,rootpath=rootpath)
        self.right = Side(sidename="right",sideimei=imei, sidecsvfile= r"Long.csv",sideimagename = r"Right.jpg",sideregiongroup=Phone.R1R5REGIONS,rootpath=rootpath)
        self.top =   Side(sidename="top"  ,sideimei=imei, sidecsvfile= r"Short.csv",sideimagename = r"Top.jpg",sideregiongroup=Phone.T1R4REGIONS,rootpath=rootpath)
        self.bottom= Side(sidename="bottom",sideimei=imei, sidecsvfile= r"Short.csv",sideimagename = r"Bottom.jpg",sideregiongroup=Phone.B1B3REGIONS,rootpath=rootpath)

