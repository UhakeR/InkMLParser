from xml.etree import ElementTree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy.typing as nty
from PIL import Image
import os
import yaml


class InkMLParser:

    def __init__(self, file:str) -> None:
        """
        Initialize the parser with the path to an INKML file.

        Args: file_path (str): The path to the INKML file.
        """
        self._continue_ = True
        self.error_message = ""
        try:
            self.tree = ElementTree.parse(file)
        except ElementTree.ParseError as err:
            self._continue_ = False
            self.error_message = err
        
        if self._continue_:
            self.root = self.tree.getroot()
            self.UI = self.root.find("{http://www.w3.org/2003/InkML}annotation[@type='UI']").text
            self.annotation: str = self.root.findtext("{http://www.w3.org/2003/InkML}annotation[@type='truth']")
            self.traces_id = [x.attrib['id'] for x in self.root.findall("{http://www.w3.org/2003/InkML}trace")]
            self.symbols_data: [{"id":str, "annotation":str,"data":[]}] = list()
            self.traces_data: {'X': [float] ,'Y': [float]} = {'X': [], 'Y': []}
            self.combine: [str] = []
            self.interupt: {str:[int]} = {}
            self._parse_traces_data()
            self._parse_symbols_data()
            if len(self.combine)>1:
                for combination in self.combine:
                    self.combine_symbols(combination)


    def _fix_traces_data_util(self,id:str) -> {'X': [], 'Y': []}:
        data = {'X': [], 'Y': []}
        element = "{0}trace[@id='{1}']".format("{http://www.w3.org/2003/InkML}",id)
        sublist = self.root.find(element).text.replace('\n','').split(',') 
        for i in range(len(sublist)):
            sublist[i] = sublist[i].strip()
            data['X'].append(float(sublist[i].split(' ')[0]))
            data['Y'].append(float(sublist[i].split(' ')[1]))
        return data
    
    def _parse_traces_data(self) -> None:
        """
        Parse and extract trace data from the INKML file.
        """
        for trace_id in self.traces_id:
            trace_data = self._fix_traces_data_util(trace_id)
            self.traces_data['X'].append(trace_data["X"])
            self.traces_data['Y'].append(trace_data["Y"])
    
    def _parse_symbols_data(self) -> None:
        """
        Parse and extract symbols data from INKML file
        """
        
        for i in self.root.find("{http://www.w3.org/2003/InkML}traceGroup").findall("{http://www.w3.org/2003/InkML}traceGroup"):
            annotation = i.find("{http://www.w3.org/2003/InkML}annotation[@type='truth']").text
            trace_id = i.findall("{http://www.w3.org/2003/InkML}traceView")
            combo = []
            if len(trace_id)>1:
                for x in trace_id:
                    combo.append(x.attrib['traceDataRef'])
                self.combine.append(tuple(combo))
            for j in range(len(trace_id)):
                self.symbols_data.append({"id": trace_id[j].attrib['traceDataRef'], "annotation":annotation,"data": self._fix_traces_data_util(trace_id[j].attrib['traceDataRef'])})


    def combine_symbols(self,combination):
        X = []
        Y = []
        delete_index = []
        father_symbol_id: int = 0
        for symbol in range(len(self.symbols_data)):
            if self.symbols_data[symbol]['id'] in combination:
                if self.symbols_data[symbol]['id'] == combination[0]:
                    father_symbol_id = symbol
                else:
                    delete_index.append(symbol)
                X.append(self.symbols_data[symbol]['data']['X'])
                Y.append(self.symbols_data[symbol]['data']['Y'])
            else:
                continue
            self.symbols_data[father_symbol_id]['data']['X'] = X
            self.symbols_data[father_symbol_id]['data']['Y'] = Y
            
        deleted = 0
        for rem in delete_index:
            if rem == len(self.symbols_data):
                self.symbols_data.pop()
            else:
                self.symbols_data.pop(rem-deleted)
                deleted+=1
                    
            

    def getData(self) -> {'Key','value'}:
        """
        Get the parsed data.

        Returns:
            dict: A dictionary containing parsed data.
        """
        return  {
            'UI':self.UI,
            'Annotation':self.annotation,
            'Traces_Data':self.traces_data,
            'Symbols':self.symbols_data
        }
       

