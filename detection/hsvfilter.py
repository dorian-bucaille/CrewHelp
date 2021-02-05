# Written by Ben from Learn Code By Gaming : https://github.com/learncodebygaming/opencv_tutorials
# Custom data structure to hold the state of an HSV filter
class HsvFilter:

    def __init__(self, hmin=None, smin=None, vmin=None, hmax=None, smax=None, vmax=None,
                 sadd=None, ssub=None, vadd=None, vsub=None):
        self.hMin = hmin
        self.sMin = smin
        self.vMin = vmin
        self.hMax = hmax
        self.sMax = smax
        self.vMax = vmax
        self.sAdd = sadd
        self.sSub = ssub
        self.vAdd = vadd
        self.vSub = vsub
