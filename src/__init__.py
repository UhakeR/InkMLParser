from InkMLParser import Inkml2Img, InkMLParser
from PIL import Image
import os
import yaml


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

