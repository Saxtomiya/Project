# -*- coding: UTF-8 -*- 
 
import cv2
import math 
import numpy as np 
import os
import copy
from PIL import Image, ImageOps


def makeimg(num):
    answers = []
    print("./short02/{0:05d}.png".format(num))
    # 画像の読み込み
    img_src1 = cv2.imread("./short02/{0:05d}.png".format(num), 1)
    yy = 243
    img_cri01=img_src1[yy+5:yy+75,0:640]
    cri_gray = cv2.cvtColor(img_cri01,cv2.COLOR_RGB2GRAY)
    cri_edge = cv2.Canny(cri_gray,100,100,True)
    point=[[4, 0], [635, 0], [11, 70], [627, 70]]
    perspective1 = np.float32(point)
    perspective2 = np.float32([[0, 0],[640, 0],[0, 70],[640, 70]])
    psp_matrix = cv2.getPerspectiveTransform(perspective1,perspective2)
    img_psp = cv2.warpPerspective(img_cri01, psp_matrix,(640,70))

    # 表示
#    cv2.imshow("psp", img_psp)
    
#    cv2.waitKey(0)
    cv2.imwrite("./short04/{0:05d}.png".format(num), img_psp)
#    cv2.destroyAllWindows()

for x in range(1,650):
	makeimg(x)
"""
totalkey = [[0,[]]]
filename1 = "./out00/{0:02d}.png".format(1)
for x in range(2,55):
    onetime = []
    filename2 = "./out00/{0:02d}.png".format(x)
    data = test(filename1,filename2)
    if data[0]:
        if x-1 != totalkey[-1][0]:
            print(x)
            for i in data[1]:
                onetime.append(KeyNameList[i])
                filename1 = "./out00/{0:02d}.png".format(x)
                totalkey.append([x,onetime])
print(totalkey)
"""
