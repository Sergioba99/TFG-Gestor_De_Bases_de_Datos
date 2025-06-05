import json
import os
from copy import deepcopy
from pathlib import Path


class Config:
    """Modulo encargado de gestionar la configuracion de la aplicacion"""

    def __init__(self):
        self.configData = None
        self.workingDirectory = os.getcwd()
        self.configFolderPath = self.workingDirectory + "/config"
        self.configFilePath = self.configFolderPath + "/config.json"
        Path(self.configFolderPath).mkdir(parents=True, exist_ok=True)
        if not Path(self.configFilePath).exists():
            self.generateDefaultConfig()
        else:
            self.getConfig()

    def generateDefaultConfig(self):
        """
        Esta función genera la configuracion inicial para la aplicación, la cual contiene querys de SQL utiles
        y bastante usadas en las bases de datos que maneja el programa.
        :return: None
        """
        try:
            data = {
                'SQL_Querys': {
                    "Mostrar test de oferta": {"db": "oferta", "query": "SELECT * FROM TESTS"},
                    "Mostrar test de demanda": {"db": "demanda", "query": "SELECT * FROM TESTS"},
                    "Mostrar test de resultados": {"db": "resultados", "query": "SELECT * FROM TESTS"}
                }
            }
            self.configData = deepcopy(data)
            with open(self.configFilePath, 'w') as configFile:
                json.dump(data, configFile, indent=4)
        except Exception as e:
            print(e)

    def getConfig(self):
        """
        Esta función carga la configuración presente en el archivo de configuración y lo almacena dentro de la variable
        del objeto llamada configData.
        :return: None
        """
        try:
            with open(self.configFilePath, 'r') as configFile:
                self.configData = json.load(configFile)
        except Exception as e:
            print(e)

    def saveConfig(self):
        """
        Esta función se encarga de volcar la configuración presente en la variable configData al archivo JSON que
        almacena
        la configuración de la aplicación.
        :return: None
        """
        try:
            with open(self.configFilePath, 'w') as configFile:
                json.dump(self.configData, configFile, indent=4)

        except Exception as e:
            print(e)

    def getSQLQuerys(self):
        """
        Esta función devuelve todas las querys almacenadas en el archivo de configuración
        :return: sqlQuerys
        """

        try:
            data = deepcopy(self.configData)
            sqlQuerys = data.get("SQL_Querys")
            if not sqlQuerys: return -2
            return sqlQuerys
        except Exception as e:
            print(e)
            return -1

    def getSQLQuerysNames(self):
        try:
            querysKeys = list(self.getSQLQuerys().keys())
            if not querysKeys: return -2
            return querysKeys

        except Exception as e:
            print(e)
            return -1

    def getSQLQueryValue(self, key):
        try:
            data = self.configData["SQL_Querys"].get(key)
            db = str(data.get("db"))
            query = str(data.get("query"))
            if not query or not db: return -2
            return db, query

        except Exception as e:
            print(e)
            return -1

    def addSQLQuery(self, name, db, query):
        """
        Esta función se encarga de añadir querys de SQL a la lista almacenada en el archivo de configuración
        :return: None
        """
        try:
            self.configData["SQL_Querys"].update({str(name): {"db": str(db), "query": str(query)}})
            self.saveConfig()
        except Exception as e:
            print(e)

    def removeSQLQuery(self, name):
        """
        Esta función se encarga de eliminar querys de SQL a la lista almacenada en el archivo de configuración
        :return: None
        """
        try:
            self.configData["SQL_Querys"].pop(name)
            self.saveConfig()
        except Exception as e:
            print(e)

    def resetConfig(self):
        """
        Esta función reinicia la configuración a los valores por defecto
        :return: None
        """
        self.generateDefaultConfig()
