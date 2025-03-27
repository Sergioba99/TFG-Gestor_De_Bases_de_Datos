import yaml
import os
from pathlib import Path
from tkinter import filedialog

class Writer:
    """Módulo encargado de generar los archivos .yml a partir de los datos obtenidos de la base de datos"""
    def __init__(self):
        self.data = None
        self.fileName = None
        self.workingDirectory = os.getcwd()
        self.defaultOutputDataFolder = self.workingDirectory + "\\outputData"
        Path(self.defaultOutputDataFolder).mkdir(parents=True, exist_ok=True)
        self.saveFilePath = ""

    def getSavePath(self):
        f = filedialog.askdirectory(title="Exportar archivo",
                                    initialdir=self.defaultOutputDataFolder)

        if f!="":
            self.saveFilePath = f.replace("\\", "/")
            self.saveFilePath = self.saveFilePath+"/"+self.fileName

    def saveFile(self,fileName,data):
        self.data = data
        self.fileName = fileName + ".yml"

        try:
            self.getSavePath()
            #print(self.saveFilePath)
            if self.saveFilePath != "":
                with open(self.saveFilePath,'w',encoding='utf-8') as file:
                    yaml.safe_dump(data=self.data,
                                   stream=file,
                                   default_flow_style=False,
                                   sort_keys=False,
                                   allow_unicode=True,
                                   width=30,
                                   indent=2)
        except Exception as e:
            print("Error: " +str(e))
