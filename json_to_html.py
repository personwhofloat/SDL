import json
import xml.etree.ElementTree as ET

f = json.load(open('output/jsons/0.json', 'r'))
for line in f['text']:
    print(line, end=' ')
data = ET.Element('div')
line_idx = 0
word_idx = 0
for i, para in enumerate(f['para']):
    para_ = ET.SubElement(data, 'div')
    para_.set('name', f'para_{i}')
    para_.set('x1', str(f['bbox'][0]))
    para_.set('y1', str(f['bbox'][1]))
    para_.set('x2', str(f['bbox'][2]))
    para_.set('y2', str(f['bbox'][3]))

    #para_.set('bbox', ' '.join([str(coord) for coord in f['bbox']]))
    for j, line in enumerate(para['lines']):
        line_idx += 1
        line_ = ET.SubElement(para_, f'div')
        line_.set('name', f'line_{line_idx}')
        line_.set('x1', str(line['bbox'][0]))
        line_.set('y1', str(line['bbox'][1]))
        line_.set('x2', str(line['bbox'][2]))
        line_.set('y2', str(line['bbox'][3]))
        for k, word in enumerate(line['words']):
            word_idx += 1
            word_ = ET.SubElement(line_, 'div')
            word_.set('name', f'word_{word_idx}')
            word_.set(
                'style', 'position:absolute;left:'+str(word['bbox'][0])+';top:'+str(word['bbox'][3]/2+word['bbox'][1]/2)+';')
            word_.set('x1', str(word['bbox'][0]))
            word_.set('y1', str(word['bbox'][1]))
            word_.set('x2', str(word['bbox'][2]))
            word_.set('y2', str(word['bbox'][3]))
            word_.text = word['text']
mydata = ET.tostring(data, encoding="unicode")
myfile = open('0.html', 'w')
myfile.write(mydata)
