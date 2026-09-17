"""Deterministic illustrated EEG finger-control explainer. No real EEG or device data."""
from pathlib import Path
from functools import lru_cache
import argparse
import json
import math
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
from typography import font

W, H, FPS, DURATION = 1920, 1080, 30, 20
INK, BLUE, MINT, CREAM = '#17282E', '#2851ED', '#B4F4D3', '#F7F3E9'
LILAC, CORAL, WHITE, GRAY = '#EEE8FA', '#FA795B', '#FFFFFF', '#51646A'

def clamp(x): return max(0., min(1., x))
def smooth(x):
    x = clamp(x)
    return x*x*(3-2*x)
def ease(t, start=0, dur=.6): return 1-(1-clamp((t-start)/dur))**3
def lerp(a,b,p): return a+(b-a)*p
def rr(d,box,fill,r=24,outline=None,width=1): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def tx(d,x,y,s,size=32,color=INK,bold=False,latin=False):
    d.text((round(x),round(y)),s,font=font(size,bold,latin),fill=color,anchor='lt')

@lru_cache(maxsize=180)
def word(s,size,color,bold=False,latin=False):
    f=font(size,bold,latin)
    im=Image.new('RGBA',(math.ceil(f.getlength(s))+10,math.ceil(size*1.5)+12))
    tx(ImageDraw.Draw(im),4,4,s,size,color,bold,latin)
    return im

def put(im,ob,x,y,p=1):
    if p<=0:return
    if p<.999:
        ob=ob.copy(); ob.putalpha(ob.getchannel('A').point(lambda a:round(a*p)))
    im.alpha_composite(ob,(round(x),round(y)))

def label(im,x,y,s,size=32,color=INK,bold=False,latin=False,p=1):
    put(im,word(s,size,color,bold,latin),x,y+28*(1-p),p)

