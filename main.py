import argparse
from util import get_img, render
from PIL import Image, ImageFont, ImageEnhance
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import json
from tqdm import tqdm
from tbd import info, error
from config import Config
import datetime
import sys
import cv2
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
def main(args):
    total_time = 0
    for idx, im in enumerate(range(args.resume_from, args.resume_from+args.repeat)):
        args.text_color = (*np.random.randint(0,80,3).tolist(), np.random.randint(160,255))
        args.col_spacing = np.random.randint(*args.col_spacing_)
        t = time.time()
        img = get_img(args.bg_img)
        img = cv2.GaussianBlur(np.array(img),(5,5),cv2.BORDER_DEFAULT)
        img = Image.fromarray(img)
        img = img.resize((1500, 2000))
        out_img, para = render(args, img)
        ps = para['para']
        paras = []
        for p in ps:
            if isinstance(p,list):
                for p_prime in p:
                    paras.append(p_prime)
            else: paras.append(p)
        para['para'] = paras
        if args.blur:
            out_img = cv2.GaussianBlur(np.array(out_img),(5,5),cv2.BORDER_DEFAULT)
            out_img = Image.fromarray(out_img)
        json.dump(para, open(os.path.join(
            args.output, 'jsons', f'{im}.json'), 'w',encoding='utf-8'))
        img2 = Image.fromarray(np.array(out_img)[:, :, :3])
        
        mask = Image.fromarray(np.array(out_img)[:, :, 3])

        out_img = Image.composite(img2, img, mask)

        enhancer = ImageEnhance.Brightness(out_img)
        out_img = enhancer.enhance((3.25+np.random.rand())/4)

        out_img.save(
            os.path.join(args.output, 'images', f'{im}.png'))
        total_time += (time.time() - t)
        if (idx - args.resume_from + 1) % args.print_freq == 0:
            avg_time = total_time / (idx - args.resume_from + 1)
            eta = avg_time * args.repeat - total_time
            eta = str(datetime.timedelta(seconds=round(eta)))
            ttime = str(datetime.timedelta(seconds=round(total_time)))
            info(f"Generated {idx-args.resume_from+1}/{args.repeat}: average time: {avg_time:.2f}s eta: {ttime}/{eta}")

def format_range(a_range, name):
    if type(a_range) != str:
        error(f'{name} should be a string')
        sys.exit()
    if '-' not in a_range:
        error(f'{name} should have form of a-b where a and b are integers and a<b')
        sys.exit()
    res = [int(s) for s in a_range.split('-')]
    res[-1] += 1
    if len(res) != 2:
        error(f'length of {name} should be 2')
        sys.exit()
    if not res[0] < res[1]:
        error(f'first number in {name} should not be greater than second number in {name}')
        sys.exit()
    return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', default= 'page.yaml',type=str)
    parser.add_argument('-bg','--bg_img', default='assets', type=str)
    parser.add_argument('--doc_images',default=r'C:\Users\sonnt72\Downloads\bg_img', type=str, help='path to images appearing in the document')
    parser.add_argument('--font_path', default='Unicode', type=str)
    parser.add_argument('--output', default='output', type=str)
    parser.add_argument('--words', default='dictionary_wiki_and_news.txt', type=str)
    parser.add_argument('--fontsize', default='16-40', type=str)
    parser.add_argument('--col_range',default='1-3',type=str)
    parser.add_argument('--repeat', default=5, type=int,
                        help='number of time we are gonna repeat process on an image')
    parser.add_argument('--spacing', default=0.15, type=float,
                        help='spacing ratio between lines in a passage')
    parser.add_argument('--period_prob', default=0.0,
                        type=float, help='probability that period appears')
    parser.add_argument('--print_freq', default = 1, type = int, help='print frequency')
    parser.add_argument('--visible_column_prob', default=0.5, type=float,
                        help='probability that we will have table with column line visible')
    parser.add_argument('--resume_from',type=int,default=0,help='index of the next image to generate')
    parser.add_argument('--type',type=str,choices=['page','table'])
    parser.add_argument('--vis_line', action='store_true')
    parser.add_argument('--vis_word', action='store_true')
    parser.add_argument('--vis_cell', action='store_true')
    parser.add_argument('--vis_char', action='store_true')
    parser.add_argument('--max_line', default=62, type=int)
    parser.add_argument('--col_spacing', default='40-50', type=str)
    parser.add_argument('--tab_at_start', action='store_true')
    parser.add_argument('--prob_image', default=0.15,type=float, help='Probability for an image to appear in the document')
    parser.add_argument('--blur',action='store_true')
    args_ = parser.parse_args()
    args = Config()
    args.merge_from_args(args_)
    args.merge_from_file(args_.config_file)
    
    args.words = [word.strip() for word in open(
        args.words, 'r', encoding='utf-8').readlines()]
    
    args.fontsize = format_range(args.fontsize, "fontsize")
    args.col_range = format_range(args.col_range, "col_range")
    args.col_spacing_ = format_range(args.col_spacing,'col_spacing')
    
    main(args)
