# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
from PIL import Image, ImageOps


def get_yy(num):
    img_src1 = cv2.imread("data/img/result/{0:03d}.jpg".format(num), 1)
    img_src2 = cv2.imread("data/img/result/{0:03d}.jpg".format(num+10), 1)

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
    for y in range(len(dst_gray)):
        count = 0
        for x in dst_gray[y]:
            if x != 0:
                count += 1
        if count > 20:
            yy = y
            break
    return yy


def make_img(num, ydata):
    answers = []
    # 画像の読み込み
    img_src1 = cv2.imread("data/img/result/{0:03d}.jpg".format(num), 1)
    yy = ydata
    img_cri01 = img_src1[yy+5:yy+75, 0:640]
    cri_gray = cv2.cvtColor(img_cri01, cv2.COLOR_RGB2GRAY)
    cri_edge = cv2.Canny(cri_gray, 100, 100, True)
    point = [[4, 0], [635, 0], [11, 70], [627, 70]]
    perspective1 = np.float32(point)
    perspective2 = np.float32([[0, 0], [640, 0], [0, 70], [640, 70]])
    psp_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
    img_psp = cv2.warpPerspective(img_cri01, psp_matrix, (640, 70))

    cv2.imwrite("data/img/result02/{0:03d}.jpg".format(num), img_psp)

ydata = get_yy(1)
for x in range(600):
    make_img(x, ydata)