"""Inspect an encoded MP4, decode it fully, and export review artifacts.

Example:
  python verify_mp4.py movie.mp4 --duration 20 --size 1920x1080 --fps 30 \
      --require-audio --times 0,4,10,15,19.96 --output ./qa

Dependencies: Pillow, NumPy, and FFmpeg (PATH, --ffmpeg, or imageio-ffmpeg).
Exit 0 means technical checks passed; visual review and listening remain manual.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def ffmpeg_path(explicit):
    if explicit:return str(Path(explicit).resolve())
    found=shutil.which('ffmpeg')
    if found:return found
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def run(exe,args):
    result=subprocess.run([exe,*args],capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8',errors='replace'))
    return result

def metadata(ff,video,out):
    result=subprocess.run([ff,'-hide_banner','-i',str(video)],capture_output=True)
    raw=result.stderr.decode('utf-8',errors='replace')
    (out/'metadata.txt').write_text(raw,encoding='utf-8')
    probe=shutil.which('ffprobe')
    sibling=Path(ff).with_name('ffprobe.exe' if Path(ff).suffix=='.exe' else 'ffprobe')
    if not probe and sibling.is_file():probe=str(sibling)
    if probe:
        data=json.loads(run(probe,['-v','error','-show_format','-show_streams','-of','json',str(video)]).stdout)
        (out/'ffprobe.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
        v=next(s for s in data['streams'] if s['codec_type']=='video')
        audio=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
        return {'duration':float(data['format']['duration']),'width':v['width'],'height':v['height'],
                'fps':float(Fraction(v['avg_frame_rate'] or v['r_frame_rate'])),
                'video_codec':v['codec_name'],'pixel_format':v.get('pix_fmt'),
                'audio':None if audio is None else {'codec':audio['codec_name'],'sample_rate':int(audio['sample_rate']),'channels':audio['channels']},'metadata_source':'ffprobe'}
    duration=re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)',raw)
    vl=next((s for s in raw.splitlines() if 'Video:' in s),'')
    size=re.search(r'\b(\d{2,5})x(\d{2,5})\b',vl)
    fps=re.search(r'(\d+(?:\.\d+)?) fps',vl)
    if not duration or not size or not fps:raise ValueError('Cannot determine duration, video size, or fps from FFmpeg metadata. Supply ffprobe for this file.')
    al=next((s for s in raw.splitlines() if 'Audio:' in s),'')
    ac=re.search(r'Audio:\s*([^ ,]+)',al);ar=re.search(r'(\d+) Hz',al)
    vc=re.search(r'Video:\s*([^ ,]+)',vl)
    return {'duration':3600*int(duration[1])+60*int(duration[2])+float(duration[3]),
            'width':int(size[1]),'height':int(size[2]),'fps':float(fps[1]),'video_codec':vc[1] if vc else None,
            'pixel_format':'yuv420p' if 'yuv420p' in vl else 'see metadata.txt',
            'audio':None if not al else {'codec':ac[1] if ac else None,'sample_rate':int(ar[1]) if ar else None,'channels':2 if 'stereo' in al else 1 if 'mono' in al else 'see metadata.txt'},
            'metadata_source':'ffmpeg stderr (rounded display values)'}

def contact_sheet(ff,video,out,indices,fps):
    expr='+'.join(f'eq(n,{i})' for i in indices)
    run(ff,['-y','-v','error','-i',str(video),'-vf',f"select='{expr}'",'-fps_mode','vfr',str(out/'frame-%03d.png')])
    columns=min(4,len(indices));cw,ch=480,315
    sheet=Image.new('RGB',(cw*columns,ch*math.ceil(len(indices)/columns)),'#EEECE5')
    d=ImageDraw.Draw(sheet)
    for i,n in enumerate(indices):
        p=out/f'frame-{i+1:03d}.png'
        if not p.is_file():raise RuntimeError(f'Missing selected frame {n}')
        with Image.open(p) as im:
            im=im.convert('RGB');im.thumbnail((480,270),Image.Resampling.LANCZOS)
            x=(i%columns)*cw;y=(i//columns)*ch
            d.text((x+12,y+10),f'{n/fps:.2f} s | frame {n}',font=ImageFont.load_default(size=20),fill='#172528')
            sheet.paste(im,(x+(480-im.width)//2,y+42+(270-im.height)//2))
    sheet.save(out/'contact-sheet.png')

def audio_report(ff,video,out,duration):
    # Bounded raw file avoids buffering an entire long audio stream in memory.
    raw=out/'decoded-audio.f32'
    run(ff,['-y','-v','error','-i',str(video),'-map','0:a:0','-t',str(duration),'-f','f32le','-acodec','pcm_f32le','-ac','2','-ar','48000',str(raw)])
    if raw.stat().st_size==0:raise ValueError('Audio stream decoded to no samples.')
    signal=np.memmap(raw,dtype='<f4',mode='r').reshape(-1,2)
    peak=0.;total=0.;full=0;finite=True
    for start in range(0,len(signal),48000):
        block=np.asarray(signal[start:start+48000],dtype=np.float64)
        finite=finite and bool(np.isfinite(block).all())
        peak=max(peak,float(np.abs(block).max()));total+=float(np.sum(block*block))
        full+=int(np.count_nonzero(np.abs(block)>=1))
    result={'analysis_sample_rate':48000,'analysis_channels':2,'decoded_samples':len(signal),'finite':finite,
            'peak_dbfs':20*math.log10(max(1e-12,peak)),
            'rms_dbfs':20*math.log10(max(1e-12,math.sqrt(total/signal.size))),
            'samples_at_or_above_full_scale':full,
            'final_100ms_rms_dbfs':20*math.log10(max(1e-12,float(np.sqrt(np.mean(np.asarray(signal[-4800:],dtype=np.float64)**2))))),
            'listening_review':'pending'}
    im=Image.new('RGB',(1600,430),'#F5F2E9');d=ImageDraw.Draw(im)
    d.text((24,14),'Encoded audio waveform (stereo analysis)',font=ImageFont.load_default(size=25),fill='#172528')
    for ch in range(2):
        center=135+ch*165
        d.line((40,center,1560,center),fill='#AFBEB5')
        for x in range(1520):
            chunk=signal[int(x*len(signal)/1520):int((x+1)*len(signal)/1520),ch]
            v=float(np.abs(chunk).max()) if len(chunk) else 0
            v=min(1,v)*65/max(.05,peak)
            d.line((40+x,center-v,40+x,center+v),fill='#254CED' if ch==0 else '#44816C')
    d.text((40,397),f'0 s                                         {duration:.3f} s total',font=ImageFont.load_default(size=18),fill='#172528')
    im.save(out/'waveform.png')
    del chunk,signal
    raw.unlink()
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video',type=Path);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--duration',type=float);ap.add_argument('--size');ap.add_argument('--fps',type=float)
    ap.add_argument('--require-audio',action='store_true');ap.add_argument('--times',default='')
    ap.add_argument('--ffmpeg')
    args=ap.parse_args()
    video=args.video.resolve();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if not video.is_file():raise FileNotFoundError(video)
    ff=ffmpeg_path(args.ffmpeg);info=metadata(ff,video,out);errors=[]
    if args.duration is not None and abs(info['duration']-args.duration)>1/info['fps']+.01:errors.append('Duration differs from expected value.')
    if args.size:
        w,h=map(int,args.size.lower().split('x'))
        if (info['width'],info['height'])!=(w,h):errors.append('Dimensions differ from expected value.')
    if args.fps is not None and abs(info['fps']-args.fps)>.02:errors.append('Frame rate differs from expected value.')
    if args.require_audio and info['audio'] is None:errors.append('Required audio stream is absent.')
    decoded=run(ff,['-v','error','-i',str(video),'-map','0:v:0','-map','0:a?','-progress','pipe:1','-f','null','-'])
    progress=decoded.stdout.decode('utf-8',errors='replace');(out/'decode.txt').write_text(progress,encoding='utf-8')
    counts=re.findall(r'frame=(\d+)',progress)
    if not counts:raise ValueError('No decoded frame count was reported.')
    n=int(counts[-1])
    if decoded.stderr.strip():errors.append('FFmpeg reported decode errors: '+decoded.stderr.decode('utf-8',errors='replace'))
    if args.duration is not None and args.fps is not None and n!=round(args.duration*args.fps):errors.append('Decoded frame count differs from rounded duration * fps.')
    times=[float(t) for t in args.times.split(',')] if args.times else np.linspace(0,max(0,(n-1)/info['fps']),12).tolist()
    indices=sorted(set([0,n-1]+[max(0,min(n-1,round(t*info['fps']))) for t in times]))
    contact_sheet(ff,video,out,indices,info['fps'])
    measured=audio_report(ff,video,out,info['duration']) if info['audio'] else None
    if measured and (not measured['finite'] or measured['samples_at_or_above_full_scale']):errors.append('Decoded audio contains non-finite or full-scale samples.')
    report={'file':str(video),'bytes':video.stat().st_size,**info,'decoded_frames':n,
            'sampled_frame_indices':indices,'audio_analysis':measured,'technical_pass':not errors,'errors':errors,
            'visual_review':'pending: inspect contact-sheet.png and full-resolution frames',
            'audio_review':'pending: listen or accurately report waveform-only inspection' if measured else 'no audio stream'}
    (out/'verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if not errors else 2

if __name__=='__main__':
    sys.exit(main())
