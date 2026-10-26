"""Render the profile's custom, self-hosted animated banners.

Run from the repository root: python scripts/render_profile.py
Requires Pillow; no network calls or credentials.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
W = 1200
BG = '#080F1E'
PANEL = '#101C30'
LINE = '#24354F'
WHITE = '#EDF5FF'
MUTED = '#9EACC3'
CYAN = '#67E8F9'
PURPLE = '#B7A2FF'
TEAL = '#45DBBA'


def font(size, bold=False, mono=False):
    windows = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    family = 'DejaVuSansMono' if mono else 'DejaVuSans'
    candidates = [
        f'/usr/share/fonts/truetype/dejavu/{family}{"-Bold" if bold else ""}.ttf',
        str(windows / ('consola.ttf' if mono else 'arialbd.ttf' if bold else 'arial.ttf')),
        f'/Library/Fonts/{"Courier New" if mono else "Arial Bold" if bold else "Arial"}.ttf',
    ]
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def text(d, xy, value, size=16, color=WHITE, bold=False, mono=False):
    d.text(xy, value, font=font(size, bold, mono), fill=color)


def centered(d, cx, y, value, size=16, color=WHITE, bold=False, mono=False):
    f = font(size, bold, mono)
    width = d.textlength(value, font=f)
    d.text((cx - width / 2, y), value, font=f, fill=color)


def base(height, grid=False):
    im = Image.new('RGB', (W, height), BG)
    d = ImageDraw.Draw(im)
    if grid:
        for x in range(0, W, 40):
            d.line((x, 0, x, height), fill='#101A2C')
        for y in range(0, height, 40):
            d.line((0, y, W, y), fill='#101A2C')
    d.rounded_rectangle((1, 1, W - 2, height - 2), radius=22, outline=LINE, width=2)
    return im, d


def save(frames, name, duration):
    # A shared palette keeps colors stable across the animation.
    sheet = Image.new('RGB', (W, frames[0].height * min(8, len(frames))))
    for i, frame in enumerate(frames[:8]):
        sheet.paste(frame, (0, i * frame.height))
    palette = sheet.quantize(colors=96, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(OUT / name, save_all=True, append_images=indexed[1:], loop=0,
                    duration=duration, optimize=True, disposal=1)
    frames[0].save(OUT / name.replace('.gif', '-still.png'))
    print(name, (OUT / name).stat().st_size, 'bytes', len(frames), 'frames')


def hero():
    frames = []
    count = 48
    for i in range(count):
        t = i / count
        im, d = base(400, True)
        d.rounded_rectangle((36, 30, 170, 61), radius=8, fill='#122D3B', outline='#235467')
        text(d, (50, 37), 'RUPEN / 18', 14, CYAN, True, True)
        text(d, (38, 91), 'RUPENDRAN', 62, WHITE, True)
        text(d, (38, 164), 'MANIGANDAN', 62, WHITE, True)
        text(d, (41, 255), 'AI & ROBOTICS  /  SOFTWARE & SYSTEMS', 17, CYAN, mono=True)
        text(d, (41, 295), 'From computer vision to things that move.', 22, MUTED)
        d.line((42, 350, 370, 350), fill=LINE, width=2)
        d.line((42, 350, 125 + int(170 * (0.5 + 0.5 * math.sin(t * math.tau))), 350), fill=PURPLE, width=2)
        text(d, (41, 365), 'BUILDING AT THE INTERSECTION OF CODE AND HARDWARE', 11, MUTED, mono=True)

        cx, cy = 970, 188
        d.line((760, 44, 760, 353), fill=LINE)
        for r in (51, 88, 125):
            d.ellipse((cx-r, cy-r, cx+r, cy+r), outline='#224056', width=1)
        for angle in range(0, 360, 30):
            a = math.radians(angle)
            d.line((cx+120*math.cos(a),cy+120*math.sin(a),cx+125*math.cos(a),cy+125*math.sin(a)), fill='#3C5B70',width=2)
        a = t * math.tau - math.pi / 2
        for j in range(7):
            tail = a - j * .045
            end = (cx+123*math.cos(tail), cy+123*math.sin(tail))
            d.line((cx,cy,*end), fill=['#4EC7D9','#398797','#2D6979','#244F63','#203E54','#193149','#142940'][j], width=2)
        d.ellipse((cx-4, cy-4, cx+4, cy+4), fill=CYAN)
        d.ellipse((cx+92*math.cos(a)-5,cy+92*math.sin(a)-5,cx+92*math.cos(a)+5,cy+92*math.sin(a)+5),fill=PURPLE)

        # A compact line-art rover and articulated arm, drawn as a UI motif.
        d.rounded_rectangle((899, 206, 1041, 247), radius=12, fill=PANEL, outline=CYAN, width=2)
        for x in (919, 1021):
            d.ellipse((x-18,236,x+18,272),fill='#0E1A2B',outline=PURPLE,width=3)
            spin = a * 2
            for add in (0,math.pi/2):
                d.line((x-10*math.cos(spin+add),254-10*math.sin(spin+add),x+10*math.cos(spin+add),254+10*math.sin(spin+add)),fill='#7B79A8',width=2)
        d.rounded_rectangle((941,216,999,232),radius=4,fill='#153444')
        for x in range(950,992,10):
            d.line((x,220,x,228),fill='#31788B',width=2)
        joint=(970,204)
        elbow=(946 + 4*math.sin(a),158)
        wrist=(987 + 8*math.sin(a),121 + 3*math.cos(a))
        d.line((*joint,*elbow,*wrist),fill=WHITE,width=8,joint='curve')
        for x,y in (joint,elbow,wrist):
            d.ellipse((x-7,y-7,x+7,y+7),fill=PANEL,outline=CYAN,width=2)
        d.line((*wrist,1004+8*math.sin(a),109),fill=PURPLE,width=4)
        d.line((*wrist,1006+8*math.sin(a),131),fill=PURPLE,width=4)
        pulse=4+int(2*(1+math.sin(a)))
        d.ellipse((866-pulse,107-pulse,866+pulse,107+pulse),outline=TEAL,width=2)
        d.ellipse((863,104,869,110),fill=TEAL)
        centered(d,970,331,'PERCEIVE. REASON. ACT.',15,CYAN,mono=True)
        centered(d,970,360,'A ROBOTICS ENGINEERING JOURNEY',10,MUTED,mono=True)
        frames.append(im)
    save(frames,'hero.gif',90)


def terminal():
    lines = [
        ('building', 'Computer vision tools for real-world problems.'),
        ('exploring', 'Robotics, embedded systems, and automation.'),
        ('learning', 'C++, Python, and better problem-solving.'),
    ]
    frames=[]
    for label,message in lines:
        for k in range(24):
            im,d=base(132)
            d.line((22,35,W-22,35),fill=LINE)
            for x,color in [(28,'#FF7B84'),(47,'#F4C56B'),(66,'#45DBBA')]:
                d.ellipse((x,16,x+8,24),fill=color)
            text(d,(95,12),'rupen@workbench : ~',12,MUTED,mono=True)
            text(d,(30,56),'$ '+label,18,CYAN,mono=True)
            shown=message[:int(len(message)*min(1,(k+1)/14))]
            text(d,(205,56),shown,19,WHITE,mono=True)
            x=205+d.textlength(shown,font=font(19,mono=True))
            if k%8<5:
                d.rectangle((x+7,58,x+17,79),fill=PURPLE)
            text(d,(30,99),'FOCUS  /  AI + ROBOTICS + PRACTICAL SOFTWARE',11,MUTED,mono=True)
            frames.append(im)
    save(frames,'workbench.gif',110)


def divider():
    frames=[]
    for i in range(32):
        im=Image.new('RGB',(W,20),BG)
        d=ImageDraw.Draw(im)
        d.line((0,10,W,10),fill=LINE,width=1)
        x=int(i/31*(W+100))-50
        for j in range(25,0,-1):
            xx=x-j*3
            if 0<=xx<W:
                d.line((xx,10,xx+3,10),fill=(25,55+4*j,80+6*j),width=2)
        for at in (150,400,650,900,1150):
            d.ellipse((at-3,7,at+3,13),fill=PURPLE if abs(at-x)<55 else '#35455F')
        frames.append(im)
    save(frames,'signal.gif',100)


def footer():
    frames=[]
    labels=['BUILD','TEST','LEARN','REPEAT']
    for i in range(48):
        im,d=base(150)
        active=i//12
        for j,label in enumerate(labels):
            x=160+j*290
            if j<3:
                d.line((x+65,56,x+225,56),fill=LINE,width=2)
                dot=x+65+int((i%12)/12*160)
                if active==j:
                    d.ellipse((dot-4,52,dot+4,60),fill=CYAN)
            fill='#123744' if active==j else '#111D30'
            d.rounded_rectangle((x-66,33,x+66,79),radius=12,fill=fill,outline=CYAN if active==j else LINE,width=2)
            centered(d,x,47,label,16,CYAN if active==j else MUTED,True,True)
        centered(d,600,107,'CURIOUS MIND. PRACTICAL ENGINEERING. CONTINUOUS PROGRESS.',12,MUTED,mono=True)
        frames.append(im)
    save(frames,'build-loop.gif',100)


if __name__=='__main__':
    hero()
    terminal()
    divider()
    footer()
