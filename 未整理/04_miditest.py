import pretty_midi
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
for x in range(len(data)):#鍵盤を話した際にとれた差分を消去
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
pm = pretty_midi.PrettyMIDI(resolution=960, initial_tempo=tmp) #pretty_midiオブジェクトを作成
instrument = pretty_midi.Instrument(0) 
instrument2 = pretty_midi.Instrument(1)
time = (tmp/60)*2
for i in range(len(data)):
    for j in data[i]:
        note_number = pretty_midi.note_name_to_number(j)
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=i/time, end=(i+2)/time)
        instrument.notes.append(note)
pm.instruments.append(instrument)

pm.write('output/test.mid') #midiファイルを書き込み
