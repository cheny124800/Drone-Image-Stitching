import cv2
import geometry as gm
import glob

def changePerspective(imageList, dataMatrix):

    images = sorted(glob.glob("temp/*.JPG"))
    print ("Warping Perspective Now")

    for i in range(0,len(images)):
        image = cv2.imread(images[i])
        image = image[::2, ::2, :]

        M = gm.computeUnRotMatrix(dataMatrix[i,:])
        correctedImage = gm.warpPerspectiveWithPadding(image,M)

        cv2.imwrite("temp/" + str(i).zfill(2) + ".JPG", correctedImage)

    print ("Done Warping Perspective")
