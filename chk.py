import glob
import cv2

image = glob.glob("fin\*.png")
stitcher = cv2.createStitcher(try_use_gpu=True)
images = []

im1 = cv2.imread("fin/593.png")
im2 = cv2.imread("fin/601.png")
im3 = cv2.imread("fin/618.png")

images.append(im1)
images.append(im2)
images.append(im3)

result = stitcher.stitch(images)
cv2.imwrite("finRes.png", result[1])
