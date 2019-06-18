# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
from PIL import Image, ImageOps
KeyNameList = [
"C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
"C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
"C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
"C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
"C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
"C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8",
"C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9", "A9", "A#9", "B9"]


def getname(num1, num2, check):
    answers = []
    # 画像の読み込み
    img_src1 = cv2.imread("data/img/02crip/{0:03d}.jpg".format(num1), 1)
    img_src2 = cv2.imread("data/img/02crip/{0:03d}.jpg".format(num2), 1)
    # 背景画像との差分を算出
    img_diff = cv2.absdiff(img_src2, img_src1)
    # 差分を二値化
    img_diffm = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)[1]
    # 膨張処理、収縮処理を施してマスク画像を生成
    operator = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_diffm, operator, iterations=4)
    img_mask = cv2.erode(img_dilate, operator, iterations=4)
    # マスク画像を使って対象を切り出す
    dst = cv2.bitwise_and(img_src2, img_mask)

    ylen = len(dst)
    xlen = len(dst[1])-50
    gray = cv2.cvtColor(img_src1, cv2.COLOR_RGB2GRAY)
    edge = cv2.Canny(gray, 180, 250, True)
    checkdist = []
    for x in range(xlen-10):
        countd = 0
        for y in range(ylen//2):
            if dst[y][x][0] != 0:
                dst[y][x] = [0, 0, 255]
                for i in range(10):
                    if dst[y][x+i][0] != 0:
                        countd += 1
        if countd > 140:##判定値
            if len(checkdist) == 0:
                checkdist.append(x)
            else:
                valuec = checkdist.pop()
                if valuec == x or valuec+1 == x or valuec+2 == x:
                    checkdist.append(x)
                else:
                    checkdist.append(valuec)
                    checkdist.append(x)

    for i in range(len(checkdist)):#探索座標の修正値
        checkdist[i] -= 10

    for i in range(len(gray)):
        for j in range(len(gray[i])):
            if gray[i][j] <= 120:
                gray[i][j] = 0
            else:
                gray[i][j] = 255

    for i in check:
        for y in dst:
            y[i][1] = 200
    keylist = []
    for a in checkdist:
        for b in range(len(check)):
            if a < check[b]:
                if b not in keylist:
                    keylist.append(b)
                    break
                else:
                    break

    for x in keylist:
        for y in range(len(dst)):
            for i in range(20):
                dst[y][check[x]+i][0] = 255

    deletelist = []
    for x in range(len(keylist)-1):
        if keylist[x]+1 == keylist[x+1]:
            deletelist.append(keylist[x+1])
    for x in deletelist:
        keylist.remove(x)

    for x in keylist:
        for y in range(len(dst)):
            for i in range(20):
                dst[y][check[x]+i] = [255, 255, 255]

    if keylist == []:
        return [False, keylist]
    else:
        #デバッグ用　差分の取れた場所と鍵盤を表示
#        cv2.imshow("dst", dst)
#        cv2.imshow("img_src1", img_src1)
#        cv2.imshow("img_src2", img_src2)
#       cv2.waitKey(0)
#        cv2.destroyAllWindows()
        return [True, keylist]


def main():
    numlist = []
    namelist = []
    one = 1
    f = open('data/keylist.txt', 'r')
    data = f.readline()
    check = data.split(",")
    check.pop()
    for x in range(len(check)):
        check[x] = int(check[x])
    f.close()

    for i in range(50, 400, 3):
        data = getname(one, i, check)
        onetime = []
        if data[0]:
            one = i
            for j in data[1]:
                onetime.append(KeyNameList[j])
        else:
            onetime.append(data[1])
        numlist.append(data[1])
        namelist.append(onetime)

    f = open('data/score.txt', 'w')
    for x in namelist:
        text = ""
        for y in x:
            if y != []:
                text += y
                text += ","
            f.write(text+"\n")
    f.close()
    print("getting keyname is finished")