"""Russian grade 9 gravity lesson. Requires Python, Pillow and FFmpeg.
Run: python render.py. Produces Gravity_Lesson.mp4 (84 s, 1280x720).
"""
from PIL import Image, ImageDraw, ImageFont
import math, random, subprocess
from pathlib import Path
W,H,FPS=1280,720,15
OUT=Path(__file__).with_name('Gravity_Lesson.mp4')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s,b=False):return ImageFont.truetype(BOLD if b else FONT,s)
scenes=[
('Почему тела притягиваются?', ['ЗАКОН ВСЕМИРНОГО ТЯГОТЕНИЯ','Физика • 9 класс'], 'Земля притягивает яблоко. Яблоко тоже притягивает Землю.'),
('Любые два тела притягиваются', ['Притяжение действует между всеми телами.','Силы равны по модулю и противоположны.'], 'Тела действуют друг на друга вдоль линии между их центрами.'),
('Закон Ньютона', ['F = G · m₁ · m₂ / r²','G = 6,67 · 10⁻¹¹ Н·м²/кг²'], 'Формула применима к точечным телам и неперекрывающимся однородным шарам.'),
('Что означают величины?', ['m₁ и m₂ — массы тел, кг','r — расстояние между центрами, м'], 'F — сила притяжения в ньютонах. Все величины переводим в СИ.'),
('Больше масса — больше сила', ['Увеличим одну массу в 2 раза:','F станет в 2 раза больше.'], 'Если обе массы увеличить вдвое, сила увеличится в 4 раза.'),
('Дальше тела — слабее притяжение', ['Расстояние × 2  →  сила ÷ 4','Расстояние × 3  →  сила ÷ 9'], 'Сила обратно пропорциональна квадрату расстояния.'),
('Разберём задачу', ['m₁ = 1000 кг     m₂ = 1000 кг','r = 10 м. Найти F.'], 'Считаем тела точечными. Данные уже выражены в СИ.'),
('Подставим числа', ['F = 6,67 · 10⁻¹¹ · 1000 · 1000 / 10²','F = 6,67 · 10⁻⁷ Н'], 'Между обычными предметами притяжение очень мало.'),
('Проверь себя', ['Расстояние уменьшили в 2 раза.','Как изменилась сила притяжения?'], 'Останови видео и объясни ответ с помощью формулы.'),
('Ответ: сила выросла в 4 раза', ['F ∝ m₁ · m₂       F ∝ 1 / r²','Масса усиливает. Расстояние ослабляет.'], 'Ты умеешь объяснять закон и применять его для расчёта силы.')]
durations=[7,8,10,8,8,8,8,10,9,8]
D=sum(durations)
random.seed(9)
stars=[(random.randrange(W),random.randrange(H),random.choice([1,1,2])) for _ in range(95)]
base=Image.new('RGB',(W,H))
pix=base.load()
for y in range(H):
 for x in range(W):
  glow=max(0,1-math.hypot((x-1020)/950,(y-250)/650))
  pix[x,y]=(int(8+7*glow),int(15+18*glow),int(32+28*glow))
d=ImageDraw.Draw(base)
for x,y,r in stars:d.ellipse((x,y,x+r,y+r),fill=(62,83,116))
def centered(d,text,y,size,color='#eff6ff',bold=False):
 f=font(size,bold); box=d.textbbox((0,0),text,font=f);d.text(((W-(box[2]-box[0]))/2,y),text,font=f,fill=color)
def arrow(d,x1,x2,y):
 d.line((x1,y,x2,y),fill='#65f3cf',width=5)
 sign=1 if x2>x1 else -1
 d.polygon([(x2,y),(x2-sign*15,y-8),(x2-sign*15,y+8)],fill='#65f3cf')
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)],stdin=subprocess.PIPE)
for n in range(D*FPS):
 t=n/FPS;start=0
 for s,duration in enumerate(durations):
  if t<start+duration:break
  start+=duration
 local=t-start
 im=base.copy();d=ImageDraw.Draw(im)
 d.text((55,32),'ФИЗИКА / 09',font=font(19,True),fill='#65f3cf')
 d.text((1100,32),f'{s+1:02d} / 10',font=font(19),fill='#a6bad6')
 title,lines,caption=scenes[s]
 centered(d,title,88,42,bold=True)
 gap=400+(100*min(local/4,1) if s==5 else 0)
 x1=(W-gap)/2;x2=(W+gap)/2;y=292
 r1=46+(14*min(local/3,1) if s==4 else 0);r2=46
 for x,r,col in [(x1,r1,'#4ba7ff'),(x2,r2,'#b797ff')]:
  for halo in range(14,0,-2):d.ellipse((x-r-halo,y-r-halo,x+r+halo,y+r+halo),outline='#1c354e',width=2)
  d.ellipse((x-r,y-r,x+r,y+r),fill=col)
  d.ellipse((x-r*.5,y-r*.55,x-r*.12,y-r*.17),fill='#d9edff')
 arrow(d,x1+r1+15,x1+r1+85,y);arrow(d,x2-r2-15,x2-r2-85,y)
 d.line((x1,y+78,x2,y+78),fill='#758ca8',width=2)
 centered(d,'r — между центрами',y+88,20,'#a6bad6')
 for j,line in enumerate(lines):centered(d,line,445+j*58,34 if len(line)<45 else 29,'#65f3cf' if j==0 else '#edf4ff',j==0)
 # Wrap explanatory captions within safe margins.
 words=caption.split();rows=['']
 for word in words:
  test=(rows[-1]+' '+word).strip()
  if d.textlength(test,font=font(22))>1140:rows.append(word)
  else:rows[-1]=test
 for j,row in enumerate(rows):centered(d,row,602+j*29,22,'#b4c5dc')
 d.rectangle((55,692,1225,696),fill='#26374d');d.rectangle((55,692,55+1170*n/(D*FPS-1),696),fill='#65f3cf')
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait():raise SystemExit('FFmpeg render failed')
print(f'{OUT}: {D} seconds, {W}x{H}, {FPS} fps')