def pill(im,x,y,s,bg=INK,fg=WHITE,size=24):
    d=ImageDraw.Draw(im); width=round(font(size).getlength(s))+44
    rr(d,(x,y,x+width,y+size+30),bg,(size+30)//2)
    tx(d,x+22,y+14,s,size,fg)

@lru_cache(maxsize=4)
def background(n):
    colors=[CREAM,BLUE,LILAC,MINT]
    im=Image.new('RGBA',(W,H),colors[n]); d=ImageDraw.Draw(im)
    if n==0:
        d.ellipse((980,-260,2160,950),fill='#CBEFD8')
        d.ellipse((1110,20,1900,920),outline='#A2C4B0',width=2)
    elif n==1:
        for r in (220,390,570):d.ellipse((1090-r,560-r*.73,1090+r,560+r*.73),outline='#5B7AF2',width=2)
    elif n==2:
        d.ellipse((-280,440,760,1420),fill='#DBCEF3')
    else:
        d.ellipse((1420,-230,2290,640),outline='#8ECDAD',width=2)
    return im

def footer(im,n,light=False):
    c='#D4DEFF' if light else GRAY
    label(im,80,1022,'Ding et al.  |  Nature Communications 2025',20,c,latin=True)
    label(im,1478,1022,f'0{n+1} / EEG TO MOTION',19,c,latin=True)

def hand(t,active=0):
    """Four-digit conceptual robot; one active digit at a time, not device footage."""
    im=Image.new('RGBA',(740,850));d=ImageDraw.Draw(im)
    d.ellipse((150,748,685,820),fill='#87BCA7')
    rr(d,(310,690,478,785),INK,30)
    rr(d,(328,704,460,772),'#E2E9E4',20)
    rr(d,(255,455,562,700),INK,50)
    rr(d,(277,470,542,677),WHITE,40)
    rr(d,(299,490,520,560),'#E5ECE8',18)
    for k in range(3):d.line((309,590+k*21,506,590+k*21),fill='#C8D4D1',width=3)
    pulse=.5+.5*math.sin(t*2.8)
    d.ellipse((350,511,377,538),fill=BLUE)
    d.ellipse((389,511,416,538),fill=MINT)
    configs=[((278,580),[-2.42,-2.55,-2.6],[90,78,66]),((310,475),[-1.66,-1.67,-1.7],[100,91,75]),((408,465),[-1.57,-1.57,-1.57],[117,101,76]),((505,482),[-1.42,-1.4,-1.39],[99,86,70])]
    for i,(origin,angles,lens) in enumerate(configs):
        selected=i==active
        bend=(.12+.63*pulse) if selected else .02
        x,y=origin
        for j,(angle,length) in enumerate(zip(angles,lens)):
            a=angle+(bend*(j+1)*.52 if i else -bend*(j+1)*.38)
            nx=x+math.cos(a)*length;ny=y+math.sin(a)*length
            d.line((x,y,nx,ny),fill=INK,width=66)
            d.line((x,y,nx,ny),fill=BLUE if selected else '#E1E9E7',width=49)
            d.ellipse((x-28,y-28,x+28,y+28),fill=INK)
            d.ellipse((x-16,y-16,x+16,y+16),fill=MINT if selected else WHITE)
            d.line((x+7,y-7,nx+7,ny-7),fill='#809CF8' if selected else WHITE,width=5)
            x,y=nx,ny
        d.ellipse((x-30,y-30,x+30,y+30),fill=INK)
        d.ellipse((x-21,y-21,x+21,y+21),fill=MINT if selected else '#F8FBF8')
        if selected:
            rad=42+7*pulse
            d.ellipse((x-rad,y-rad,x+rad,y+rad),outline=CORAL,width=3)
    return im

def show_hand(im,t,cx,cy,scale=1,angle=0,active=0,p=1):
    ob=hand(t,active)
    if scale!=1:ob=ob.resize((round(740*scale),round(850*scale)),Image.Resampling.LANCZOS)
    if angle:ob=ob.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
    put(im,ob,cx-ob.width/2,cy-ob.height/2,p)

def trace(d,x,y,w,t,color=BLUE,amp=22,phase=0):
    pts=[]
    for j in range(0,round(w)+1,4):
        q=j/w
        v=math.sin(q*26-t*3+phase)*.62+math.sin(q*61-t*5+phase)*.25+math.sin(q*107+t*2)*.13
        pts.append((x+j,y+amp*v))
    d.line(pts,fill=color,width=4)

def scene1(t):
    im=background(0).copy();d=ImageDraw.Draw(im)
    pill(im,82,65,'EEG / FINGER CONTROL',INK,WHITE,22)
    label(im,77,223,'让想象，',112,INK,True,p=ease(t+.4,0))
    label(im,77,375,'动到指尖。',112,BLUE,True,p=ease(t+.4,.15))
    label(im,84,558,'无创脑电 · 单指级机器人控制',34,GRAY,p=ease(t,.3))
    label(im,86,728,'MIND → FINGER',31,INK,True,True,p=ease(t,.65))
    trace(d,88,827,667,t,BLUE,30)
    q=ease(t+.3,0,.95)
    show_hand(im,t,1435+260*(1-q),540,.99,-9,0,q)
    pill(im,1250,919,'同名手指映射 · 原创示意',WHITE,INK,24)
    d.ellipse((800,811,830,841),fill=CORAL)
    footer(im,0)
    return im

def scene2(t):
    im=background(1).copy();d=ImageDraw.Draw(im)
    label(im,80,72,'从脑电，到动作。',74,WHITE,True,p=ease(t,.0))
    label(im,85,191,'个体化 EEGNet + 同日微调',30,'#D6E2FF',p=ease(t,.2))
    label(im,77,349,'128',166,MINT,True,True,p=ease(t,.25))
    label(im,89,542,'通道 EEG',42,WHITE,True,p=ease(t,.35))
    for i in range(4): trace(d,89,671+i*50,484,t,'#A9DCCA',17,i)
    # Decoder core and animated neural connections.
    p=ease(t,0,.8);cx=1050;cy=545
    r=147*p
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=WHITE)
    if p>.8:
        label(im,930,505,'EEGNet',45,INK,True,True)
        label(im,966,574,'解码器',27,GRAY)
    d.line((608,555,879,555),fill='#91ADF9',width=4)
    d.line((1220,555,1380,555),fill='#91ADF9',width=4)
    for i in range(5):
        q=(t*.43+i*.21)%1
        x=lerp(610,876,q);d.ellipse((x-8,547,x+8,563),fill=MINT)
    for j,(x,y,s) in enumerate([(790,275,'时间特征'),(1160,264,'空间特征'),(918,806,'同日适配')]):
        q=ease(t,.45+j*.32)
        if q>0:
            yy=y+50*(1-q)
            rr(d,(x,yy,x+225,yy+82),MINT if j!=1 else '#CFC4FE',25)
            tx(d,x+40,yy+24,s,29,INK,True)
    show_hand(im,t,1580,551,.58,5,3,ease(t,.5))
    pill(im,1404,859,'对应手指动作',WHITE,INK,25)
    label(im,81,938,'波形与机器人均为方法示意',23,'#D4DEFF')
    footer(im,1,True)
    return im

