# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
from PIL import Image, ImageOps


def get_yy(num):#差分から鍵盤の位置を切り抜く関数
    img_src1 = cv2.imread("data/img/01image/{0:03d}.jpg".format(num), 1)
    img_src2 = cv2.imread("data/img/01image/{0:03d}.jpg".format(num+200), 1)

    img_diff = cv2.absdiff(img_src2, img_src1)
    # 差分を二値化
    img_diffm = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)[1]
    # 膨張処理、収縮処理を施してマスク画像を生成
    operator = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_diffm, operator, iterations=4)
    img_mask = cv2.erode(img_dilate, operator, iterations=4)
    # マスク画像を使って対象を切り出す
    img_dst = cv2.bitwise_and(img_src2, img_mask)
    dst_gray = cv2.cvtColor(img_dst, cv2.COLOR_RGB2GRAY)
    yy = 0
    for y in range(len(dst_gray)):#切り出された場所から鍵盤のy座標を取得
        count = 0
        for x in dst_gray[y]:
            if x != 0:
                count += 1
        if count > 10:
            yy = y
            break
    return yy


def get_point(num, yy):#鍵盤を縦にまっすぐに変換するための4点を取得
    point = [[0, 0], [0, 0], [0, 100], [0, 100]]#4点の座標を格納
    R1 = 0
    L1 = 0
    R2 = 0
    L2 = 0
    img_src = cv2.imread("data/img/01image/{0:03d}.jpg".format(num), 1)
    crip = img_src[yy+5:yy+105, 100:1180]
    gray = cv2.cvtColor(crip, cv2.COLOR_RGB2GRAY)
    edge = cv2.Canny(gray, 180, 250, True)
    for x in range(len(edge[0])-30):#エッジ検出を用いて鍵盤の角度を推定
        if edge[0][x] != 0:
            if point[0][0] == 0:
                point[0][0] = x
            point[1][0] = x
    for y in range(2, len(edge)):#どれだけ斜めになっているか判定
        if edge[y][point[0][0]] != 0:
            L1 += 1
        if edge[y][point[1][0]] != 0:
            R1 += 1
    for i in range(point[0][0], 300):
        if edge[98][i] != 0:
            L2 += 1
            if L1 == L2:
                point[2][0] = i
                break
    for i in range(300):
        if edge[98][1079-i] != 0:
            R2 += 5
            if R1 <= R2:
                point[3][0] = 1079-i
                break
    return point


def make_img(num, yy, point):#画像をクリッピング、射影変換する関数。
    answers = []
    # 画像の読み込み
    img_src1 = cv2.imread("data/img/01image/{0:03d}.jpg".format(num), 1)
    img_cri01 = img_src1[yy+5:yy+105, 100:1180]
    cri_gray = cv2.cvtColor(img_cri01, cv2.COLOR_RGB2GRAY)
    cri_edge = cv2.Canny(cri_gray, 100, 100, True)
    perspective1 = np.float32(point)
    perspective2 = np.float32([[100, 0], [1180, 0], [100, 100], [1180, 100]])
    psp_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
    img_psp = cv2.warpPerspective(img_cri01, psp_matrix, (1280, 100))
    result = img_psp[0:100, 100:1180]
    cv2.imwrite("data/img/02crip/{0:03d}.jpg".format(num), result)#result02に変換した画像を保存


def main():
    ydata = get_yy(100)
    point = get_point(1, ydata)
    for x in range(464):
        make_img(x, ydata, point)
    print("exchanging img is finished")