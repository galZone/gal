import numpy as np
import cv2
import os
from PIL import Image as pil_image
import skimage.io as io
from matplotlib import pyplot as plt
from skimage import data_dir

# 函数功能： 图片转为灰度图
def binarization():    
    # 获取目录下所有图片名    
    filename = os.listdir(r"D:\Coding\ur_aruco\data")
    print(filename)
    # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
    base_dir = r"D:\Coding\ur_aruco\data" # input
    new_dir  = r"D:\Coding\ur_aruco\train_data" #output
    for img in filename:
      name = img
      path1= os.path.join(base_dir,img)
      img = cv2.imread(path1)
      # print(img)
      Grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      ret, thresh = cv2.threshold(Grayimg, 250, 255,cv2.THRESH_TOZERO_INV)
      cv2.imwrite('img.png', thresh)
      image = pil_image.open('img.png')
      # 有需要可对图像进行大小调整
      #image = image.resize((350, 350),Image.ANTIALIAS)
      path= os.path.join(new_dir,name)
      image.save(path)
 
binarization()