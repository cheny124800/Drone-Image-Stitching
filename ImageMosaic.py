'''
Driver script. Execute this to perform the mosaic procedure.
'''

import utilities as util
import Combiner
<<<<<<< HEAD
import cv2
import Dataset
import os
import datetime


now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

Dataset.write()

if os.path.isdir('results') == True:
    os.rename('results', 'results - ' + str(now))

os.mkdir('results')

=======
import Dataset

Dataset.write()
>>>>>>> 01bb016deff80f1a90292757a521e2b8ee47594d

fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"
allImages, dataMatrix = util.importData(fileName, imageDirectory)
myCombiner = Combiner.Combiner(allImages, dataMatrix)
result = myCombiner.createMosaic()
util.display("RESULT", result)
cv2.imwrite("results/finalResult.png", result)