def scene3(t):
    im=background(2).copy();d=ImageDraw.Draw(im)
    label(im,79,69,'连续更新，让反馈跟上意图。',61,INK,True,p=ease(t))
    label(im,75,237,'125',210,BLUE,True,True,p=ease(t,.1))
    label(im,479,381,'ms',69,BLUE,True,True,p=ease(t,.3))
    label(im,87,495,'机器人命令更新间隔',36,INK,True,p=ease(t,.3))
    label(im,87,581,'每次解码：最近 1 秒 EEG',29,GRAY,p=ease(t,.5))
    label(im,87,633,'试次开始 1 秒后提供反馈',29,GRAY,p=ease(t,.6))
    # A close-up, moving time window; synthetic signal is visibly labeled.
    rr(d,(848,236,1802,570),WHITE,34)
    tx(d,889,270,'滚动窗口 / 示意信号',26,GRAY)
    for row in range(3):trace(d,891,367+row*64,866,t,BLUE,21,row)
    sweep=895+int((t*.23)%1*609)
    overlay=Image.new('RGBA',(W,H));od=ImageDraw.Draw(overlay)
    rr(od,(sweep,325,sweep+226,539),(115,224,170,65),12)
    od.line((sweep+226,324,sweep+226,539),fill=CORAL,width=4)
    im=Image.alpha_composite(im,overlay);d=ImageDraw.Draw(im)
    for i in range(9):
        x=915+i*104
        d.line((x,694,x,724),fill='#9B90BE',width=2)
        if i<8:d.line((x,709,x+104,709),fill='#B7ACD0',width=3)
    selected=int(t*8)%8
    x=915+selected*104;d.ellipse((x-13,696,x+13,722),fill=BLUE)
    label(im,1004,752,'解码 → 选择手指 → 更新动作',31,INK,True,p=ease(t,.65))
    pill(im,86,854,'125 ms 更新 ≠ 125 ms 总延迟',INK,WHITE,25)
    pill(im,997,874,'在线微调，适配当天信号',BLUE,WHITE,25)
    footer(im,2)
    return im

def scene4(t):
    im=background(3).copy();d=ImageDraw.Draw(im)
    label(im,79,67,'想象单指运动，在线驱动机器人。',57,INK,True,p=ease(t))
    pill(im,85,184,'MI 在线试次准确率 · 训练与微调后',INK,WHITE,25)
    p=smooth((t-.1)/1.1)
    label(im,67,304,f'{80.56*p:.2f}',240,BLUE,True,True,p=ease(t,0,.25))
    label(im,835,458,'%',78,BLUE,True,True,p=ease(t,.25))
    label(im,87,587,'二分类 / 拇指 · 小指',40,INK,True,p=ease(t,.35))
    d.line((1048,301,1048,703),fill='#82BEA4',width=2)
    label(im,1151,347,f'{60.61*p:.2f}%',107,INK,True,True,p=ease(t,.25))
    label(im,1158,507,'三分类',33,INK,True,p=ease(t,.4))
    label(im,1158,565,'拇指 · 食指 · 小指',31,GRAY,p=ease(t,.5))
    rr(d,(1157,651,1799,675),'#DEF8E9',12)
    if p>0:rr(d,(1157,651,1157+642*.6061*p,675),BLUE,12)
    # Stable evidence boundary and closing identity band.
    label(im,87,728,'21 名经筛选、有 BCI 经验的健康参与者',30,INK,True,p=ease(t,.55))
    q=ease(t,.5,.65);y=863+217*(1-q)
    d.rectangle((0,y,W,H),fill=CREAM)
    label(im,79,y+36,'EEG → FINGER',61,INK,True,True)
    label(im,83,y+126,'方法演绎 · 试次多数投票准确率 · 尚非临床疗效验证',26,GRAY)
    label(im,1145,y+48,'Ding et al. / Nature Communications',25,INK,True,True)
    label(im,1148,y+100,'2025 · 16:5401',24,GRAY,latin=True)
    label(im,1148,y+148,'doi:10.1038/s41467-025-61064-x',22,GRAY,latin=True)
    return im

