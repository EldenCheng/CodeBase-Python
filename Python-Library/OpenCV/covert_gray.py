import cv2
import numpy as np

if __name__ == "__main__":
    img_path = "slidbar_authcode_pic5.PNG"
    img = cv2.imread(img_path)
    #获取图片的宽和高
    width, height = img.shape[:2][::-1]
    #将图片缩小便于显示观看
    # img_resize = cv2.resize(img, (int(width*0.5), int(height*0.5)), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("img",img_resize)
    # print("img_reisze shape:{}".format(np.shape(img_resize)))

    #将图片转为灰度图
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    # ret, thresh = cv2.threshold(img_gray, 12, 255, cv2.THRESH_BINARY)
    # cv2.imshow("img_gray",img_gray)
    # cv2.imshow("img_gray", thresh)
    print("img_gray shape:{}".format(np.shape(img_gray)))
    cv2.waitKey()
    cv2.imwrite('5.jpg', img_gray)
    # cv2.imwrite('3.jpg', thresh)

