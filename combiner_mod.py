import cv2
import numpy as np
import utilities as util
import copy
import gc

def combine(image1, image2):
        '''
        :param index2: index of self.imageList and self.kpList to combine with self.referenceImage and self.referenceKeypoints
        :return: combination of reference image and image at index 2
        '''

        #Attempt to combine one pair of images at each step. Assume the order in which the images are given is the best order.
        #This intorduces drift!
        '''
        image1 = copy.copy(self.imageList[index2 - 1])
        image2 = copy.copy(self.imageList[index2])
        '''
        '''
        Descriptor computation and matching.
        Idea: Align the images by aligning features.
        '''
        detector = cv2.ORB_create(nfeatures=1000000, scoreType=cv2.ORB_FAST_SCORE) #SURF showed best results
        #detector.setExtended(True)
        gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        ret1, mask1 = cv2.threshold(gray1,1,255,cv2.THRESH_BINARY)
        kp1, descriptors1 = detector.detectAndCompute(gray1,mask1) #kp = keypoints

        gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        ret2, mask2 = cv2.threshold(gray2,1,255,cv2.THRESH_BINARY)
        kp2, descriptors2 = detector.detectAndCompute(gray2,mask2)

        #Visualize matching procedure.
        keypoints1Im = cv2.drawKeypoints(image1, kp1, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color = (0, 0, 255))
        util.display("KEYPOINTS", keypoints1Im)
        keypoints2Im = cv2.drawKeypoints(image2, kp2, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color = (0, 0, 255))
        util.display("KEYPOINTS", keypoints2Im)

        matcher = cv2.BFMatcher() #use brute force matching
        matches = matcher.knnMatch(descriptors2,descriptors1, k=2) #find pairs of nearest matches
        #prune bad matches
        good = []
        for m, n in matches:
            if m.distance <= 0.55 * n.distance:
                good.append(m)

        val = (len(good))
        '''
        if len(good) >= 70:
            good = []
            for m, n in matches:
                if 1:#m.distance <= 0.6 * n.distance:
                     good.append(m)

		'''
        '''
        good.sort(reverse=True)
        print(len(good))'''
        matches = copy.copy(good)

        #Visualize matches
        matchDrawing = util.drawMatches(gray2,kp2,gray1,kp1,matches)
        util.display("matches",matchDrawing)

        #NumPy syntax for extracting location data from match data structure in matrix form
        src_pts = np.float32([ kp2[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp1[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        '''
        Compute Affine Transform
        Idea: Because we corrected for camera orientation, an affine transformation *should* be enough to align the images
        '''

        A = cv2.estimateRigidTransform(src_pts, dst_pts, fullAffine = False) #false because we only want 5 DOF. we removed 3 DOF when we unrotated
        if A is None: #RANSAC sometimes fails in estimateRigidTransform(). If so, try full homography. OpenCV RANSAC implementation for homography is more robust.
            HomogResult = cv2.findHomography(src_pts, dst_pts, method = cv2.RANSAC)
            H = HomogResult[0]


        '''
        Compute 4 Image Corners Locations
        Idea: Same process as warpPerspectiveWithPadding() excewpt we have to consider the sizes of two images. Might be cleaner as a function.
        '''
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

        '''Compute Image Alignment and Keypoint Alignment'''
        translation = np.float32(([1,0,-1*xMin],[0,1,-1*yMin],[0,0,1]))
        warpedResImg = cv2.warpPerspective(image1, translation, (xMax-xMin, yMax-yMin))
        if A is None:
            fullTransformation = np.dot(translation,H) #again, images must be translated to be 100% visible in new canvas
            warpedImage2 = cv2.warpPerspective(image2, fullTransformation, (xMax-xMin, yMax-yMin))
        else:
            warpedImageTemp = cv2.warpPerspective(image2, translation, (xMax - xMin, yMax - yMin))
            warpedImage2 = cv2.warpAffine(warpedImageTemp, A, (xMax - xMin, yMax - yMin))

        #self.imageList[index2] = copy.copy(warpedImage2) #crucial: update old images for future feature extractions

        resGray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        warpedResGray = cv2.warpPerspective(resGray, translation, (xMax - xMin, yMax - yMin))

        '''Compute Mask for Image Combination'''
        ret, mask1 = cv2.threshold(warpedResGray,1,255,cv2.THRESH_BINARY_INV)
        mask3 = np.float32(mask1)/255

        #apply mask
        warpedImage2[:,:,0] = warpedImage2[:,:,0]*mask3
        warpedImage2[:,:,1] = warpedImage2[:,:,1]*mask3
        warpedImage2[:,:,2] = warpedImage2[:,:,2]*mask3

        result = warpedResImg + warpedImage2
        #visualize and save result
        #self.resulmage = result
        #util.display("result",result)
        #cv2.imwrite("results/intermediateResult"+str(index2)+".png",result)
        gc.collect()
        del gc.garbage[:]

        return result
