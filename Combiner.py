import cv2
import glob
import CombinePair
import JPEGEncoder as en

def combine():
    imagelist = sorted(glob.glob("temp/*.JPG"))

    result = en.compress(cv2.imread(imagelist[0]))
    detector = cv2.xfeatures2d.SURF_create(300)

    for i in range(1, len(imagelist)):
        image = en.compress(cv2.imread(imagelist[i]))

        try:
            result = CombinePair.combine(result, image, detector)
            cv2.imwrite("results/int_res" + str(i) + ".JPG", result)
            print ("Done " + str(i))

        except:
            print ("Fail " + str(i))
            #cv2.imwrite("results/int_res" + str(i) + ".JPG", result)

    return result
