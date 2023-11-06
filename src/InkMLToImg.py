import matplotlib.pyplot as plt
import numpy as np

class InkMLToImg:
    def __init__(self,data:{'X': [float] ,'Y': [float]},UI:str,image_path: str,mode:str) -> None:
        """
        Save InkML file's trace data to image

        Args: 
            data (dict): data of the InkML file you want to save as image
            image_path (str): Path in which the image will be saved
            mode (str):
                'symbols' to save only simbols as img
                'traces' to save the full pictures
                'both' to save both symbols and traces
        """
        self.Traces = data
        self.UI = UI
        self.image_path = image_path
        self.path: str = ''
        self.paths: [str] = []
        match mode:
            case 'symbols':
                self.paths= self.saveSymbolsImg()

            case 'traces':
                self.path = self.saveTracesAsImage()

            case 'both':
                self.paths = self.saveSymbolsImg()
                self.path = self.saveTracesAsImage()

    
    def saveTracesAsImage(self) -> str:  
        """
        Save all traces as a single image

        Returns:
            - str: path of the saved image
        """
        name = self.UI.replace('"','').replace('.ink','')
        image_path = f'{self.image_path}\{name}.png'
        Traces = self.Traces['TracesData']
        self._plot_util(Traces,image_path)
        return image_path
    
    def saveSymbolsImg(self) -> [str]:
        """
        Save all the symbols as single image

        Returns:
            - str: path of the saved image
        """
        name = self.UI.replace('"','').replace('.ink','')
        images_path: [str]=[]
        for symbol in self.Traces['Symbols']:
            image_path = f'{self.image_path}\{name}_{symbol["id"]}.png'
            images_path.append(image_path)
            self._plot_util(symbol['data'],image_path)
        return images_path
    
    def _plot_util(self,data,image_path:str) -> None:

        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().invert_yaxis()
        plt.rcParams["figure.figsize"] = (256,256)
        try:
            plt.plot(np.array(data['X']),np.array(data['Y']) , color='black',linewidth=5)
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
        """
        Returns:
            - dict: both path of the single image of combined symbols and a list of paths of each symbol
        """
        return {'full_image':self.path,'symbols_path':self.paths}
