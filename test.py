from PIL import Image
import os
from tqdm import tqdm
img_path = 'output/images/'

for path in tqdm(os.listdir(img_path)):
    img = Image.open(os.path.join(img_path,path))
    img.save(os.path.join(img_path, path.split('.')[0]+'.jpg'))
    os.remove(os.path.join(img_path,path))
