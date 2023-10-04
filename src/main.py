from InkMLParser import Inkml2Img, InkMLParser
from PIL import Image
import os
import yaml


# size = 228, 228

# im= Image.open(r"C:\Users\urreh\Documents\MATH-OCR\MfrDB2934.png")
# im.thumbnail(size)
# im.convert('RGB')
# array = np.array(im)

if __name__=="__main__":
    config = yaml.safe_load(open(r".\config.yml"))
    directory = config['INKML_FILES_PATH']
 

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        InkML = InkMLParser(file)
        if InkML._continue_:
            Inkml2Img(InkML,config['IMAGES_TEMP_PATH'])
        else:
            continue

