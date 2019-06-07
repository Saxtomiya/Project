import s00_make_img as s00
import s01_img_exchanged as s01
import s02_search_keypoint as s02
import s03_mov_to_keyname as s03
import s04_make_midi as s04

print("Program Start\nPrease wait about 2 min...\n")
s00.main("project.mp4")
s01.main()
s02.main()
s03.main()
s04.main()