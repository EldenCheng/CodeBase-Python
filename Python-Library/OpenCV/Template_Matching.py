import cv2
import numpy as np

if __name__ == '__main__':

    # 读取目标图像并将其转换成灰度图
    img = cv2.imread("./target.jpg", 1)
    img2 = cv2.imread("./target.jpg", 1)
    img3 = cv2.imread("./target.jpg", 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 读取要查找的子图像并且获取子图像的长度与高度
    template = cv2.imread('./tem.jpg', 0)
    w, h = template.shape[::-1]

    '''
    使用OpenCV的方法查找满足条件的目标图像区域, 注意的是返回的区域不一定只有一个, 用法
    cv2.matchTemplata(img_big,img_temp,cv2.method)
    img_big:在该图上查找图像
    img_temp:待查找的图像，模板图像
    method: 模板匹配的方法
    method有以下几种:
    
       method                           introduce
    CV_TM_SQDIFF 平方差匹配法    该方法采用平方差来进行匹配；最好的匹配值为0；匹配越差，匹配值越大
    CV_TM_CCORR 相关匹配法       该方法采用乘法操作；数值越大表明匹配程度越好。
    CV_TM_CCOEFF 相关系数匹配法   1表示完美的匹配；-1表示最差的匹配。
    CV_TM_SQDIFF_NORMED        归一化平方差匹配法
    CV_TM_CCORR_NORMED         归一化相关匹配法
    CV_TM_CCOEFF_NORMED        归一化相关系数匹配法
    '''
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    '''
    根据不同的方法,可能会有多个匹配度(匹配度0 - 1)的结果返回,但由于各种原因, 匹配度最高的区域不一定就是我们想要的区域, 但一般来说我们一个
    template只需要获得一个理想中的匹配区域, 所以我们尝试调整匹配度临界值来查找最有可能的一个匹配区域, 
    下面就是用二分法来尝试调整匹配度临界值以获取唯一的一个区域:
    1. 阈值始终为区间左端和右端的均值，即 threshhold = (R+L)/2；
    2. 如果当前阈值查找结果数量大于1，则说明阈值太小，需要往右端靠近，即左端就增大，即L += (R - L) / 2；
    3. 如果结果数量为0，则说明阈值太大，右端应该减小，即R -= (R - L) / 2；
    4. 当结果数量为1时，说明阈值刚好
    '''

    L = 0  # 最小的临界值为0
    R = 1  # 最大的临界值为1
    count = 0
    while count < 20:  # 最多尝试20次
        threshold = (L + R) / 2  # 最小与最大值二分
        count += 1
        loc = np.where(res >= threshold)  # 返回res矩阵中的满足匹配度>=临界值的那一部分, 组成一个新矩阵loc
        if len(loc[0]) > 1:  # 如果当前阈值查找结果数量大于1，则说明阈值太小，需要往右端靠近，即左端就增大，即L += (R - L) / 2
            L += (R - L) / 2  # 如果结果数量为0，则说明阈值太大，右端应该减小，即R -= (R - L) / 2
        elif len(loc[0]) == 1:  # 当结果数量为1时，说明阈值刚好
            pt = loc[::-1]
            print('目标区域的左上角坐标:', pt[0], pt[1])
            print('次数:', count)
            print('阀值', threshold)
            break
        elif len(loc[0]) < 1:
            R -= (R - L) / 2

    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (34, 139, 34), 2)

    cv2.imshow("img_template", template)
    cv2.imshow("Auto adjust processed", img)

    '''
    除了人工调整匹配度临界值之外, 实际上OpenCV也提供了一个方法用于直接返回最高的与最低匹配度的区域的方法cv2.minMaxLoc()
    '''
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc  # 左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位
    # 在原图上画矩形
    cv2.rectangle(img2, top_left, bottom_right, (0, 0, 255), 2)
    cv2.imshow("MiniMax adjust processed", img2)

    '''
    当然有时候也需要使用template来获得多个匹配区域, 这样子就不能使用上面的方法来只获取唯一的一个值, 而是指定一个稍低的匹配度临界值
    来期望获取与目标区域数量一致的的匹配区域
    '''
    threshold = 0.9  # 唯一匹配度的值为0.9921875, 所以尝试稍微降低匹配度来获取其它相似的匹配区域
    loc = np.where(res >= threshold)
    loc = loc[::-1]  # # 矩阵反转, 作用应该是从最小满足临界点的匹配区域开始
    p = zip(*loc)  # 将矩阵元素变回一对对的列表
    for pt in p:
        cv2.rectangle(img3, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)

    cv2.imshow('Multi match area', img3)

    cv2.waitKey(0)
