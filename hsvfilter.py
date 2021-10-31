
#custom data structure to hold state of an HSV filter
class HsvFilter:

    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                    sAdd=None, sSub=None, vAdd=None, vSub=None):

        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
    
    def set_elixirlvl13(self):
        self.hMin = 16
        self.sMin = 136
        self.vMin = 0
        self.hMax = 28
        self.sMax = 149
        self.vMax = 255
        self.sAdd = 184
        self.sSub = 116
        self.vAdd = 137
        self.vSub = 20
    
    def set_troop_placement(self):
        self.hMin = 35
        self.sMin = 198
        self.vMin = 186
        self.hMax = 47
        self.sMax = 255
        self.vMax = 255
        self.sAdd = 128
        self.sSub = 46
        self.vAdd = 44
        self.vSub = 0
