import cv2
import numpy as np


def importData(fileName, imageDirectory):
    '''
    :param fileName: Name of the pose data file in string form e.g. "datasets/imageData.txt"
    :param imageDirectory: Name of the directory where images arer stored in string form e.g. "datasets/images/"
    :return: dataMatrix: A NumPy ndArray contaning all of the pose data. Each row stores 6 floats containing pose information in XYZYPR form
        allImages: A Python List of NumPy ndArrays containing images.
    '''

    allImages = [] #list of cv::Mat aimghes
    dataMatrix = np.genfromtxt(fileName,delimiter=",",usecols=range(1,7),dtype=float) #read numerical data
    fileNameMatrix = np.genfromtxt(fileName,delimiter=",",usecols=[0],dtype=str) #read filen name strings
    for i in range(0,fileNameMatrix.shape[0]): #read images
        allImages.append(cv2.imread(imageDirectory+fileNameMatrix[i]))
    return allImages, dataMatrix

def display(title, image):
    '''
    OpenCV machinery for showing an image until the user presses a key.
    :param title: Window title in string form
    :param image: ndArray containing image to show
    :return:
    '''

    cv2.namedWindow(title,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title,1920,1080)
    cv2.imshow(title,image)
    cv2.waitKey(400)
    cv2.destroyWindow(title)

def drawMatches(img1, kp1, img2, kp2, matches):
    """
    Makes an image with matched features denoted.
    drawMatches() is missing in OpenCV 2. This boilerplate implementation taken from http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for m in matches:

        # Get the matching keypoints for each of the images
        img1_idx = m.queryIdx
        img2_idx = m.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        radius = 8
        thickness = 3
        color = (255,0,0) #blue
        cv2.circle(out, (int(x1),int(y1)), radius, color, thickness)
        cv2.circle(out, (int(x2)+cols1,int(y2)), radius, color, thickness)

        # Draw a line in between the two points
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), color, thickness)

    # Also return the image if you'd like a copy
    return out