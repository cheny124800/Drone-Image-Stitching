'''
Driver script. Execute this to perform the mosaic procedure.
'''

import utilities as util
import Combiner
import cv2
import gc

fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"

allImages, dataMatrix = util.importData(fileName, imageDirectory)

myCombiner = Combiner.Combiner(allImages, dataMatrix)
result = myCombiner.createMosaic()
util.display("RESULT", result)
cv2.imwrite("results/finalResult.png", result)