def frame(t):
    if t<3.6:im=scene1(t)
    elif t<4.3:
        p=smooth((t-3.6)/.7);mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask);r=2250*p
        d.ellipse((1450-r,525-r,1450+r,525+r),fill=255)
        im=Image.composite(scene2(max(0,t-3.7)),scene1(t),mask)
    elif t<9.35:im=scene2(t-3.7)
    elif t<10.1:
        p=smooth((t-9.35)/.75);mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
        cx=lerp(1090,960,p);cy=lerp(545,540,p);rw=1300*p;rh=1000*p
        d.rounded_rectangle((cx-rw,cy-rh,cx+rw,cy+rh),radius=round(80*(1-p)),fill=255)
        im=Image.composite(scene3(max(0,t-9.5)),scene2(t-3.7),mask)
    elif t<14.2:im=scene3(t-9.5)
    elif t<14.95:
        p=smooth((t-14.2)/.75);mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
        d.rectangle((0,0,W*p,H),fill=255)
        im=Image.composite(scene4(max(0,t-14.4)),scene3(t-9.5),mask)
    else:im=scene4(t-14.4)
    return im.convert('RGB')

def make_audio(out):
    sr=48000;n=sr*DURATION;sound=np.zeros((n,2));rng=np.random.default_rng(71)
    def mix(start,sig,pan=0):
        pos=round(start*sr);count=min(len(sig),n-pos)
        gains=np.array([math.cos((pan+1)*math.pi/4),math.sin((pan+1)*math.pi/4)])
        sound[pos:pos+count]+=sig[:count,None]*gains
    for start,dur,notes in [(0,4,[146.83,220,293.66]),(4,5.5,[130.81,196,261.63]),(9.5,5,[164.81,220,329.63]),(14.5,5.5,[146.83,220,293.66,440])]:
        t=np.arange(round(dur*sr))/sr;env=np.minimum(1,t/.6)*np.maximum(0,np.minimum(1,(dur-t)/.8))
        mix(start,.026*env*sum(np.sin(2*np.pi*f*t) for f in notes)/len(notes))
    for k,start in enumerate([.35,.9,1.55,3.7,4.2,4.6,5.,5.5,9.6,10.2,10.8,11.4,12.,14.5,15.,15.6,16.4,17.3]):
        dur=.38 if start<17 else 1.25;t=np.arange(round(dur*sr))/sr
        env=(1-np.exp(-t*250))*np.exp(-t*9)*np.sin(np.pi*t/dur)**.4
        mix(start,.075*env*(np.sin(2*np.pi*(520+k%4*110)*t)+.15*np.sin(2*np.pi*1540*t)),(-.4,.4)[k%2])
    for start in [3.55,9.3,14.15]:
        t=np.arange(round(.75*sr))/sr;noise=np.convolve(rng.standard_normal(len(t)),np.ones(18)/18,'same')
        mix(start,.075*noise*np.sin(np.pi*t/.75)**2)
    sound[:2400]*=np.linspace(0,1,2400)[:,None]
    sound[-48000:]*=(np.linspace(1,0,48000)**2)[:,None]
    sound*=.29/np.max(np.abs(sound));pcm=np.rint(sound*32767).astype('<i2')
    path=out/'soundtrack.wav'
    with wave.open(str(path),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
    return path

def preview(out):
    times=[2.4,7.2,12.1,18.5];sheet=Image.new('RGB',(1920,1160),'#E5E6DF');d=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        im=frame(t);im.save(out/f'scene-{i+1}.png')
        x=i%2*960;y=i//2*580
        tx(d,x+18,y+12,f'0{i+1} / {t:.1f} s',22,INK,latin=True)
        sheet.paste(im.resize((960,540),Image.Resampling.LANCZOS),(x,y+40))
    sheet.save(out/'storyboard.png')
    print(out/'storyboard.png',flush=True)

def render(out):
    wav=make_audio(out);mp4=out/'eeg-finger-control-20s.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
    args=[ff,'-y','-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(DURATION),'-movflags','+faststart',str(mp4)]
    with (out/'encode.log').open('w') as log:
        p=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
        try:
            for i in range(FPS*DURATION):
                p.stdin.write(frame(i/FPS).tobytes())
                if i%60==0:print(f'Rendered {i}/{FPS*DURATION}',flush=True)
            p.stdin.close()
            if p.wait()!=0:raise RuntimeError('FFmpeg failed; see encode.log')
        except BaseException:p.kill();p.wait();raise
    print(mp4,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--output',type=Path,default=Path.cwd()/'motion-output');a=p.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    preview(out) if a.preview else render(out)
