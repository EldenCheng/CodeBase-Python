import cv2
import matplotlib.pyplot as plt

#计算方差
def getss(list):
    #计算平均值
    avg=sum(list)/len(list)
    #定义方差变量ss，初值为0
    ss=0
    #计算方差
    for l in list:
        ss+=(l-avg)*(l-avg)/len(list)
    #返回方差
    return ss

#获取每行像素平均值
def getdiff(img):
    #定义边长
    Sidelength=250
    #缩放图像
    img=cv2.resize(img,(Sidelength,Sidelength),interpolation=cv2.INTER_CUBIC)
    #灰度处理
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #avglist列表保存每行像素平均值
    avglist=[]
    #计算每行均值，保存到avglist列表
    for i in range(Sidelength):
        #print("gray[%d]=" % i, gray[i])
        avg=sum(gray[i])/len(gray[i])
        avglist.append(avg)
    #返回avglist平均值
    return avglist

#读取测试图片
img1=cv2.imread(r".\testimages\Screenshot1440P.png")
diff1=getdiff(img1)
print('img1:',getss(diff1))

#读取测试图片
img11=cv2.imread(r".\testimages\Other_Screenshot1080P.png")
diff11=getdiff(img11)
print('img11:',getss(diff11))

x=range(250)
plt.figure("avg")
plt.plot(x,diff1,marker="*",label="$walk01$")
plt.plot(x,diff11,marker="*",label="$walk03$")
plt.title("avg")
plt.legend()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
