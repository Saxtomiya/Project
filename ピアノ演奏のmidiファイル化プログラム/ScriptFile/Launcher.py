import s00_make_img as s00
import s01_img_exchanged as s01
import s02_search_keypoint as s02
import s03_mov_to_keyname as s03
import s04_make_midi as s04
import os

#filename = input("input the filename >>")
filename = "Test.mp4"
print("Program Start")
if os.path.exists("data/img/02crip"):
    pass
else:
    os.makedirs("data/img/02crip")
if os.path.exists("data/img/01image"):
    pass
else:
    os.makedirs("data/img/01image")
s00.main(filename)
s01.main()
s02.main()
s03.main()
s04.main()
