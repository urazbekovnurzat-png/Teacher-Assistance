import ctypes as C, wave, subprocess, pathlib, espeakng_loader
P=pathlib.Path(__file__).parent
lib=C.CDLL(espeakng_loader.get_library_path())
lib.espeak_Initialize.argtypes=[C.c_int,C.c_int,C.c_char_p,C.c_int]
sr=lib.espeak_Initialize(2,0,str(pathlib.Path(espeakng_loader.get_data_path()).parent).encode(),0)
if sr<1:raise RuntimeError('Cannot initialize speech')
lib.espeak_SetVoiceByName(b'ru')
lib.espeak_SetParameter(1,155,0)
chunks=[]
CB=C.CFUNCTYPE(C.c_int,C.POINTER(C.c_short),C.c_int,C.c_void_p)
@CB
def callback(wav,count,events):
 if wav and count:chunks.append(C.string_at(wav,count*2))
 return 0
lib.espeak_SetSynthCallback(callback)
texts=[
'Закон всемирного тяготения. Физика, девятый класс. Почему тела притягиваются?',
'Любые два тела притягиваются. Земля притягивает яблоко, а яблоко притягивает Землю. Эти силы равны по модулю.',
'По закону Ньютона сила равна произведению гравитационной постоянной и масс двух тел, делённому на квадрат расстояния между их центрами.',
'Массы измеряют в килограммах, расстояние между центрами в метрах, а силу в ньютонах. Используем систему СИ.',
'Увеличим одну массу в два раза. Сила тоже вырастет вдвое. Если увеличить обе массы вдвое, сила вырастет в четыре раза.',
'Увеличим расстояние в два раза. Сила уменьшится в четыре раза. Если расстояние увеличить втрое, сила уменьшится в девять раз.',
'Решим задачу. Масса каждого тела тысяча килограммов. Расстояние между центрами десять метров. Считаем тела точечными.',
'Подставим данные в формулу. Тысячу умножаем на тысячу и делим на сто. Ответ: шесть целых шестьдесят семь сотых, умножить на десять в минус седьмой степени ньютонов.',
'Проверь себя. Расстояние между телами уменьшили в два раза. Как изменилась сила притяжения? Останови видео и подумай.',
'Сила выросла в четыре раза. Запомни: увеличение массы усиливает притяжение, а увеличение расстояния ослабляет его.'
]
durations=[7,8,10,8,8,8,8,10,9,8]
for i,(text,dur) in enumerate(zip(texts,durations)):
 chunks.clear();data=text.encode()+b'\0'
 lib.espeak_Synth(data,len(data),0,0,0,1,None,None)
 lib.espeak_Synchronize()
 raw=P/f'speech_{i}.wav'
 with wave.open(str(raw),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(chunks))
 seconds=sum(map(len,chunks))/2/sr
 rate=max(1,seconds/(dur-.4))
 filters=[]
 while rate>2:filters.append('atempo=2');rate/=2
 filters.extend([f'atempo={rate}',f'apad',f'atrim=duration={dur}'])
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(raw),'-af',','.join(filters),'-ar','44100',str(P/f'part_{i}.wav')],check=True)
 print(i,round(seconds,1),flush=True)
(P/'audio.txt').write_text(''.join(f"file 'part_{i}.wav'\n" for i in range(10)))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(P/'audio.txt'),'-i',str(P/'Gravity_Lesson.mp4'),'-map','1:v','-map','0:a','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(P/'Gravity_Lesson_Voice.mp4')],check=True)
