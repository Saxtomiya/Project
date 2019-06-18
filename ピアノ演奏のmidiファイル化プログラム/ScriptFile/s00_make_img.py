import cv2
import os

#動画をフレームごとの画像に変換する関数
def save_frames(video_path, dir_path, basename):
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
            cv2.imwrite('{}{}.jpg'.format(base_path, str(n).zfill(digit)), frame)
            n += 1
        else:
            return


def main(filename):
    save_frames('{}'.format(filename), 'data/img/01image', '')
    print("makeing img is finished")
