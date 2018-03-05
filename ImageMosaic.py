'''
Driver script. Execute this to perform the mosaic procedure.
'''

import utilities as util
import Combiner
import cv2
#import Dataset
import os
import datetime
import combiner_mod as com
import glob
import MatchNum as mn
import gc

now = datetime.datetime.now()
imagelist = sorted(glob.glob("fin\*.png"))
image = []

#Dataset.write()

#if os.path.isdir('results') == True:
#    os.rename('results', 'results - ' + str(now))

#os.mkdir('results')

result = cv2.imread(imagelist[0])
#result = result[::3,::3,:]

for i in range (1, len(imagelist)):
	im = cv2.imread(imagelist[i])
	#im = im[::1,::1,:]

	#val = mn.matchnum(result, im)

	#print(val)
	#if val <= 100:
		#continue

	result = com.combine(result, im)


	'''
	src = result
	tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
	b, g, r = cv2.split(src)
	rgba = [b,g,r, alpha]
	dst = cv2.merge(rgba,4)
	result = dst
	'''


	#result = cv2.resize(result, (4000, 3000))
	cv2.imwrite("results/imres" + str(i) + ".png", result)
	gc.collect()
	del gc.garbage[:]

cv2.imwrite("results/finalResult.png", result)

'''
fileName = "datasets/imageData.txt"
imageDirectory = "datasets/images/"
allImages, dataMatrix = util.importData(fileName, imageDirectory)
myCombiner = Combiner.Combiner(allImages, dataMatrix)
result = myCombiner.createMosaic()
util.display("RESULT", result)
cv2.imwrite("results/finalResult.png", result)
'''
