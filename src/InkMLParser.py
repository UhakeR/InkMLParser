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
            
            self._parse_traces_data()
            self._parse_symbols_data()

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
            trace_id = i.find("{http://www.w3.org/2003/InkML}traceView").attrib['traceDataRef']
            annotation = i.find("{http://www.w3.org/2003/InkML}annotation[@type='truth']").text
            self.symbols_data.append({"id": trace_id, "annotation":annotation,"data": self._fix_traces_data_util(trace_id)})
    
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
    def __init__(self,traces_data:{'X': [float] ,'Y': [float]},UI:str,image_path: str) -> None:
        """
        Save InkML file's trace data to image

        Args: 
            inkML (InkMLParser): InkMLParser object of the file you want to save as image
            image_path (str): Path in which the image will be saved
        """
        self.Traces = traces_data
        self.UI = UI
        self.image_path = image_path
        self.saveImage()
    
    def saveTracesAsImage(self) -> str:  
        plt.gca().set_aspect('equal', adjustable='box')
        plt.rcParams["figure.figsize"] = (20,3)
        for i in range(len(self.Traces['X'])):
            plt.plot(np.array(self.Traces['X'][i]),np.array(self.Traces['Y'][i]) , color='black',linewidth=2)
        plt.axis('off')
        name = self.UI.replace('"','')
        self.image_path = f'{self.image_path}\{name}.png'
        plt.savefig(self.image_path)
        plt.clf()
        return self.image_path

    def saveSymbolsAsImage(self) -> str:  
        """
        """

        return self.image_path






class InkML2Table(InkMLParser):
    def __init__(self, files_path:str, size:(int,int), temp:str) -> None:
        
        super().__init__(file=files_path)
        self.temp = temp
        self.image_size = size
        print(self.symbols_data)
        self.image_path = Inkml2Img(self.symbols_data,self.UI,self.temp)
        
        self.symbols_array = self.img2array()

        #Parse the InkML file
        #Get the InkML metadata
        #Save the InkML symbols as image
        #Save the inkML traces as image
        #Read each image and create the array of it
        #Connect the symbol data with the traces data with some unique key
        #Save the traces and symbols data as a table  

        #for each image in images_path:
            # Read the image
            
        pass

    def img2array(self):
        img =Image.open(self.image_path)
        img.resize(size=self.image_size)
        img.convert('RGB')
        return np.array(img)