'''
Driver script. Execute this to perform the mosaic procedure.
'''

import utilities as util
import untranscom
import cv2
#import Dataset
import os
import datetime
import combiner_mod as com
import glob
import MatchNum as mn

fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"
allImages, dataMatrix = util.importData(fileName, imageDirectory)
myCombiner = untranscom.Combiner(allImages, dataMatrix)
'''
result = myCombiner.createMosaic()
util.display("RESULT", result)
cv2.imwrite("results/finalResult.png", result)
'''
