import csv
import os
from pathlib import Path
from tkinter import filedialog

class CsvFileNotFound(Exception):
    """
        Excepcion que indica que no hay datos de resultados cargados en el programa
    """

    def __init__(self):
        self.message = (
            "No se encuentran datos de los resultados, asegúrese de que el archivo se encuentra en el directorio "
            "correcto y se ha cargado correctamente")
        super().__init__(self.message)

class csvReader:
    def __init__(self):
        self.csvReader = csv.DictReader
        self.workingDirectory = os.getcwd()
        self.defaultInputDataFolder = self.workingDirectory + "/inputData"
        self.csvFilePath:str = ""
        self.csvFileName:str = ""
        self.csvData = []
        Path(self.defaultInputDataFolder).mkdir(parents=True, exist_ok=True)

    def loadCsvFile(self):
        try:
            f = filedialog.askopenfilename(title="Seleccionar archivo de resultados",
                                           initialdir=self.defaultInputDataFolder,
                                           filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                                           defaultextension=".csv")

            if f != "":
                self.csvFilePath = f.replace("/", "/")
            if self.csvFilePath is None or self.csvFilePath == '':
                print("Archivo de oferta no seleccionado")
                raise CsvFileNotFound

            self.csvFileName = self.csvFilePath.split("/")[-1].split(".")[0]
            self.getRawDataFromCsv()
            return f

        except CsvFileNotFound:
            return -2

        except Exception as e:
            print(e)
            return -1

    def getRawDataFromCsv(self):
        try:
            with open(self.csvFilePath,mode="r", encoding='utf-8') as file:
                sample = file.read(100)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                file.seek(0)
                for row in self.csvReader(file, delimiter=delimiter):
                    self.csvData.append((row.get("id"),
                                         row.get("user_pattern"),
                                         row.get("departure_station"),
                                         row.get("arrival_station"),
                                         row.get("arrival_day"),
                                         row.get("arrival_time"),
                                         row.get("purchase_day"),
                                         row.get("service"),
                                         row.get("service_departure_time"),
                                         row.get("service_arrival_time"),
                                         row.get("seat"),
                                         row.get("price"),
                                         row.get("utility"),
                                         row.get("best_service"),
                                         row.get("best_seat"),
                                         row.get("best_utility")))
            print(self.csvData[:][0])
            print(self.csvData)
        except Exception as e:
            print(e)
            return -1

class csvWriter:
    def __init__(self,csvFileName,data,columnsName = None):
        if columnsName is not None: self.columnsName = columnsName
        else:
            self.columnsName = ("id",
                                "user_pattern",
                                "departure_station",
                                "arrival_station",
                                "arrival_day",
                                "arrival_time",
                                "purchase_day",
                                "service",
                                "service_departure_time",
                                "service_arrival_time",
                                "seat",
                                "price",
                                "utility",
                                "best_service",
                                "best_seat",
                                "best_utility")
        self.csvWriter = csv.writer
        self.workingDirectory = os.getcwd()
        self.defaultOutputDataFolder = self.workingDirectory + "/outputData"
        self.csvSavePath: str = ""
        self.csvFileName: str = csvFileName+".csv"
        self.csvData = data
        Path(self.defaultOutputDataFolder).mkdir(parents=True, exist_ok=True)

    def getSavePath(self):
        f = filedialog.askdirectory(title="Exportar archivo",
                                    initialdir=self.defaultOutputDataFolder)

        if f != "":
            self.csvSavePath = f.replace("/", "/")
            self.csvSavePath = self.csvSavePath + "/" + self.csvFileName

    def saveFile(self):
        try:
            self.getSavePath()
            # print(self.saveFilePath)
            if self.csvSavePath != "":
                with open(self.csvSavePath, 'w', encoding='utf-8') as file:
                    writer = self.csvWriter(file,delimiter=",",lineterminator="\n")
                    writer.writerow(self.columnsName)
                    writer.writerows(self.csvData)
        except Exception as e:
            print("Error: " + str(e))
        finally: del self