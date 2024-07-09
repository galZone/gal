# 导入所有必要的库
import cv2
import os
  
# 从指定的路径读取视频
cam = cv2.VideoCapture( "D:\\Coding\\ur_aruco\\image\\data_vido1.mp4" )
  
try :
      
     # 创建名为data的文件夹
     if not os.path.exists( 'data' ):
         os.makedirs( 'data' )
  
# 如果未创建，则引发错误
except OSError:
     print ( 'Error: Creating directory of data' )
  
# frame
currentframe = 0
  
while ( True ):
      
     # reading from frame
     ret, frame = cam.read()
  
     if ret:
         # 如果视频仍然存在，继续创建图像
         name = './data/frame' + str (currentframe) + '.jpg'
         print ( 'Creating...' + name)
  
         # 写入提取的图像
         cv2.imwrite(name, frame)
  
         # 增加计数器，以便显示创建了多少帧
         currentframe += 1
     else :
         break
  
# 一旦完成释放所有的空间和窗口
cam.release()
cv2.destroyAllWindows()