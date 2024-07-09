import cv2
import os
import numpy as np
import functools

def sys_moments(img):
    moments = cv2.moments(img)#返回的是一个字典，三阶及以下的几何矩（mpq）、中心矩(mupq)和归一化的矩(nupq)
    humoments = cv2.HuMoments(moments)#根据几何矩（mpq）、中心矩(mupq)和归一化的矩(nupq)计算出hu不变矩
    humoment = -(np.log(np.abs(humoments)))/np.log(10)
    return humoment

def main():
    f1 = open("D:\\Coding\\ur_aruco\\image\\Humoments_data.txt",'w+')
    input_dir = "D:\\Coding\\ur_aruco\\train_data\\"
    aa = os.listdir( input_dir) 
    abc=0
    set_list = []
    list00=[]
    zs=len(aa)*7
    for ia in aa:
        grayy=cv2.imread(input_dir+ia,0)
#         arr1=def_moments2(grayy)
        arr1=sys_moments(grayy)  
#         print(type(arr1))
        for item in range(len(arr1)):
            s=arr1[item,0]
            set_list.append(s)
            list00.append(s)
    for cs0 in range(zs):
        if cs0%7==0:
            abc=abc+1
        f1.write("第 "+str(abc)+"张图片:\t"+str(format(list00[cs0],".3f"))+"\n")
    f1.close()    
if __name__ == '__main__':
    main()   
    print("well done")    
