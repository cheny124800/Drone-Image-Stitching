from libxmp.utils import file_to_dict

f_ = "datasets/images/DJI_0570.JPG"

def xmp (f_):
    #f_ = "datasets/images/DJI_0570.JPG"

    xmp = file_to_dict(f_)
    dji = xmp['http://www.dji.com/drone-dji/1.0/']

    return dji[0][1], dji[5][1], dji[6][1], dji[7][1]

    '''for x in dji:
        print x
    '''
'''
    print dji[0][0], dji[0][1]
    print dji[1][0], dji[1][1]
    print dji[2][0], dji[2][1]
    print dji[3][0], dji[3][1]
    print dji[4][0], dji[4][1]
'''
#xmp (f_)
'''
def main():
    M = np.random.randn(3,3)
    img = np.random.randint(255, size=(1024, 1024, 3))
    while(1):
        rot = cv2.warpPerspective(img, M, (1024, 1024))
        time.sleep(1)

def main():
    M = np.random.randn(3,3)
    img = np.random.randint(255, size=(4096, 4096, 3))
    img = np.uint8(img)
    rot = np.zeros_like(img)
    while(1):
        cv2.warpPerspective(img, M, (4096, 4096), dst=rot)
        time.sleep(1)
'''
