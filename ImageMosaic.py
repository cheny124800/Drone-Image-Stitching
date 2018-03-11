'''
Driver script. Execute this to perform the mosaic procedure.
'''

import utilities as util
import Combiner
import cv2
import Dataset
import os
import datetime
import Perspective
import shutil

cv2.ocl.setUseOpenCL(False)
now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

Dataset.write()

if os.path.isdir('results') == True:
    os.rename('results', 'results - ' + str(now))

os.mkdir('results')

fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"

if os.path.isdir('temp') == True:
    shutil.rmtree('temp', ignore_errors=False, onerror=None)

os.mkdir('temp')

allImages, dataMatrix = util.importData(fileName, imageDirectory)
Perspective.changePerspective(allImages, dataMatrix)

result = Combiner.combine()

util.display("RESULT", result)
cv2.imwrite("results/finalResult.png", result)
