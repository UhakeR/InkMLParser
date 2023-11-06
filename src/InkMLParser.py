from xml.etree import ElementTree
import numpy as np
import numpy.typing as nty


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
            self.UI = self.root.find("{http://www.w3.org/2003/InkML}annotation[@type='UI']").text.replace('"','')
            self.annotation: str = self.root.findtext("{http://www.w3.org/2003/InkML}annotation[@type='truth']")
            self.traces_id = [x.attrib['id'] for x in self.root.findall("{http://www.w3.org/2003/InkML}trace")]
            self.symbols_data: [{"id":str, "annotation":str,"data":[]}] = list()
            self.traces_data: {'X': [float] ,'Y': [float]} = {'X': [], 'Y': []}
            self.combine: [str] = []
            self._parse_traces_data()
            self._parse_symbols_data()
            if len(self.combine)>1:
                for combination in self.combine:
                    self._combine_symbols_util(combination)


    def _fix_traces_data_util(self,id:str) -> {'X': [], 'Y': []}:
        """
        Util used to fix and process traces data
        """
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


    def _combine_symbols_util(self,combination):
        """
        Util used to combine symbols devided in two or more traces
        """
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
            'Unique_identifier':self.UI,
            'Annotation':self.annotation,
            'TracesData':self.traces_data,
            'Symbols':self.symbols_data
        }