# Importamos las librerias necesarios para el funcionamiento del módulo
# yamlParser
import json
import os
from copy import deepcopy
from pathlib import Path
from tkinter import filedialog

import yaml


# Excepción personalizada para falta de datos de oferta
class EmptySupplyData(Exception):
    """
        Excepcion que indica que no hay datos de oferta cargados en el programa
    """

    def __init__(self):
        self.message = (
            "No se encuentran datos de la oferta, asegúrese de que el archivo "
            "se encuentra en el directorio "
            "correcto y se ha cargado correctamente")
        super().__init__(self.message)


# Excepción personalizada para falta de datos de oferta
class EmptyDemandData(Exception):
    """
        Excepción que indica que no hay datos de demanda cargados en el programa
    """

    def __init__(self):
        self.message = (
            "No se encuentran datos de la demanda, asegúrese de que el "
            "archivo se encuentra en el directorio "
            "correcto y se ha cargado correctamente")
        super().__init__(self.message)


# Excepción personalizada para archivo de oferta faltante
class SupplyFileNotFound(Exception):
    """
        Excepción que indica que no se ha podido cargar el archivo de oferta
    """

    def __init__(self):
        self.message = (
            "No se ha podido cargar el archivo de oferta, asegúrese de que el "
            "archivo se encuentra en el "
            "directorio correcto y tiene el nombre de supply_data.yml")
        super().__init__(self.message)


# Excepción personalizada para archivo de demanda faltante
class DemandFileNotFound(Exception):
    """
        Excepción que indica que no se ha podido cargar el archivo de oferta
    """

    def __init__(self):
        self.message = (
            "No se ha podido cargar el archivo de oferta, asegúrese de que el "
            "archivo se encuentra en el "
            "directorio correcto y tiene el nombre de demand_data.yml")
        super().__init__(self.message)


