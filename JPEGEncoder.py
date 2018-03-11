import cv2

def compress(im):

    return im
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    result, im = cv2.imencode('.jpg', im, encode_param)
    decimg = cv2.imdecode(im, 1)

    return decimg
