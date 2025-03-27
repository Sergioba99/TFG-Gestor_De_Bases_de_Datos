from Modules.yamlParser import Parser
from Modules import SQLHandler
from Modules import csvHandler

class SupplyLoger:
    """
        Clase del módulo dataLoger que se encarga de introducir los datos extraidos de los archivos yaml de la oferta
        a la base de datos de la oferta
        :param yml: objeto del módulo yamlParser para extraer los datos del yaml
        :param sqlSupply: objeto del módulo SQLHandler que se encarga de la base de datos de la oferta
        """

    def __init__(self, yml: Parser, sqlSupply: SQLHandler.SqlSupply):
        self.yml = yml  # objeto del módulo yamlParser para extraer los datos del yaml
        self.sqlSupply = sqlSupply  # objeto del módulo SQLHandler que se encarga de la base de datos de la oferta
        self.testID = None

    # Funciones para introducir datos a la base de datos de la oferta
    # Funcion principal
    def logSupplyTestData(self,observations=""):
        """
        Introduce todos los datos de un test a la base de datos de la oferta apoyandose en subfunciones para este fin
        :return:
        """
        testData = self.yml.supplyFileName
        self.sqlSupply.insertTestsData(testData,observations)
        self.testID = self.sqlSupply.executeSelectTestsIDQuery(f"SELECT ID FROM TESTS WHERE TESTS.NAME='{testData}'")
        print("Tests -> Data: " + str([self.testID, testData]))
        self.logCorridorData()
        self.logRollingStockData()
        self.logStationsData()
        self.logLineData()
        self.logTimeSlotData()
        self.logTrainServiceProviderData()
        self.logSeatData()
        self.logServiceData()
        self.testID = None

    # Funciones auxiliares
    def logCorridorData(self):
        """
        Introduce los datos del corredor a la base de datos de la oferta
        :return:
        """
        data = self.yml.getCorridorData()
        self.sqlSupply.insertCorridorData(data)
        self.sqlSupply.insertAuxCorridorData(data, self.testID)
        self.sqlSupply.insertCorridorStationsData(data, self.testID)

    def logTimeSlotData(self):
        """
        Introduce los datos de los slots de tiempo a la base de datos de la oferta
        :return:
        """
        data = self.yml.getTimeSlotData()
        self.sqlSupply.insertTimeSlotData(data)
        self.sqlSupply.insertAuxTimeSlotData(data, self.testID)

    def logStationsData(self):
        """
        Introduce los datos de las estaciones a la base de datos de la oferta
        :return:
        """

        data = self.yml.getStationsData()
        self.sqlSupply.insertStationsData(data)
        self.sqlSupply.insertAuxStationsData(data, self.testID)

    def logRollingStockData(self):
        """
        Introduce los datos del stock rodante a la base de datos de la oferta
        :return:
        """
        data = self.yml.getRollingStockData()
        self.sqlSupply.insertRollingStockData(data)
        self.sqlSupply.insertAuxRollingStockData(data, self.testID)
            
    def logSeatData(self):
        """
        Introduce los datos de los asientos a la base de datos de la oferta
        :return:
        """
        data = self.yml.getSeatData()
        self.sqlSupply.insertSeatData(data)
        self.sqlSupply.insertAuxSeatData(data, self.testID)

    def logTrainServiceProviderData(self):
        """
        Introduce los datos de los proveedores de servicios ferroviarios a la base de datos de la oferta
        :return:
        """
        data = self.yml.getTrainServiceProviderData()
        self.sqlSupply.insertTrainServiceProviderData(data)
        self.sqlSupply.insertAuxTrainServiceProviderData(data, self.testID)

    def logLineData(self):
        """
        Introduce los datos de las líneas a la base de datos de la oferta
        :return:
        """
        data = self.yml.getLineData()
        self.sqlSupply.insertLineData(data)
        self.sqlSupply.insertStopsData(data,self.testID)

    def logServiceData(self):
        """
        Introduce los datos de los servicios a la base de datos de la oferta
        :return:
        """
        data = self.yml.getServiceData()
        self.sqlSupply.insertServiceData(data)
        self.sqlSupply.insertAuxServiceData(data, self.testID)
        self.sqlSupply.insertOdtData(data, self.testID)
        self.sqlSupply.insertRestrictionsData(data)
        self.sqlSupply.insertSeatsPriceData(data,self.testID)

