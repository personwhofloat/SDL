import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw, ImageFont
import sys, os
from tqdm import tqdm
# i = sys.argv[1]
comp = sys.argv[1]
comps = {
    'paragraph': 0,
    'char': 1,
    'word': 2,
    'line': 3,
    'cell': 4,
    'table': 5,
    'figure': 6,
    'formula': 1,
    'title': 2
}
if comp == 'all':
    compz = ['paragraph','table','figure','formula', 'title']
else: 
    compz = [comp]
colors = [(0,255,0,64),(255,0,0,64),(0,0,255,64),(0,255,255,64),
        (255,0,255,64),(255,255,0,128),(64,64,64,150)]
font=ImageFont.truetype('arial.ttf',50)
# colors = ['green','red','pink','orange','blue','yellow','black']
for i in tqdm(range(len(os.listdir('output/images')))):    
    root = ET.parse(f'output/xmls/{i}.xml').getroot()
    info = root.findall('.//info')[0]
    w,h = info.attrib['width'],info.attrib['height']
    img = np.zeros((int(h),int(w),4),dtype='uint8')
    img = Image.fromarray(img)
    img2 = Image.open(f'output/images/{i}.png').convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    for comp in compz:
        comp_id = comps[comp]
        words = root.findall(f'.//{comp}')
        for word in words:
            attr = word.attrib
            x1,y1,x2,y2 = attr['x1'],attr['y1'],attr['x2'],attr['y2']
            x1,y1,x2,y2 = int(float(x1)),int(float(y1)),int(float(x2)),int(float(y2))
            draw.rectangle((x1,y1,x2,y2),fill=colors[comp_id])#,outline=(*colors[comp_id][:3],255),width=3)
            if len(compz) > 1:
                draw.rectangle(draw.textbbox((x1,y1),comp,font=font),fill=(0,0,0,170))
                draw.text((x1,y1),comp,fill='white',width=1, font=font)
            
    img = Image.composite(img,img2,Image.fromarray(np.array(img)[:,:,3]))
    img.save(f'output/vis/vis_{i}.png')
