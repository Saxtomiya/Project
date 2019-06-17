# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
import pretty_midi
from PIL import Image, ImageOps


class FileData:
    def __init__(self, filename):
        self.mov = filename
        self.img = []
        self.y = 0
        self.KeyNameList = [
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
        "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
        "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8",
        "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9", "A9", "A#9", "B9"]

    # 動画をフレームごとの配列に変換する関数
    def make_frames(self):
        cap = cv2.VideoCapture(self.mov)
        if not cap.isOpened():
            print("File Not Found")
            return False
        n = 0
        while True:
            ret, frame = cap.read()
            if ret:
                self.img.append(frame)
                n += 1
            else:
                print("{} is inputed".format(self.mov))
                return True

    # 配列を画像として出力する関数
    def save_frame(self, dir_path):
        if os.path.exists(dir_path):
            pass
        else:
            os.makedirs(dir_path, exist_ok=True)
        base_path = os.path.join(dir_path, "")
        digit = 3
        for data in range(len(self.img)):
            cv2.imwrite('{}{}.jpg'.format(base_path, str(data).zfill(digit)), self.img[data])
            print('{}{}.jpg'.format(base_path, str(data).zfill(digit)))

    # 鍵盤のｙ座標を取得
    def crip_yy(self):
        for i in range(1, 100):
            diff = cv2.absdiff(self.img[i], self.img[i+1])
            # 差分を二値化
            diffm = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
            # 膨張処理、収縮処理を施してマスク画像を生成
            operator = np.ones((3, 3), np.uint8)
            dilate = cv2.dilate(diffm, operator, iterations=4)
            mask = cv2.erode(dilate, operator, iterations=4)
            # マスク画像を使って対象を切り出す
            img_dst = cv2.bitwise_and(self.img[i+1], mask)
            dst_gray = cv2.cvtColor(img_dst, cv2.COLOR_RGB2GRAY)
            for y in range(len(dst_gray)):
                count = 0
                for x in dst_gray[y]:
                    if x != 0:
                        count += 1
                if count > 10:
                    self.y = y
                    break
            for i in range(len(self.img)):
                self.img[i] = self.img[i][self.y+5:self.y+105, 100:1180]

    def go(self):
        while True:
            check = self.make_frames()
            if check:
                break
#        self.save_frame("file/01framedata/")
        # 全フレームを出力
        self.crip_yy()
        self.save_frame("file/02cripping/")
        # クリッピング後の全フレームを出力

data = FileData("Project.mp4")
data.go()