# -*- coding: UTF-8 -*-

import cv2
import math
import numpy as np
import os
import copy
import pretty_midi
from PIL import Image, ImageOps

if os.path.exists("data/img/02crip"):
    pass
else:
    os.makedirs("data/img/02crip")
if os.path.exists("data/img/01image"):
    pass
else:
    os.makedirs("data/img/01image")
"""
filename = "Project.mp4"
print("file name >>Project.mp4")
"""
filename = input("input file name>>")

KeyNameList = [
"C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
"C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
"C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
"C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
"C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
"C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8",
"C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9", "A9", "A#9", "B9"]


#動画をフレームごとの画像に変換する関数
def save_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return


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


def get_point(num, yy):#鍵盤を縦にまっすぐに変換するための4点を取得する関数
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
    result = img_psp[0:100, 100:1180]\

    base_path = os.path.join("data/img/02crip/", "")
    cv2.imwrite('{}{}.jpg'.format(base_path, str(num).zfill(3)), result)


def search_white():#手が映っていない画像を検索する関数(鍵盤の境目を判断するのに用いる)
    result = 1
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


def search_key(num):#画像の色を見て鍵盤の境目の座標を検索する関数
    img_src = cv2.imread("data/img/02crip/{0:03d}.jpg".format(num), 1)
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
        if countd > 150:##判定値
            if len(checkdist) == 0:
                checkdist.append(x)
            else:
                valuec = checkdist.pop()
                if valuec == x or valuec+1 == x or valuec+2 == x:
                    checkdist.append(x)
                else:
                    checkdist.append(valuec)
                    checkdist.append(x)

    for i in range(len(checkdist)):#修正値
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


print("Start Program...")

# 動画をフレームに分解
save_frames('{}'.format(filename), 'data/img/01image', '')
print("makeing img is finished")

# 鍵盤の位置を推定、切り抜いたものを出力
ydata = get_yy(100)
#point = get_point(1, ydata)
point = [[5, 0], [1030, 0], [0, 100], [1038, 100]]
for x in range(464):
    make_img(x, ydata, point)
print("exchanging img is finished")

# 各鍵盤の座標を検索、出力
data = search_white()
keypoint = search_key(data)
f = open('data/keylist.txt', 'w')
for i in keypoint:
    f.write(str(i)+",")
f.close()
print("searching keypoint is finished")

# 動画から押された鍵盤を推定、出力
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

data = []
f = open('data/score.txt', 'r')
line = f.readline()
while line:
    l = list(line.rsplit(','))
    l.pop()
    data.append(l)
    line = f.readline()
f.close()

pushing = []
for x in range(len(data)):# 鍵盤を話した際にとれた差分を消去
    delete = []
    append = []
    for y in data[x]:
        if y in pushing:
            delete.append(y)
        else:
            append.append(y)
    for i in delete:
        data[x].remove(i)
        pushing.remove(i)
    for j in append:
        pushing.append(j)
for x in data:
    if data[0] == []:
        data.remove([])
    else:
        break


tmp = 250
pm = pretty_midi.PrettyMIDI(resolution=960, initial_tempo=tmp)# pretty_midiオブジェクトを作成
instrument = pretty_midi.Instrument(0)
time = (tmp/60)*2
for i in range(len(data)):
    for j in data[i]:
        note_number = pretty_midi.note_name_to_number(j)
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=i/time, end=(i+2)/time)
        instrument.notes.append(note)
pm.instruments.append(instrument)

pm.write('Output.mid') #midiファイルを書き込み
print("All Program is Finished")