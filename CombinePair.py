import cv2
import numpy as np
import geometry as gm
import copy
import utilities as util
import glob
from PIL import Image

def combine(image1, image2, detector):

    #detector = cv2.ORB_create(nfeatures=10000, score = cv2.ORB_FAST_SCORE) #SURF showed best results
    #detector = cv2.xfeatures2d.SIFT_create(nfeatures=10000)



    '''
    detector = cv2.xfeatures2d.SURF_create(10)
    >>>>>>> 01bb016deff80f1a90292757a521e2b8ee47594d
    '''

    #detector.setExtended (True)
    #detector.setUpright (True)

    gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    ret1, mask1 = cv2.threshold(gray1,1,255,cv2.THRESH_BINARY)
    kp1, descriptors1 = detector.detectAndCompute(gray1,mask1)

    gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
    ret2, mask2 = cv2.threshold(gray2,1,255,cv2.THRESH_BINARY)
    kp2, descriptors2 = detector.detectAndCompute(gray2,mask2)

    keypoints1Im = cv2.drawKeypoints(image1, kp1, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color=(0,0,255))
    util.display("KEYPOINTS",keypoints1Im)
    keypoints2Im = cv2.drawKeypoints(image2, kp2, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color=(0,0,255))
    util.display("KEYPOINTS",keypoints2Im)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(descriptors2,descriptors1, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.55 * n.distance:
            good.append(m)

    print (str(len(good)) + " Matches were Found")

    if len(good) <= 10:
        return image1

    matches = copy.copy(good)

    matchDrawing = util.drawMatches(gray2,kp2,gray1,kp1,matches)
    util.display("matches",matchDrawing)

    src_pts = np.float32([ kp2[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp1[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

    A = cv2.estimateRigidTransform(src_pts,dst_pts,fullAffine=False)

    if A is None:
        HomogResult = cv2.findHomography(src_pts,dst_pts,method=cv2.RANSAC)
        H = HomogResult[0]

    height1,width1 = image1.shape[:2]
    height2,width2 = image2.shape[:2]

    corners1 = np.float32(([0,0],[0,height1],[width1,height1],[width1,0]))
    corners2 = np.float32(([0,0],[0,height2],[width2,height2],[width2,0]))

    warpedCorners2 = np.zeros((4,2))

    for i in range(0,4):
        cornerX = corners2[i,0]
        cornerY = corners2[i,1]
        if A is not None: #check if we're working with affine transform or perspective transform
            warpedCorners2[i,0] = A[0,0]*cornerX + A[0,1]*cornerY + A[0,2]
            warpedCorners2[i,1] = A[1,0]*cornerX + A[1,1]*cornerY + A[1,2]
        else:
            warpedCorners2[i,0] = (H[0,0]*cornerX + H[0,1]*cornerY + H[0,2])/(H[2,0]*cornerX + H[2,1]*cornerY + H[2,2])
            warpedCorners2[i,1] = (H[1,0]*cornerX + H[1,1]*cornerY + H[1,2])/(H[2,0]*cornerX + H[2,1]*cornerY + H[2,2])

    allCorners = np.concatenate((corners1, warpedCorners2), axis=0)

    [xMin, yMin] = np.int32(allCorners.min(axis=0).ravel() - 0.5)
    [xMax, yMax] = np.int32(allCorners.max(axis=0).ravel() + 0.5)

    translation = np.float32(([1,0,-1*xMin],[0,1,-1*yMin],[0,0,1]))
    warpedResImg = cv2.warpPerspective(image1, translation, (xMax-xMin, yMax-yMin))


    if A is None:
        fullTransformation = np.dot(translation,H) #again, images must be translated to be 100% visible in new canvas
        warpedImage2 = cv2.warpPerspective(image2, fullTransformation, (xMax-xMin, yMax-yMin))

    else:
        warpedImageTemp = cv2.warpPerspective(image2, translation, (xMax-xMin, yMax-yMin))
        warpedImage2 = cv2.warpAffine(warpedImageTemp, A, (xMax-xMin, yMax-yMin))


    #util.display("r", warpedResImg, 400000)

    #util.display("r", warpedResImg, 400000)



    #warpedImage2 = warpedImage2[::2, ::2, :]
    #warpedResImg = warpedResImg[::2, ::2, :]
    #warpedImage2 = 0.8*warpedImage2

    #warpedImage2[::2, ::2,:] = 0
    result = np.where(warpedImage2 != 0, warpedImage2, warpedResImg)
#    cv2.imwrite("back.JPG", warpedResImg)
#    cv2.imwrite("fore.JPG", warpedImage2)
    #result = Image.blend(warpedResImg, warpedImage2, alpha=0.5)
    #print (warpedImage2.shape[:2])
    #print (warpedResImg.shape[:2])

    #result = image1 + image2
    #result = Image.blend(warpedResImg, warpedImage2, alpha=0.5)

    util.display("result", result)

    return result
