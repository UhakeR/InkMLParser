from InkMLParser import InkMLParser
from InkMLToImg import InkMLToImg

import numpy.typing as nty
import numpy as np
from PIL import Image
import pandas as pd


class InkMLToTable(InkMLParser):
    def __init__(self, files_path:str, temp:str) -> None:
        
        super().__init__(file=files_path) #Parse the InkML file

        
        self.temp = temp
        self.image_size = (256,256)
        self.mode = 'both'
        self.data = self.getData() #Get the InkML file's data
        saved_images = InkMLToImg(self.data,self.UI,self.temp,mode=self.mode) #Save the InkML symbols and traces as image
        self.images:{'full_image':str,'symbols_path':[str]} = saved_images.get_paths()

        # Read the saved imges and convert them in arrays 
        self.data['TracesData'] = list(self.img2array(self.images['full_image']).flatten())

        # for path_index in range(len(self.images['symbols_path'])):
        #    id = self.images['symbols_path'][path_index][-5]
        #    if self.data['Symbols'][path_index]['id']==id:
        #        self.data['Symbols'][path_index]['data'] = self.img2array(self.images['symbols_path'][path_index])
        
        

        #TODO

        #Connect the symbol data with the traces data with some unique key
        #Save the traces and symbols data as a table  


    def parse_data(self):
        pass

    def save_data(self):
        pass

           

    def img2array(self,img_path) -> nty.NDArray:
        try:
            img =Image.open(img_path)
        except FileNotFoundError:
            raise ValueError("Image not found")
        img = img.convert('1')
        img.thumbnail(size=self.image_size)
        print(np.sqrt(np.array(img).size))
        return np.array(img).astype(int)
    
    



if __name__=="__main__":

    table = InkMLToTable(r'C:\Users\urreh\Documents\MATH-OCR\data\TrainINKML_2013\TrainINKML\MathBrush\200923-1556-167.inkml',r'C:\Users\urreh\Documents\MATH-OCR\data\Temp')