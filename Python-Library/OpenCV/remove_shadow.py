import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread('Pics/slidbar_authcode_pic5.PNG', -1)

    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    index = 0
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        cv2.imwrite('shadows_out_dilated_{0}.png'.format(str(index)), dilated_img)
        bg_img = cv2.medianBlur(dilated_img, 21)
        cv2.imwrite('shadows_out_bg_{0}.png'.format(str(index)), bg_img)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        cv2.imwrite('shadows_out_bg_{0}.png'.format(str(index)), diff_img)
        norm_img = cv2.normalize(diff_img, img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(img)
        index +=1

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    cv2.imwrite('Pics/shadows_out.png', result)
    # cv2.imwrite('shadows_out_norm.png', result_norm)
