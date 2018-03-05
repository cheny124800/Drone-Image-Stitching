import cv2
import copy

def matchnum(image1, image2):
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
        detector = cv2.ORB_create(nfeatures=100000, scoreType=cv2.ORB_FAST_SCORE) #SURF showed best results
        #detector.setExtended(True)
        gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        ret1, mask1 = cv2.threshold(gray1,1,255,cv2.THRESH_BINARY)
        kp1, descriptors1 = detector.detectAndCompute(gray1,mask1) #kp = keypoints

        gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        ret2, mask2 = cv2.threshold(gray2,1,255,cv2.THRESH_BINARY)
        kp2, descriptors2 = detector.detectAndCompute(gray2,mask2)

        #Visualize matching procedure.
        keypoints1Im = cv2.drawKeypoints(image1, kp1, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color = (0, 0, 255))
        #util.display("KEYPOINTS", keypoints1Im)
        keypoints2Im = cv2.drawKeypoints(image2, kp2, outImage = cv2.DRAW_MATCHES_FLAGS_DEFAULT, color = (0, 0, 255))
        #util.display("KEYPOINTS", keypoints2Im)

        matcher = cv2.BFMatcher() #use brute force matching
        matches = matcher.knnMatch(descriptors2,descriptors1, k=2) #find pairs of nearest matches
        #prune bad matches
        good = []
        for m, n in matches:
            if m.distance <= 0.7 * n.distance:
                good.append(m)

        val = (len(good))
        return val