class Inkml2Img:
    def __init__(self,traces_data:{'X': [float] ,'Y': [float]},UI:str,image_path: str,mode:str,breakpoints) -> None:
        """
        Save InkML file's trace data to image

        Args: 
            inkML (InkMLParser): InkMLParser object of the file you want to save as image
            image_path (str): Path in which the image will be saved
            mode (str):
                'symbols' to save only simbols as img
                'traces' to save the full pictures
                'both' to save both symbols and traces
        """
        self.Traces = traces_data
        self.UI = UI
        self.image_path = image_path
        self.breakpoints = breakpoints
        self.path: str = ''
        self.paths: [str] = []
        match mode:
            case 'symbols':
                self.paths= self.saveSymbolsImg()

            case 'traces':
                self.path = self.saveTracesAsImage()

            case 'both':
                self.paths= self.saveSymbolsImg()
                self.path = self.saveTracesAsImage()

    
    def saveTracesAsImage(self) -> str:  
        name = self.UI.replace('"','').replace('.ink','')
        image_path = f'{self.image_path}\{name}.png'
        Traces = self.Traces['Traces_Data']
        self.plot(Traces,image_path)
        return image_path
    
    def saveSymbolsImg(self) -> [str]:
        name = self.UI.replace('"','').replace('.ink','')
        images_path: [str]=[]
        for symbol in self.Traces['Symbols']:
            image_path = f'{self.image_path}\{name}_{symbol["id"]}.png'
            images_path.append(images_path)
            self.plot(symbol['data'],image_path)
        return images_path
    
    def plot(self,data,image_path:str) -> None:
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().invert_yaxis()
        plt.rcParams["figure.figsize"] = (20,3)
        try:
            plt.plot(np.array(data['X']),np.array(data['Y']) , color='black',linewidth=3)
        except:
            for i in range(len(data['X'])):
                try: 
                    plt.plot(np.array(data['X'][i]),np.array(data['Y'][i]) , color='black',linewidth=3)
                except ValueError as war:
                    continue
        plt.axis('off')
        plt.savefig(image_path)
        plt.clf()
    
    def get_paths(self) -> {'full_image':str,'symbols_path':[str]}:
        return {'full_image':self.path,'symbols_path':self.paths}





class InkML2Table(InkMLParser):
    def __init__(self, files_path:str, size:(int,int), temp:str) -> None:
        
        super().__init__(file=files_path)
        self.temp = temp
        self.image_size = size
        self.data = self.getData()
        self.mode = 'both'
        Imgs = Inkml2Img(self.data,self.UI,self.temp,mode=self.mode,breakpoints=self.interupt)
        self.images:{'full_image':str,'symbols_path':[str]} = Imgs.get_paths()

        #TODO
        #Parse the InkML file
        #Get the InkML metadata
        #Save the InkML symbols as image
        #Save the inkML traces as image
        #Read each image and create the array of it
        #Connect the symbol data with the traces data with some unique key
        #Save the traces and symbols data as a table  

        #for each image in images:
            # Read the image
            

    def img2array(self,img_path):
        img =Image.open(img_path)
        img.resize(size=self.image_size)
        img.convert('RGB')
        return np.array(img)
    
    



if __name__=="__main__":

    table = InkML2Table(r'C:\Users\urreh\Documents\MATH-OCR\data\TrainINKML_2013\TrainINKML\KAIST\KME1G3_0_sub_21.inkml',(128,128),r'C:\Users\urreh\Documents\MATH-OCR\data\Temp')
    print(table.data)