class DemandLoger:
    def __init__(self,yml:Parser,sqlDemand:SQLHandler.SqlDemand):
        self.yml = yml              # objeto del módulo yamlParser para extraer los datos del yaml
        self.sqlDemand = sqlDemand  # objeto del módulo SQLHandler que se encarga de la base de datos de la demanda
        self.testID = None

    # Funciones para introducir datos a la base de datos de la demanda
    # Funcion principal
    def logDemandTestData(self,observations=""):
        """
        Introduce todos los datos de un test a la base de datos de la demanda apoyandose en subfunciones para este fin
        :return:
        """
        testData = self.yml.demandFileName
        self.sqlDemand.insertTestData(testData,observations)
        self.testID = self.sqlDemand.executeSelectTestsIDQuery(
            f"SELECT ID FROM TESTS WHERE TESTS.NAME='{testData}'")
        print("Tests -> Data: " + str([self.testID, testData]))

        self.logMarketData()
        self.logUserPatternData()
        self.logDemandPatternData()
        self.logDayData()

    # Funciones auxiliares
    def logMarketData(self):
        """
        Introduce los datos de los mercados a la base de datos de la demanda
        :return:
        """

        data = self.yml.getMarketData()
        self.sqlDemand.insertMarketData(data)
        self.sqlDemand.insertAuxMarketData(data, self.testID)

    def logUserPatternData(self):
        """
        Introduce los datos de los patrones de usuario a la base de datos de la demanda
        :return:
        """

        data = self.yml.getUserPatternData()
        self.sqlDemand.insertUserPatternData(data)
        self.sqlDemand.insertAuxUserPatternData(data, self.testID)
        self.sqlDemand.insertVariableData(data)

    def logDemandPatternData(self):
        """
        Introduce los datos de los patrones de demanda a la base de datos de la demanda
        :return:
        """
        data = self.yml.getDemandPatternData()
        self.sqlDemand.insertDemandPatternData(data)
        self.sqlDemand.insertAuxDemandPatternData(data, self.testID)
        self.sqlDemand.insertMarketsData(data)
        self.sqlDemand.insertUserPatternDistributionData(data)

    def logDayData(self):
        """
        Introduce los datos del día a la base de datos de la demanda
        :return:
        """
        data = self.yml.getDayData()
        self.sqlDemand.insertDayData(data)
        self.sqlDemand.insertAuxDayData(data, self.testID)

class ResultsLoger:
    def __init__(self,csvReader:csvHandler.csvReader,sqlResults:SQLHandler.SqlResults):
        self.csv = csvReader            # objeto del módulo csvHandler para extraer los datos del csv
        self.sqlResults = sqlResults    # objeto del modulo SQLHandler encargado de la base de datos de los resultados
        self.testID = None

    # Funciones para introducir datos a la base de datos de resultados

    def logResultsTestData(self,observations=""):
        testData = self.csv.csvFileName
        self.sqlResults.insertTestData(testData,observations)
        self.testID = self.sqlResults.executeSelectTestsIDQuery(
            f"SELECT ID FROM TESTS WHERE TESTS.NAME='{testData}'")
        print("Tests -> Data: " + str([self.testID, testData]))

        self.logResultsData()

    # Funciones auxiliares
    def logResultsData(self):
        """
        Introduce los datos de los resultados a la base de datos de resultados
        :return:
        """

        data = self.csv.csvData
        self.sqlResults.insertResultsData(data)
        self.sqlResults.insertAuxReslutsData(data,self.testID)