# Clase para manejar la lectura del archivo Yaml
class Parser:
    # Definición del constructor de la clase Parser
    def __init__(self, supplyFile=None, demandFile=None):
        self.workingDirectory = os.getcwd()  # Directorio de trabajo
        # Directorio de entrada de datos
        self.defaultInputDataFolder = self.workingDirectory + "/inputData"
        self.supplyFilePath: str = supplyFile  # Dirección del archivo de oferta
        self.demandFilePath: str = demandFile  # Dirección del archivo de
        # demanda
        self.supplyData = dict()  # Datos del archivo de oferta
        self.demandData = dict()  # Datos del archivo de demanda
        self.supplyFileName: str = ''  # Nombre del archivo de oferta
        self.demandFileName: str = ''  # Nombre del archivo de demanda
        Path(self.defaultInputDataFolder).mkdir(parents=True,
                                                exist_ok=True)  # Generamos
        # la carpeta inputData si no existe

    def loadSupplyFile(self):
        try:
            f = filedialog.askopenfilename(
                title="Seleccionar archivo de oferta",
                initialdir=self.defaultInputDataFolder,
                filetypes=[("Archivos YAML", ("*.yml", "*.yaml")),
                           ("Todos los archivos",
                            "*.*")],
                defaultextension=".yml")
            if f != "":
                self.supplyFilePath = f.replace("/", "/")
            else:
                self.supplyFilePath = ""
                self.supplyFileName = ""
            if self.supplyFilePath is None or self.supplyFilePath == '':
                # print("Archivo de oferta no seleccionado")
                raise SupplyFileNotFound

            self.supplyFileName = self.supplyFilePath.split("/")[-1].split(".")[
                0]
            self.getRawDataFromSupply()
            return f

        except SupplyFileNotFound:
            return -2

        except Exception as e:
            print(e)
            return -1

    def loadDemandFile(self):
        try:
            f = filedialog.askopenfilename(
                title="Seleccionar archivo de demanda",
                initialdir=self.defaultInputDataFolder,
                filetypes=[("Archivos YAML", ("*.yml", "*.yaml")),
                           ("Todos los archivos", "*.*")],
                defaultextension=".yml")
            if f != "":
                self.demandFilePath = f.replace("/", "/")
            else:
                self.demandFilePath = ""
                self.demandFileName = ""
            if self.demandFilePath is None or self.demandFilePath == '':
                # print("Archivo de demanda no seleccionado")
                raise DemandFileNotFound

            self.demandFileName = self.demandFilePath.split("/")[-1].split(".")[
                0]
            self.getRawDataFromDemand()
            return f

        except DemandFileNotFound:
            return -2

        except Exception as e:
            print(e)
            return -1

    def getRawDataFromFile(self, path):
        """
        Esta funcion lee el contenido del archivo en la direccion introducida
        a la funcion como parametro
        :param path: Direccion del archivo .yml del que se van a extraer los
        datos.
        :return: Devuelve los datos almacenados en el archivo indicado en path.
        """
        try:
            file = open(path, 'r')
            data = yaml.safe_load(
                file)  # Cargamos los datos desde el archivo yaml
            return data
        except Exception as e:
            print(e)
            return {}

    def getRawDataFromSupply(self):
        """
        Esta funcion lee el contenido del archivo de oferta y lo almacena en
        self.supplyData.
        :return: None
        """
        try:
            file = open(self.supplyFilePath, 'r', encoding='utf-8')
            self.supplyData = yaml.safe_load(
                file)  # Cargamos los datos del archivo yaml de la oferta

        except Exception as e:
            print(e)

    def getRawDataFromDemand(self):
        """
        Esta funcion lee el contenido del archivo de demanda y lo almacena en
        self.demandData
        :return: Devuelve los datos almacenados en el archivo indicado en path.
        """
        try:
            file = open(self.demandFilePath, 'r', encoding='utf-8')
            self.demandData = yaml.safe_load(file)
        except Exception as e:
            print(e)

    def clearData(self):
        """
        Borra los datos cargados de los archivos de oferta y demanda.
        :return: None
        """
        self.supplyData = None
        self.demandData = None

    def getStations(self):
        """
        Funcion que obtiene los datos dentro de stations en el archivo Yaml
        de la oferta.
        :return: Devuelve los datos almacenados en stations
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("stations")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getSeat(self):
        """
        Funcion que obtiene los datos dentro de seat en el archivo Yaml de la
        oferta.
        :return: Devuelve los datos almacenados en seat.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("seat")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getCorridor(self):
        """
        Funcion que obtiene los datos dentro de corridor en el archivo Yaml
        de la oferta.
        :return: Devuelve los datos almacenados en corridor.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("corridor")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getLine(self):
        """
        Funcion que obtiene los datos dentro de line en el archivo Yaml de la
        oferta.
        :return: Devuelve los datos almacenados en line.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("line")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getRollingStock(self):
        """
        Funcion que obtiene los datos dentro de rollingStock en el archivo
        Yaml de la oferta.
        :return: Devuelve los datos almacenados en rollingStock.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("rollingStock")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getTrainServiceProvider(self):
        """
        Funcion que obtiene los datos dentro de trainServiceProvider en el
        archivo Yaml de la oferta.
        :return: Devuelve los datos almacenados en trainServiceProvider.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("trainServiceProvider")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getTimeSlot(self):
        """
        Funcion que obtiene los datos dentro de timeSlot en el archivo Yaml
        de la oferta.
        :return: Devuelve los datos almacenados en timeSlot.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("timeSlot")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getService(self):
        """
        Funcion que obtiene los datos dentro de service en el archivo Yaml de
        la oferta.
        :return: Devuelve los datos almacenados en service.
        """
        try:
            if self.supplyData is None: raise EmptySupplyData
            return self.supplyData.get("service")
        except EmptySupplyData as e:
            print(e)
            return -1
        except:
            return -1

    def getMarket(self):
        """
        Funcion que obtiene los datos dentro de market en el archivo Yaml de
        la demanda.
        :return: Devuelve los datos almacenados en market.
        """
        try:
            if self.demandData is None: raise EmptyDemandData
            return self.demandData.get("market")
        except EmptyDemandData as e:
            print(e)
            return -1
        except:
            return -1

    def getUserPattern(self):
        """
        Funcion que obtiene los datos dentro de userPattern en el archivo
        Yaml de la demanda.
        :return: Devuelve los datos almacenados en userPattern.
        """
        try:
            if self.demandData is None: raise EmptyDemandData
            return self.demandData.get("userPattern")
        except EmptyDemandData as e:
            print(e)
            return -1
        except:
            return -1

    def getDemandPattern(self):
        """
        Funcion que obtiene los datos dentro de demandPattern en el archivo
        Yaml de la demanda.
        :return: Devuelve los datos almacenados en demmandPattern.
        """
        try:
            if self.demandData is None: raise EmptyDemandData
            return self.demandData.get("demandPattern")
        except EmptyDemandData as e:
            print(e)
            return -1
        except:
            return -1

    def getDay(self):
        """
        Funcion que obtiene los datos dentro de day en el archivo Yaml de la
        demanda.
        :return: Devuelve los datos almacenados en day.
        """
        try:
            if self.demandData is None: raise EmptyDemandData
            return self.demandData.get("day")
        except EmptyDemandData as e:
            print(e)
            return -1
        except:
            return -1

    # Funciones para el archivo de oferta
    # Funciones para campos específicos de timeSlot
    def getTimeSlotData(self):
        """
        Función que devuelve todos los campos de time slot en la posición
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>, <start>, <end>]
        :return: Devuelve el value de timeSlot en la posicion index.
        """
        TimeSlot = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            timeSlot = self.getTimeSlot()
            TimeSlot = [[
                data.get("id"),
                data.get("start"),
                data.get("end")]
                for data in timeSlot
            ]
            return TimeSlot
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos específicos de timeSlot por índice
    def getTimeSlotByIndex(self, index):
        """
        Función que devuelve todos los campos de time slot en la posición
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>, <start>, <end>]
        :param index: Índice de value de timeSlot que queremos obtener.
        :return: Devuelve el value de timeSlot en la posicion index.
        """
        TimeSlot = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            TimeSlot.append(self.getTimeSlot()[index].get("id"))
            TimeSlot.append(self.getTimeSlot()[index].get("start"))
            TimeSlot.append(self.getTimeSlot()[index].get("end"))
            return TimeSlot
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de trainServiceProvider
    def getTrainServiceProviderData(self):
        """
        Funcion que devuelve todos los campos de trainServiceProvider en la
        posicion index ordenados en una lista
        como en el archivo Yaml.\n
        Salida: [<id>,<name>,<{<seat>:<quantity>}>]
        :return: Devuelve el value de trainServiceProvider en la posicion index.
        """
        TrainServiceProvider = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            trainServiceProvider = self.getTrainServiceProvider()
            TrainServiceProvider = [[
                data.get("id"),
                data.get("name"),
                json.dumps(data.get("rolling_stock"))]
                for data in trainServiceProvider
            ]
            return TrainServiceProvider
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de trainServiceProvider por índice
    def getTrainServiceProviderByIndex(self, index):
        """
        Funcion que devuelve todos los campos de trainServiceProvider en la
        posicion index ordenados en una lista
        como en el archivo Yaml.\n
        Salida: [<id>,<name>,<{<seat>:<quantity>}>]
        :param index: Indice del value del trainServiceProvider que queremos
        obtener.
        :return: Devuelve el value de trainServiceProvider en la posicion index.
        """
        TrainServiceProvider = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            TrainServiceProvider.append(
                self.getTrainServiceProvider()[index].get("id"))
            TrainServiceProvider.append(
                self.getTrainServiceProvider()[index].get("name"))
            TrainServiceProvider.append(json.dumps(
                self.getTrainServiceProvider()[index].get("rolling_stock")))
            return TrainServiceProvider
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de stations
    def getStationsData(self):
        """
        Funcion que devuelve todos los campos de stations en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<name>,<city>,<shortName>,{"latitude":>lat>,
        "longitude":<lon>}]
        :return: Devuelve el value de stations en la posicion index.
        """
        Stations = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            stations = self.getStations()
            Stations = [[
                data.get("id"),
                data.get("name"),
                data.get("city"),
                data.get("short_name"),
                json.dumps(data.get("coordinates"))]
                for data in stations
            ]
            return Stations
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de stations por índice
    def getStationsByIndex(self, index):
        """
        Funcion que devuelve todos los campos de stations en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<name>,<city>,<shortName>,{"latitude":>lat>,
        "longitude":<lon>}]
        :param index: Indice del value de stations que queremos obtener.
        :return: Devuelve el value de stations en la posicion index.
        """
        Stations = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            Stations.append(self.getStations()[index].get("id"))
            Stations.append(self.getStations()[index].get("name"))
            Stations.append(self.getStations()[index].get("city"))
            Stations.append(self.getStations()[index].get("short_name"))
            Stations.append(
                json.dumps(self.getStations()[index].get("coordinates")))
            return Stations
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de corridor
    def getCorridorData(self):
        """
        Funcion que devuelve todos los campos de corridor en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>, <name>, <[<station_1>, <station_2>, …, <station_n>]>]
        :return: Devuelve el value de corridor en la posicion index.
        """
        Corridor = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            corridor = self.getCorridor()
            Corridor = [[
                data.get("id"),
                data.get("name"),
                self.extractStationsFromCorridor(data.get("stations"))]
                for data in corridor
            ]
            return Corridor
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de corridor por índice
    def getCorridorByIndex(self, index):
        """
        Funcion que devuelve todos los campos de corridor en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>, <name>, <[<station_1>, <station_2>, …, <station_n>]>]
        :param index: Índice del value de corridor que queremos obtener.
        :return: Devuelve el value de corridor en la posicion index.
        """
        Corridor = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            Corridor.append(self.getCorridor()[index].get("id"))
            Corridor.append(self.getCorridor()[index].get("name"))
            Corridor.append(self.extractStationsFromCorridor(
                self.getCorridor()[index].get("stations")))
            return Corridor
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares de corridor
    def extractStationsFromCorridor(self, stationsData: list, stations=None):
        """
        Extrae los ramales del corredor. Esta función devuelve una lista
        ordenada con todos los ramales. Cada ramal será una lista ordenada
        siendo el primer elemento la estación de inicio del ramal y el último
        elemento será la última estación del ramal.
        :param stationsData: Lista en las que están contenidos los IDs de
        todas las estaciones por las que va a pasar el
        corredor
        :param stations: Ruta actual acumulada (se utiliza internamente al
        llamar recursivamente).
        :return: Devuelve una lista de listas con todos los ramales del
        corredor.
        """
        if stations is None:
            stations = []

        # Se hace una copia de stationsData para evitar modificar el original
        data = deepcopy(stationsData)
        allStations = []

        if isinstance(data, list):
            # Se recorre cada elemento de la lista (cada elemento representa
            # un inicio o ramal)
            for item in data:
                newStations = stations.copy()
                newStations.append(item.get("org"))
                l2 = item.get("des")
                if l2:
                    # Si existen destinos, se llama recursivamente (ya sea
                    # que l2 sea lista o diccionario)
                    if isinstance(l2, (list, dict)):
                        allStations.extend(
                            self.extractStationsFromCorridor(l2, newStations))
                    else:
                        allStations.append(newStations)
                else:
                    # No hay más destinos: se agrega la ruta completa
                    allStations.append(newStations)
        elif isinstance(data, dict):
            # Caso en el que data es un único diccionario
            newStations = stations.copy()
            newStations.append(data.get("org"))
            l2 = data.get("des")
            if l2:
                if isinstance(l2, (list, dict)):
                    allStations.extend(
                        self.extractStationsFromCorridor(l2, newStations))
                else:
                    allStations.append(newStations)
            else:
                allStations.append(newStations)
        else:
            # En caso de que data no tenga el formato esperado, se retorna la
            # ruta actual
            allStations.append(stations)

        return allStations

    # Funciones para campos especificos de seats
    def getSeatData(self):
        """
        Funcion que devuelve todos los campos de seat en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<hardType>,<softType>]
        :return: Devuelve el value de seat en la posicion index.
        """
        Seat = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            seat = self.getSeat()
            Seat = [[
                data.get("id"),
                data.get("name"),
                data.get("hard_type"),
                data.get("soft_type")]
                for data in seat
            ]
            return Seat
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de seats por índice
    def getSeatByIndex(self, index):
        """
        Funcion que devuelve todos los campos de seat en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<hardType>,<softType>]
        :param index: Indice del value de seat que queremos obtener.
        :return: Devuelve el value de seat en la posicion index.
        """
        Seat = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            Seat.append(self.getSeat()[index].get("id"))
            Seat.append(self.getSeat()[index].get("name"))
            Seat.append(self.getSeat()[index].get("hard_type"))
            Seat.append(self.getSeat()[index].get("soft_type"))
            return Seat
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de line
    def getLineData(self):
        """
        Funcion que devuelve todos los campos de line en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<corridor>,<[<[<station>,<arrivalTime>,
        <departureTime>]>,...]>]
        :return: Devuelve el value de line en la posicion index.
        """
        Line = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            line = self.getLine()
            Line = [[
                data.get("id"),
                data.get("name"),
                data.get("corridor"),
                self.extractStopsFromLine(data.get("stops"))]
                for data in line
            ]
            return Line
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de line por índice
    def getLineByIndex(self, index):
        """
        Funcion que devuelve todos los campos de line en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<corridor>,<[<[<station>,<arrivalTime>,
        <departureTime>]>,...]>]
        :param index: Indice de value de line que queremos obtener.
        :return: Devuelve el value de line en la posicion index.
        """
        Line = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            Line.append(self.getLine()[index].get("id"))
            Line.append(self.getLine()[index].get("name"))
            Line.append(self.getLine()[index].get("corridor"))
            Line.append(
                self.extractStopsFromLine(self.getLine()[index].get("stops")))
            return Line
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares de Line
    @staticmethod
    def extractStopsFromLine(stopsData: list):
        """
        Esta función extrae todas las paradas con sus tiempos de llegada y
        salida de una linea.
        Devuelve una lista de listas donde cada lista se compone de la
        parada, tiempo de llegada y tiepo de salida,
        por lo que respeta el orden del archivo Yaml.
        :param stopsData: Lista de diccionarios con los datos de todas las
        paradas en la linea.
        :return: lista de listas con los datos de todas las paradas de la linea.
        """
        stops = []
        data = deepcopy(stopsData)
        while data:
            stops.append(
                [str(data[0].get("station")), data[0].get("arrival_time"),
                 data[0].get("departure_time")])
            data.pop(0)
        return stops

    # Funciones para campos especificos de rollingStock
    def getRollingStockData(self):
        """
        Funcion que devuelve todos los campos de line en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<{<seat>:<quantity>}>]
        :return: Devuelve el value de line en la posicion index.
        """
        RollingStock = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            rollingStock = self.getRollingStock()
            RollingStock = [[
                data.get("id"),
                data.get("name"),
                json.dumps(
                    self.extractSeatsFromRollingStock(data.get("seats")))]
                for data in rollingStock
            ]
            return RollingStock
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de rollingStock por índice
    def getRollingStockByIndex(self, index):
        """
        Funcion que devuelve todos los campos de line en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<name>,<{<seat>:<quantity>}>]
        :param index: Indice de value de line que queremos obtener.
        :return: Devuelve el value de line en la posicion index.
        """
        RollingStock = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            RollingStock.append(self.getRollingStock()[index].get("id"))
            RollingStock.append(self.getRollingStock()[index].get("name"))
            RollingStock.append(
                json.dumps(self.extractSeatsFromRollingStock(
                    self.getRollingStock()[index].get("seats"))))
            return RollingStock
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares de rollingStock
    @staticmethod
    def extractSeatsFromRollingStock(seatsData: list):
        """
        Esta funcion extrae los datos de los asientos de uno de los trenes de
        rollingStock pasado como parametro.
        Devuelve un diccionario que emplea como key el hard_type y como value
        para esa key el numero de asientos de
        ese tipo de los que dispone dicho tren.
        :param seatsData: Datos extraidos de seats en rollingStock.
        :return: Devuelve un diccionario con los tipos de asiento y la
        cantidad de estos.
        """
        seats = {}
        data = deepcopy(seatsData)
        while data:
            seats.update(
                {str(data[0].get("hard_type")): data[0].get("quantity")})
            data.pop(0)
        return seats

    # Funciones para campos especificos de service
    def getServiceData(self):
        """
        Funcion que devuelve todos los campos de service en la posicion index
        ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<date>,<line>,<trainServiceProvider>,<timeSlot>,
        <rollingStock>,<[[<origin>,<destination>,
        <{<seat>:<price>}>],...]>,<{"restrictionName":restrictionValue,...}>]
        :return: Devuelve el value de service en la posicion index.
        """
        Service = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            service = self.getService()
            Service = [[
                           data.get("id"),
                           data.get("date"),
                           data.get("line"),
                           data.get("train_service_provider"),
                           data.get("time_slot"),
                           data.get("rolling_stock"),
                           self.extractSeatsPriceFromServiceOdt(
                               data.get("origin_destination_tuples"))]
                       +
                       [{str(restriction): data.get(str(restriction))} for
                        restriction in [
                            key for key in list(data.keys()) if
                            key not in ["id", "date", "line",
                                        "train_service_provider",
                                        "time_slot", "rolling_stock",
                                        "origin_destination_tuples"]]]
                       for data in service
                       ]
            return Service
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de service por índice
    def getServiceByIndex(self, index):
        """
        Funcion que devuelve todos los campos de service en la posicion index
        ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<date>,<line>,<trainServiceProvider>,<timeSlot>,
        <rollingStock>,<[[<origin>,<destination>,
        <{<seat>:<price>}>],...]>,<{"restrictionName":restrictionValue,...}>]
        :param index: Indice de value de service que queremos obtener.
        :return: Devuelve el value de service en la posicion index.
        """
        Service = []
        try:
            if self.supplyData is None: raise EmptySupplyData
            Service.append(self.getService()[index].get("id"))
            Service.append(self.getService()[index].get("date"))
            Service.append(self.getService()[index].get("line"))
            Service.append(
                self.getService()[index].get("train_service_provider"))
            Service.append(self.getService()[index].get("time_slot"))
            Service.append(self.getService()[index].get("rolling_stock"))
            Service.append(
                self.extractSeatsPriceFromServiceOdt(
                    self.getService()[index].get("origin_destination_tuples")))
            Service.append({"capacity_constraints": self.getService()[
                index].get("capacity_constraints")})
            return Service
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares de service
    @staticmethod
    def extractSeatsPriceFromServiceOdt(odtData: list):
        data = deepcopy(odtData)
        outputData = []
        while data:
            price = {}
            seats = data[0].get("seats")
            odt = data[0]
            while seats:
                price.update({str(seats[0].get("seat")): seats[0].get("price")})
                seats.pop(0)
            output = [odt.get("origin"), odt.get("destination"),
                      deepcopy(price)]
            outputData.append(output)
            data.pop(0)
        return outputData

    # Funciones para el archivo de demanda
    # Funciones para campos especificos de market
    def getMarketData(self):
        """
        Funcion que devuelve todos los campos de market en la posicion index
        ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<departure_station>,<[<departure_station_coords>]>,
        <arrival_station>,<timeSlot>,
        <[<arrival_station_coords>]>]
        :return: Devuelve el value de market en la posicion index.
        """
        Market = []
        try:
            if self.demandData is None: raise EmptyDemandData
            market = self.getMarket()
            Market = [
                [
                    market[index].get("id"),
                    market[index].get("departure_station"),
                    json.dumps(market[index].get("departure_station_coords")),
                    market[index].get("arrival_station"),
                    json.dumps(market[index].get("arrival_station_coords"))]

                for index in range(0, len(market))
            ]

            return Market
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de market por índice
    def getMarketByIndex(self, index):
        """
        Funcion que devuelve todos los campos de market en la posicion index
        ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<departure_station>,<[<departure_station_coords>]>,
        <arrival_station>,<timeSlot>,
        <[<arrival_station_coords>]>]
        :param index: Indice de value de market que queremos obtener.
        :return: Devuelve el value de market en la posicion index.
        """
        Market = []
        try:
            if self.demandData is None: raise EmptyDemandData
            Market.append(self.getMarket()[index].get("id"))
            Market.append(self.getMarket()[index].get("departure_station"))
            Market.append(json.dumps(
                self.getMarket()[index].get("departure_station_coords")))
            Market.append(self.getMarket()[index].get("arrival_station"))
            Market.append(json.dumps(
                self.getMarket()[index].get("arrival_station_coords")))
            return Market
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de day
    def getDayData(self):
        """
        Funcion que devuelve todos los campos de day en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<departure_station>,<[<departure_station_coords>]>,
        <arrival_station>,<timeSlot>,
        <[<arrival_station_coords>]>]
        :return: Devuelve el value de day en la posicion index.
        """
        Day = []
        try:
            if self.demandData is None: raise EmptyDemandData
            day = self.getDay()
            Day = [
                [
                    day[index].get("id"),
                    str(day[index].get("date")),
                    day[index].get("demandPattern")]

                for index in range(0, len(day))
            ]

            return Day
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de day por índice
    def getDayByIndex(self, index):
        """
        Funcion que devuelve todos los campos de day en la posicion index
        ordenados en una lista como en el archivo
        Yaml.\n
        Salida: [<id>,<date>,<demandPattern>]
        :param index: Indice de value de day que queremos obtener.
        :return: Devuelve el value de day en la posicion index.
        """
        Day = []
        try:
            if self.demandData is None: raise EmptyDemandData
            Day.append(self.getDay()[index].get("id"))
            Day.append(str(self.getDay()[index].get("date")))
            Day.append(self.getDay()[index].get("demandPattern"))
            return Day
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de demmandPattern
    def getDemandPatternData(self):
        """
        Funcion que devuelve todos los campos de demandPattern en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<name>,<[<[<market>,<potential_demand>,
        <{"low":<lowValue>,"high":<highValue>}>,
        <{<id_1>:<percentage_1>,...,<id_n>:<percentage_n>}>]*n_markets>]>]
        :return: Devuelve el value de demandPattern en la posicion index.
        """
        DemandPattern = []
        try:
            if self.demandData is None: raise EmptyDemandData
            demandPattern = self.getDemandPattern()
            DemandPattern = [
                [
                    demandPattern[index].get("id"),
                    demandPattern[index].get("name"),
                    self.extractMarketsFromDemmandPattern(
                        demandPattern[index].get("markets"))]

                for index in range(0, len(demandPattern))
            ]

            return DemandPattern
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de demmandPattern por índice
    def getDemandPatternByIndex(self, index):
        """
        Funcion que devuelve todos los campos de demandPattern en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<name>,<[<[<market>,<potential_demand>,
        <{"low":<lowValue>,"high":<highValue>}>,
        <{<id_1>:<percentage_1>,...,<id_n>:<percentage_n>}>]*n_markets>]>]
        :param index: Indice de value de demandPattern que queremos obtener.
        :return: Devuelve el value de demandPattern en la posicion index.
        """
        DemmandPattern = []
        try:
            if self.demandData is None: raise EmptyDemandData
            DemmandPattern.append(self.getDemandPattern()[index].get("id"))
            DemmandPattern.append(self.getDemandPattern()[index].get("name"))
            DemmandPattern.append(self.extractMarketsFromDemmandPattern(
                self.getDemandPattern()[index].get("markets")))
            return DemmandPattern
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares para demmandPattern
    def extractMarketsFromDemmandPattern(self, marketsData):
        markets = []
        data = deepcopy(marketsData)
        while data:
            markets.append([data[0].get("market"),
                            data[0].get("potential_demand"),
                            json.dumps(data[0].get("potential_demand_kwargs")),
                            self.extractUserPatternDistributionFromMarkets(
                                data[0].get("user_pattern_distribution"))])
            data.pop(0)
        return markets

    @staticmethod
    def extractUserPatternDistributionFromMarkets(UpdData):
        percentage = {}
        data = deepcopy(UpdData)
        while data:
            percentage.update(
                {str(data[0].get("id")): data[0].get("percentage")})
            data.pop(0)
        return percentage

    # Funciones para campos especificos de userPattern
    def getUserPatternData(self):
        """
        Funcion que devuelve todos los campos de userPattern en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<departure_station>,<[<departure_station_coords>]>,
        <arrival_station>,<timeSlot>,
        <[<arrival_station_coords>]>]
        :return: Devuelve el value de userPattern en la posicion index.
        """
        UserPattern = []
        try:
            if self.demandData is None: raise EmptyDemandData
            userPattern = self.getUserPattern()
            UserPattern = [
                [
                    userPattern[index].get("id"),
                    userPattern[index].get("name"),
                    json.dumps(userPattern[index].get("rules")),
                    self.reformatVariableSets(
                        userPattern[index].get("variables")),
                    userPattern[index].get("arrival_time"),
                    json.dumps(userPattern[index].get("arrival_time_kwargs")),
                    userPattern[index].get("purchase_day"),
                    json.dumps(userPattern[index].get("purchase_day_kwargs")),
                    json.dumps(
                        userPattern[index].get("forbidden_departure_hours")),
                    json.dumps(self.extractSeatsFromUserPattern(
                        userPattern[index].get("seats"))),
                    json.dumps(self.extractTrainServiceProvidersFromUserPattern(
                        userPattern[index].get("train_service_providers"))),
                    userPattern[index].get("early_stop"),
                    userPattern[index].get("utility_threshold"),
                    userPattern[index].get("error"),
                    json.dumps(userPattern[index].get("error_kwargs"))]

                for index in range(0, len(userPattern))
            ]

            return UserPattern
        except Exception as e:
            print(e)
            return -1

    # Funciones para campos especificos de userPattern por índice
    def getUserPatternByIndex(self, index):
        """
        Funcion que devuelve todos los campos de userPattern en la posicion
        index ordenados en una lista como en el
        archivo Yaml.\n
        Salida: [<id>,<name>,{'R0':<rule_0>,...,'Rn':<rule_n>},
        {"name":<name>,"type":<type>,"support":<support>,
        "sets":{<name_set_0>:<set_0>,...,<name_set_n>:<set_n>}/"labels":[
        <label_0>,...,<label_n>]},<arrival_time>,
        {"loc":<locAtkValue>,"scale":<scaleAtkValue>},<purchase_day>,
        {"low":<lowValue>,"high":<highValue>},
        {"start":<FdhStart>,"end":<FdhEnd>},{<seatID_0>:<utility_0>,...,
        <seatID_n>:<utility_n>},
        {"<TspID_0>":<utility_0>,...,"<TspID_n>":<utility_n>},<early_stop>,
        <utility_threshold>,<error>,
        {"loc":<locErrorValue>,"scale":<scaleErrorValue>}]\n
        Tsp: train_service_provider.\n
        Fdh: forbidden_departure_hours.\n
        Atk: arrival_time_kwargs.\n
        :param index: Indice de value de userPattern que queremos obtener.
        :return: Devuelve el value de userPattern en la posicion index.
        """
        UserPattern = []
        try:
            if self.demandData is None: raise EmptyDemandData
            UserPattern.append(self.getUserPattern()[index].get("id"))
            UserPattern.append(self.getUserPattern()[index].get("name"))
            UserPattern.append(
                json.dumps(self.getUserPattern()[index].get("rules")))
            UserPattern.append(self.reformatVariableSets(
                self.getUserPattern()[index].get("variables")))
            UserPattern.append(self.getUserPattern()[index].get("arrival_time"))
            UserPattern.append(json.dumps(
                self.getUserPattern()[index].get("arrival_time_kwargs")))
            UserPattern.append(self.getUserPattern()[index].get("purchase_day"))
            UserPattern.append(json.dumps(
                self.getUserPattern()[index].get("purchase_day_kwargs")))
            UserPattern.append(json.dumps(
                self.getUserPattern()[index].get("forbidden_departure_hours")))
            UserPattern.append(json.dumps(self.extractSeatsFromUserPattern(
                self.getUserPattern()[index].get("seats"))))
            UserPattern.append(
                json.dumps(self.extractTrainServiceProvidersFromUserPattern(
                    self.getUserPattern()[index].get(
                        "train_service_providers"))))
            UserPattern.append(self.getUserPattern()[index].get("early_stop"))
            UserPattern.append(
                self.getUserPattern()[index].get("utility_threshold"))
            UserPattern.append(self.getUserPattern()[index].get("error"))
            UserPattern.append(
                json.dumps(self.getUserPattern()[index].get("error_kwargs")))
            return UserPattern
        except IndexError:
            print("Se ha sobrepasado el índice máximo")
            return "indexError"
        except Exception as e:
            print(e)
            return -1

    # Funciones auxiliares para userPattern

    @staticmethod
    def extractSeatsFromUserPattern(seatsData):
        seats = {}
        data = deepcopy(seatsData)
        while data:
            seats.update({str(data[0].get("id")): data[0].get("utility")})
            data.pop(0)
        return seats

    @staticmethod
    def extractTrainServiceProvidersFromUserPattern(tspData):
        tsp = {}
        data = deepcopy(tspData)
        while data:
            tsp.update({str(data[0].get("id")): data[0].get("utility")})
            data.pop(0)
        return tsp

    @staticmethod
    def reformatVariableSets(variableData: dict):
        outputData = []
        for varData in variableData:
            if "labels" in varData.keys():
                outputData.append(varData)
            else:
                data = deepcopy(varData)
                variables = {"name": data.get("name"), "type": data.get("type"),
                             "support": data.get("support")}
                setsData = data.get("sets")
                sets = {}
                while setsData:
                    sets.update({str(setsData[0]): data.get(setsData[0])})
                    setsData.pop(0)
                variables.update({"sets": sets})
                outputData.append(variables)
        return outputData
