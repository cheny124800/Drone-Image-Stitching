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


now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

Dataset.write()

if os.path.isdir('results') == True:
    os.rename('results', 'results - ' + str(now))

os.mkdir('results')

fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"

print ("Creating Temp Directory")

if os.path.isdir('temp') == True:
    shutil.rmtree('temp', ignore_errors=False, onerror=None)

os.mkdir('temp')

print ("Copying Images to Temp Directory")

allImages, dataMatrix = util.importData(fileName, imageDirectory)
Perspective.changePerspective(allImages, dataMatrix)

print ("Stitching Images")

result = Combiner.combine()

util.display("RESULT", result, 4000000)
cv2.imwrite("results/finalResult.png", result)

print ("Done. Find your final image in results folder as finalResult.png")
