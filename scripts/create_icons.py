"""Generate the project's small-size-friendly trophy icons (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parents[1] / 'web' / 'public'
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#153e75"/>
  <path d="M20 18H12V25Q12 34 25 34M44 18H52V25Q52 34 39 34" fill="none" stroke="#fbbf24" stroke-width="5" stroke-linejoin="round"/>
  <path d="M19 13H45V27Q45 40 32 40Q19 40 19 27Z" fill="#fbbf24"/>
  <path d="M32 38V49M23 51H41" fill="none" stroke="#fbbf24" stroke-width="6" stroke-linecap="round"/>
  <path d="M26 24L30 28L38 20" fill="none" stroke="#153e75" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
(out / 'favicon.svg').write_text(svg, encoding='utf-8')
scale = 16
im = Image.new('RGBA', (64 * scale, 64 * scale))
d = ImageDraw.Draw(im)
blue, gold = '#153e75', '#fbbf24'
def box(coords): return tuple(int(v * scale) for v in coords)
def line(points, color, width):
    d.line([(x*scale, y*scale) for x,y in points], fill=color, width=width*scale, joint='curve')
    for x,y in (points[0], points[-1]):
        r=width/2
        d.ellipse(box((x-r,y-r,x+r,y+r)), fill=color)
d.rounded_rectangle(box((0,0,64,64)), radius=14*scale, fill=blue)
d.rounded_rectangle(box((10,15.5,29,36.5)), radius=10*scale, outline=gold, width=5*scale)
d.rounded_rectangle(box((35,15.5,54,36.5)), radius=10*scale, outline=gold, width=5*scale)
line([(32,38),(32,49)],gold,6)
line([(23,51),(41,51)],gold,6)
d.rounded_rectangle(box((19,13,45,40)), radius=13*scale, fill=gold)
d.rectangle(box((19,13,45,27)), fill=gold)
line([(26,24),(30,28),(38,20)],blue,4)
im = im.resize((256,256), Image.Resampling.LANCZOS)
im.save(out / 'app-icon.png')
im.save(out / 'app-icon.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
im.resize((180,180), Image.Resampling.LANCZOS).save(out / 'apple-touch-icon.png')
