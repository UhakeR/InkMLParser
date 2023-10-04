
from xml.etree import ElementTree
import numpy as np
import matplotlib.pyplot as plt
import sys
import numpy.typing as nty
from PIL import Image
import numpy as np
import os
import yaml


class InkMLParser():

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
    def __init__(self,inkML:InkMLParser,image_path: str) -> None:
        """
        Save InkML file's trace data to image

        Args: 
            inkML (InkMLParser): InkMLParser object of the file you want to save as image
            image_path (str): Path in which the image will be saved
        """
        self.inkML = inkML
        self.image_path = image_path
        self.saveImage()
    
    def saveImage(self):  
        Trace = self.inkML.traces_data
        plt.gca().set_aspect('equal', adjustable='box')
        plt.rcParams["figure.figsize"] = (20,3)
        for i in range(len(Trace['X'])):
            plt.plot(np.array(Trace['X'][i]),np.array(Trace['Y'][i]) , color='black',linewidth=2)
        plt.axis('off')
        name = self.inkML.UI.replace('"','')
        self.image_path = f'{self.image_path}\{name}.png'
        plt.savefig(f'{self.image_path}\{name}.png',)
        plt.clf()





class InkML2Table:
    def __init__(self, InkML:InkMLParser,image_path:str, size:(int,int), temp:str) -> None:
        
        self.InkML = InkML

        # config = yaml.safe_load(open(r".\config.yml"))
        # directory = config['INKML_FILES_PATH']
 

        # for filename in os.listdir(directory):
        #     file = os.path.join(directory, filename)
        #     InkML = InkMLParser(file)
        #     if InkML._continue_:
        #         Inkml2Img(InkML,config['IMAGES_TEMP_PATH'])
        #     else:
        #         continue
        # self.img = Image.open(image_path)
        # self.img.thumbnail(size)
        # self.img.convert('RGB')
        # self.array = np.array(self.img)
        pass
    # Salviamo un inkml in una cartella in png
    # leggiamo il png con Image.open
    # convertiamo l'immagine in array
    # salviamo l'array ed i dati dell'array in un file csv


if __name__=="__main__":
    InkML = InkMLParser(sys.argv[1])
    ink = Inkml2Img(InkML,sys.argv[2])