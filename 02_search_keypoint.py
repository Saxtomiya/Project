# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
from PIL import Image, ImageOps


def search_white():#手が映っていない(=鍵盤の白率が高い)画像を検索
    result = 0
    Max = 0
    for i in range(10):
        count = 0
        img_src = cv2.imread("data/img/02crip/{0:03d}.jpg".format(i), 1)
        gray = cv2.cvtColor(img_src, cv2.COLOR_RGB2GRAY)
        for y in gray:
            for x in y:
                if x >= 230:
                    count += 1
        if count >= Max:
            Max = count
            result = i
    return result

def search_key(num):#画像の色を見て鍵盤の境目の座標を検索
    img_src = cv2.imread("data/img/02crip/{0:03d}.jpg".format(data), 1)
    gray = cv2.cvtColor(img_src, cv2.COLOR_RGB2GRAY)
    check = []
    for x in range(len(gray[0])):
        value = 0
        for y in range(len(gray)):
            value += gray[y][x]
        check.append(value)
    check2 = []
    time = 0
    for x in range(len(check)-3):
        if time > 0:
            time -= 1
        else:
            a = check[x-1]
            b = check[x+1]
            if abs(a-b) >= 2000:
                check2.append(x)
                time += 35
    check2.sort()
    for i in range(len(check2)-1):#色合いがかぶっているE,Fの境目を作成
        abs2 = abs(check2[i]-check2[i+1])
        if abs2 >= 30:
            check2.append(abs2//2+check2[i])
    check2.sort()
    return check2

#デバッグ用、鍵盤の分かれ目を表示
"""    for y in range(len(gray)):
        for x in range(len(gray[y])):
            if gray[y][x] >= 100:
                gray[y][x] -= 100
            if x in check2:
                gray[y][x] = 255

    print(check2)
    cv2.imshow("", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""

data = search_white()
keypoint = search_key(data)

f = open('data/keylist.txt','w')
for i in keypoint:
    f.write(str(i)+",")
f.close()