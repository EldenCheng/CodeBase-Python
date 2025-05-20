import cv2
import numpy as np

"""
We use the Mean Square Error (MSE) of the pixel values of the two images. Similar images will have less mean square error value. 
Using this method, we can compare two images having the same height, width and number of channels.
The 'Mean Squared Error' between the two images is the sum of the squared difference between the two images;
NOTE: the two images must have the same dimension
"""


# define the function to compute MSE between two images
def mse(img1, img2):
    """
    这个方法只会给出两个图像之间有差异的像素差的比例
    这个比例一定程序上可以看成两个图像之前的差异
    但是问题在于如果使用摄像头的话, 环境光, 阴影的差异也会被open cv认为是像素差异
    所以实用性好像比较一般
    """
    height, width = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    mse = err / (float(height * width))
    return mse, diff


if __name__ == '__main__':
    # load the input images
    img1 = cv2.imread('Pics/desk1.jpg')
    img2 = cv2.imread('Pics/desk2.jpg')
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    mse, diff = mse(img1, img2)
    print("Image matching Error between the two images:", mse)  # The less the errors get, the similar the pics are

    cv2.imshow("difference", diff)
    cv2.waitKey(0)
    if cv2:
        cv2.destroyAllWindows()
