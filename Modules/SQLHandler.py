# Importamos las librerias necesarias para que el módulo SQLHandler funcione
import json
import os
import sqlite3
from pathlib import Path


# Excepcion personalizada para test vacios en la base de datos de la oferta
class EmptyTestData(Exception):
    """
        Excepción que indica que no hay ningun test dentro de la base de datos
    """

    def __init__(self):
        self.message = (
            "No existen datos de ningun test dentro de la base de datos, "
            "esto puede deberse a un error "
            "o a que la base de datos se encuentra vacia")
        super().__init__(self.message)


class SqlSupply:
    """
    Módulo que se encarga de gestionar la entrada y salida de datos de la
    base de datos de la oferta
    :param db: Direccion de la base de datos de la oferta, por defecto será:
    <currentWorkingDirectory>/Database/supplyDb.db
    """

    # Inicializacion del objeto SqlSupply, encargado de manejar las
    # interacciones con la base de datos de la oferta
    def __init__(self, db=None):
        self.workingDirectory = os.getcwd()  # Directorio de trabajo
        self.defaultDatabaseFolder = self.workingDirectory + "/Database"  #
        # Directorio para las bases de datos
        Path(self.defaultDatabaseFolder).mkdir(parents=True,
                                               exist_ok=True)  # Generamos la
        # carpeta Database en caso de no existir
        self.defaultSupplyPath = self.defaultDatabaseFolder + "/supplyDb.db"
        # Direccion de la base de datos por
        # defecto
        self.conector = sqlite3.connect(
            db if db is not None  # Creamos la conexion con la base de datos
            # de la oferta
            else self.defaultSupplyPath)  # Si la base de datos no existe,
        # se generara
        # automaticamente
        self.cursor = self.conector.cursor()  # Creamos el cursor para la
        # base de datos
        self.enableForeignKeys()  # Habilitamos el uso de las claves foraneas
        # en la base de datos

        self.generateDatabaseTables()  # Generamos las tablas de la base de
        # datos si estas no existen

    def enableForeignKeys(self):
        self.cursor.execute(
            "PRAGMA foreign_keys = ON")  # Habilita las claves foraneas
        # usando los PRAGMA de sqlite3
        self.conector.commit()

    def initCursor(self):
        """
        Inicializa el cursor de la base de datos, en caso de que se haya
        cerrado anteriormente.
        :return:
        """
        self.cursor = self.conector.cursor()

    def executeSelectTestsIDQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            data = self.cursor.fetchone()[0]
            return data
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
        return -1

    def executeQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            self.conector.commit()

            strippedQuery = query.strip().upper()

            if strippedQuery.startswith("SELECT"):
                cols = [item[0] for item in self.cursor.description]
                result = self.cursor.fetchall()
                return cols, result

        except sqlite3.Error as e:
            print(e)
            return -1
        except Exception as e:
            print(e)
            return -1
        except sqlite3.ProgrammingError as e:
            print(e)
            return -1
        finally:
            self.cursor.close()

    def generateDatabaseTables(self):
        """
        Genera las tablas de la base de datos, si estas no existieran
        previamente
        :return:
        """
        self.createTestsTable()
        self.createCorridorTable()
        self.createAuxCorridorTable()
        self.createCorridorStationsTable()
        self.createOriginDestinationTuplesTable()
        self.createSeatTable()
        self.createAuxSeatTable()
        self.createTrainServiceProviderTable()
        self.createAuxTrainServiceProviderTable()
        self.createRollingStockTable()
        self.createAuxRollingStockTable()
        self.createTimeSlotTable()
        self.createAuxTimeSlotTable()
        self.createStationsTable()
        self.createAuxStationsTable()
        self.createLineTable()
        self.createStopsTable()
        self.createSeatsPriceTable()
        self.createServiceTable()
        self.createAuxServiceTable()
        self.createRestrictionsTable()

    # Generadores de las tablas de la base de datos de la oferta
    def createCorridorTable(self):
        """
        Genera la tabla CORRIDOR en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS CORRIDOR (
                            ID          TEXT PRIMARY KEY,
                            
                            NAME        TEXT,
                            
                            UNIQUE(ID,NAME)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxCorridorTable(self):
        """
        Genera la tabla AUX_CORRIDOR en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_CORRIDOR (
                            ID  INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,

                            CORRIDOR_ID TEXT REFERENCES CORRIDOR (ID) ON 
                            DELETE CASCADE
                                                                      ON 
                                                                      UPDATE 
                                                                      CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,
                            UNIQUE(CORRIDOR_ID, TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createCorridorStationsTable(self):
        """
        Genera la tabla CORRIDOR_STATIONS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS CORRIDOR_STATIONS (
                            ID       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            TEST_ID          REFERENCES TESTS (ID) ON DELETE 
                            CASCADE
                                                                   ON UPDATE 
                                                                   CASCADE,
                            
                            CORRIDOR TEXT    REFERENCES CORRIDOR (ID) ON 
                            DELETE CASCADE
                                                                      ON 
                                                                      UPDATE 
                                                                      CASCADE,
                            STATIONS JSON,
                            UNIQUE(TEST_ID,CORRIDOR, STATIONS)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createLineTable(self):
        """
        Genera la tabla LINE en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS LINE (
                            ID          TEXT PRIMARY KEY,

                            NAME        TEXT,
                            
                            CORRIDOR    TEXT REFERENCES CORRIDOR (ID) ON 
                            DELETE CASCADE
                                                                      ON 
                                                                      UPDATE 
                                                                      CASCADE,
                            
                            UNIQUE(ID,NAME,CORRIDOR)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createOriginDestinationTuplesTable(self):
        """
        Genera la tabla ORIGIN_DESTINATION_TUPLES en la base de datos,
        si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS ORIGIN_DESTINATION_TUPLES (
                            ID          TEXT UNIQUE PRIMARY KEY,
                            TEST_ID     TEXT REFERENCES TESTS (ID) ON DELETE 
                            CASCADE
                                                                   ON UPDATE 
                                                                   CASCADE,
                            SERVICE_ID  TEXT REFERENCES SERVICE (ID) ON 
                            DELETE CASCADE
                                                                     ON 
                                                                     UPDATE 
                                                                     CASCADE,
                            ORIGIN      TEXT,
                            
                            DESTINATION TEXT,
                            
                            SEATS       JSON
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createRollingStockTable(self):
        """
        Genera la tabla ROLLING_STOCK en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS ROLLING_STOCK (
                            ID          INTEGER PRIMARY KEY AUTOINCREMENT 
                            UNIQUE,
                            
                            ID_ON_FILE  TEXT,
                            
                            NAME                TEXT,
                            
                            SEATS               JSON
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxRollingStockTable(self):
        """
        Genera la tabla AUX_ROLLING_STOCK en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_ROLLING_STOCK (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,

                            ROLLING_STOCK_ID TEXT REFERENCES ROLLING_STOCK (
                            ID) ON DELETE CASCADE
                                                                                ON UPDATE CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(ROLLING_STOCK_ID,TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createSeatTable(self):
        """
        Genera la tabla SEAT en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS SEAT (
                            ID          INTEGER PRIMARY KEY AUTOINCREMENT 
                            UNIQUE,
                            
                            ID_ON_FILE  TEXT,

                            NAME        TEXT,

                            HARD_TYPE   TEXT,
                            
                            SOFT_TYPE   TEXT
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxSeatTable(self):
        """
        Genera la tabla AUX_SEAT en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_SEAT (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,

                            SEAT_ID TEXT REFERENCES SEAT (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(SEAT_ID,TEST_ID)                           
                                 
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createSeatsPriceTable(self):
        """
        Genera la tabla SEATS_PRICE en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS SEATS_PRICE (
                            ID     INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                            ODT_ID TEXT    REFERENCES 
                            ORIGIN_DESTINATION_TUPLES (ID) ON DELETE CASCADE
                                                                                     ON UPDATE CASCADE,
                            SEAT   TEXT,
                            PRICE  REAL,
                            UNIQUE(ODT_ID,SEAT,PRICE)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createServiceTable(self):
        """
        Genera la tabla SERVICE en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS SERVICE (
                            ID                        TEXT PRIMARY KEY,

                            DATE                      DATE,
                            
                            LINE                      TEXT REFERENCES LINE (
                            ID) ON DELETE CASCADE
                                                                                ON UPDATE CASCADE,
                            TRAIN_SERVICE_PROVIDER    TEXT REFERENCES 
                            TRAIN_SERVICE_PROVIDER (ID) ON DELETE CASCADE
                                                                                                  ON UPDATE CASCADE,
                                                                                                  
                            TIME_SLOT                 TEXT REFERENCES 
                            TIME_SLOT (ID) ON DELETE CASCADE
                                                                                     ON UPDATE CASCADE,
                                                                                     
                            ROLLING_STOCK             TEXT REFERENCES 
                            ROLLING_STOCK (ID) ON DELETE CASCADE
                                                                                         ON UPDATE CASCADE,
                                                                                         
                            UNIQUE(ID,DATE,LINE,TRAIN_SERVICE_PROVIDER,
                            TIME_SLOT,ROLLING_STOCK)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxServiceTable(self):
        """
        Genera la tabla AUX_SERVICE en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_SERVICE (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,

                            SERVICE_ID TEXT REFERENCES SERVICE (ID) ON DELETE 
                            CASCADE
                                                                    ON UPDATE 
                                                                    CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(SERVICE_ID, TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createStationsTable(self):
        """
        Genera la tabla STATIONS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS STATIONS (
                            ID          TEXT PRIMARY KEY,
                            
                            NAME        TEXT,
                            CITY        TEXT,
                            SHORT_NAME  TEXT,
                            COORDINATES JSON,
                            UNIQUE(ID,NAME,CITY,SHORT_NAME)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxStationsTable(self):
        """
        Genera la tabla AUX_STATIONS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_STATIONS (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            
                            STATIONS_ID TEXT REFERENCES STATIONS (ID) ON 
                            DELETE CASCADE
                                                                      ON 
                                                                      UPDATE 
                                                                      CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(STATIONS_ID, TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createStopsTable(self):
        """
        Genera la tabla STOPS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS STOPS (
                            ID             INTEGER PRIMARY KEY AUTOINCREMENT,
                            TEST_ID        TEXT    REFERENCES TESTS (ID) ON 
                            DELETE CASCADE
                                                                         ON 
                                                                         UPDATE CASCADE,
                            LINE_ID        TEXT    REFERENCES LINE (ID) ON 
                            DELETE CASCADE
                                                                             ON UPDATE CASCADE,
                            STATION        TEXT    REFERENCES STATIONS (ID) 
                            ON DELETE CASCADE
                                                                                     ON UPDATE CASCADE,
                            ARRIVAL_TIME   INTEGER,
                            DEPARTURE_TIME INTEGER,
                            UNIQUE(TEST_ID,LINE_ID,STATION,ARRIVAL_TIME,
                            DEPARTURE_TIME)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createTimeSlotTable(self):
        """
        Genera la tabla TIME_SLOT en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS TIME_SLOT (
                            ID              TEXT PRIMARY KEY,

                            START           TEXT,
                            END             TEXT,
                            UNIQUE(ID,START,END)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxTimeSlotTable(self):
        """
        Genera la tabla AUX_TIME_SLOT en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_TIME_SLOT(
                            ID              INTEGER UNIQUE PRIMARY KEY 
                            AUTOINCREMENT,

                            TIME_SLOT_ID    REFERENCES TIME_SLOT (ID) ON 
                            DELETE CASCADE
                                                                        ON 
                                                                        UPDATE CASCADE,

                            TEST_ID         REFERENCES TESTS (ID) ON DELETE 
                            CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(TIME_SLOT_ID,TEST_ID)                      
                                                                    
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createTrainServiceProviderTable(self):
        """
        Genera la tabla TRAIN_SERVICE_PROVIDER en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS TRAIN_SERVICE_PROVIDER (
                            ID          INTEGER PRIMARY KEY AUTOINCREMENT 
                            UNIQUE,
                            
                            ID_ON_FILE  TEXT,

                            NAME                        TEXT,
                            ROLLING_STOCK               JSON
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxTrainServiceProviderTable(self):
        """
        Genera la tabla AUX_TRAIN_SERVICE_PROVIDER en la base de datos,
        si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_TRAIN_SERVICE_PROVIDER (
                            ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,

                            TRAIN_SERVICE_PROVIDER_ID REFERENCES 
                            TRAIN_SERVICE_PROVIDER (ID) ON DELETE CASCADE
                                                                                             ON UPDATE CASCADE,

                            TEST_ID     REFERENCES TESTS (ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,

                            UNIQUE(TRAIN_SERVICE_PROVIDER_ID,TEST_ID)         
                                               
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createTestsTable(self):
        """
        Genera la tabla TESTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS TESTS (
                            ID           INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME         TEXT UNIQUE ON CONFLICT IGNORE,
                            OBSERVATIONS TEXT
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createRestrictionsTable(self):
        """
        Genera la tabla RESTRICTIONS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS RESTRICTIONS (
                            ID          INTEGER PRIMARY KEY AUTOINCREMENT,
                            SERVICE_ID  TEXT    REFERENCES SERVICE (ID) ON 
                            DELETE CASCADE
                                                                                ON UPDATE CASCADE,
                            TYPE        TEXT,
                            RESTRICTION JSON,
                            UNIQUE(SERVICE_ID,TYPE)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    # Funciones para introducir los datos a la base de datos de la oferta
    def insertCorridorData(self, corridorData):
        """
        Inserta los datos del corredor en la tabla CORRIDOR
        :param corridorData: Datos del corredor
        :return:
        """
        self.initCursor()
        id = []
        try:
            query = "INSERT OR IGNORE INTO CORRIDOR (ID,NAME) VALUES (?,?)"
            data = [corridor[:2]
                    for corridor in corridorData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, data)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()
        return id

    def insertAuxCorridorData(self, corridorData, testID):
        """
        Inserta los datos auxiliares del corredor en la tabla AUX_CORRIDOR
        :param corridorData: Datos del corredor
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_CORRIDOR (CORRIDOR_ID,TEST_ID) "
                     "VALUES (?,?)")
            data = [[corridor[0], testID]
                    for corridor in corridorData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, data)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_CORRIDOR: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertCorridorStationsData(self, corridorData, testID):
        """
        Inserta los datos de las estaciones del corredor en la tabla
        CORRIDOR_STATIONS
        :param corridorData: Datos del corredor
        :return:
        """
        self.initCursor()
        try:
            # query = ("INSERT OR IGNORE INTO CORRIDOR_STATIONS (CORRIDOR,
            # STATIONS) "
            #            "VALUES ({corridor},json(\"{stations}\")) ")
            # for line in corridorData[2]:
            #    queryFormated = query.format(corridor = corridorData[0],
            #    stations = str(line))
            #    self.cursor.execute(queryFormated)
            query = (
                "INSERT OR IGNORE INTO CORRIDOR_STATIONS (TEST_ID,CORRIDOR,"
                "STATIONS) "
                "VALUES (?,?,?) ")
            inputData = [[testID, corridor[0], json.dumps(line)]
                         for corridor in corridorData
                         for line in corridor[2]]
            # lines = [[line] for corridor in corridorData for line in
            # corridor[2]]
            # for n,line in enumerate(lines):
            #     print(f"Ramal {n}: {line}")
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error CORRIDOR_STATIONS: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertTimeSlotData(self, timeSlotData):
        """
        Inserta los datos de los slots de tiempo en la tabla TIME_SLOT
        :param timeSlotData: Datos de los slots de tiempo
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO TIME_SLOT (ID,START,END) VALUES ("
                     "?,?,?)")
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, timeSlotData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error TIME_SLOT: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxTimeSlotData(self, timeSlotData, testID):
        """
        Inserta los datos auxiliares de los slots de tiempo en la tabla
        AUX_TIME_SLOT
        :param timeSlotData: Datos de los slots de tiempo
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_TIME_SLOT (TIME_SLOT_ID,"
                     "TEST_ID) VALUES (?,?)")
            inputData = [[timeSlot[0], testID]
                         for timeSlot in timeSlotData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_TIME_SLOT: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertStationsData(self, stationsData):
        """
        Inserta los datos de las estaciones en la tabla STATIONS
        :param stationsData: Datos de las estaciones
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO STATIONS (ID,NAME,CITY,SHORT_NAME,"
                     "COORDINATES) VALUES (?,?,?,?,json(?))")
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, stationsData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error STATIONS: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxStationsData(self, stationsData, testID):
        """
        Inserta los datos auxiliares de las estaciones en la tabla AUX_STATIONS
        :param stationsData: Datos de las estaciones
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_STATIONS (STATIONS_ID,TEST_ID) "
                     "VALUES (?,?)")
            inputData = [[stations[0], testID]
                         for stations in stationsData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_STATIONS: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertTestsData(self, testName, observations=""):
        """
        Inserta los datos del test en la tabla TESTS.
        :param testName: Nombre del test actual.
        :param observations: Observaciones sobre el test actual.
        :return:
        """
        self.initCursor()
        try:
            query = f"INSERT OR IGNORE INTO TESTS (NAME) VALUES ('{
            testName}') RETURNING ID"
            self.cursor.execute(query)
            id = self.cursor.fetchone()
            query = (f"UPDATE TESTS SET OBSERVATIONS = '{observations}' WHERE "
                     f"TESTS.NAME = '{testName}'")
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()
        return id

    def insertRollingStockData(self, rollingStockData):
        """
        Inserta los datos del stock rodante en la tabla ROLLING_STOCK
        :param rollingStockData: Datos del stock rodante
        :return:
        """
        self.initCursor()
        id = []
        try:
            query = ("INSERT OR IGNORE INTO ROLLING_STOCK (ID_ON_FILE,NAME,"
                     "SEATS) VALUES (?,?,json(?)) RETURNING ID")
            self.cursor.execute("BEGIN TRANSACTION")
            for data in rollingStockData:
                self.cursor.execute(query, data)
                result = self.cursor.fetchone()
                if result: id.append(result)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error ROLLING_STOCK: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()
        return id

    def insertAuxRollingStockData(self, rollingStockData, testID):
        """
        Inserta los datos auxiliares del stock rodante en la tabla
        AUX_ROLLING_STOCK
        :param rollingStockData: Datos del stock rodante
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_ROLLING_STOCK ("
                     "ROLLING_STOCK_ID,TEST_ID) VALUES (?,?)")
            inputData = [[rollingStock[0], testID]
                         for rollingStock in rollingStockData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_ROLLING_STOCK: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertSeatData(self, seatData):
        """
        Inserta los datos de los asientos en la tabla SEAT
        :param seatData: Datos de los asientos
        :return:
        """
        self.initCursor()
        id = []
        try:
            query = ("INSERT OR IGNORE INTO SEAT (ID_ON_FILE,NAME,HARD_TYPE,"
                     "SOFT_TYPE) VALUES (?,?,?,?) RETURNING ID")
            self.cursor.execute("BEGIN TRANSACTION")
            for data in seatData:
                self.cursor.execute(query, data)
                result = self.cursor.fetchone()
                if result: id.append(result)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error SEAT: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()
        return id

    def insertAuxSeatData(self, seatData, testID):
        """
        Inserta los datos auxiliares de los asientos en la tabla AUX_SEAT
        :param seatData: Datos de los asientos
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_SEAT (SEAT_ID,TEST_ID) VALUES "
                     "(?,?)")
            inputData = [[seat[0], testID]
                         for seat in seatData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_SEAT: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertTrainServiceProviderData(self, TspData):
        """
        Inserta los datos de los proveedores de servicios ferroviarios en la
        tabla TRAIN_SERVICE_PROVIDERS
        :param TspData: Datos de los proveedores de servicios ferroviarios
        :return:
        """
        self.initCursor()
        id = []
        try:
            query = (
                "INSERT OR IGNORE INTO TRAIN_SERVICE_PROVIDER (ID_ON_FILE,"
                "NAME,ROLLING_STOCK) VALUES (?,?,"
                "json(?)) RETURNING ID")
            self.cursor.execute("BEGIN TRANSACTION")
            for data in TspData:
                self.cursor.execute(query, data)
                result = self.cursor.fetchone()
                if result: id.append(result)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error TRAIN_SERVICE_PROVIDER: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()
        return id

    def insertAuxTrainServiceProviderData(self, TspData, testID):
        """
        Inserta los datos auxiliares del proveedor de servicios feroviarios
        en la tabla AUX_CORRIDOR
        :param TspData: Datos del proveedor de servicios ferroviarios
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_TRAIN_SERVICE_PROVIDER ("
                     "TRAIN_SERVICE_PROVIDER_ID,TEST_ID) VALUES (?,?)")
            inputData = [[tsp[0], testID]
                         for tsp in TspData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error AUX_TRAIN_SERVICE_PROVIDER: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertLineData(self, lineData):
        """
        Inserta los datos de las líneas en la tabla LINE
        :param lineData: Datos del las líneas
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO LINE (ID,NAME,CORRIDOR) VALUES (?,"
                     "?,?)")
            inputData = [line[:3]
                         for line in lineData]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error LINE: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertStopsData(self, lineData, testID):
        """
        Inserta los datos de las paradas de cada una de las líneas en la
        tabla STOPS
        :param lineData: Datos de las líneas
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO STOPS (TEST_ID,LINE_ID,STATION,"
                "ARRIVAL_TIME,DEPARTURE_TIME) VALUES (?,?,?,"
                "?,?)")
            inputData = [[testID, line[0]] + stop
                         for line in lineData
                         for stop in line[3]]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error STOPS: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertServiceData(self, serviceData):
        """
        Inserta los datos de los servicios en la tabla SERVICE
        :param serviceData: Datos de los servicios
        :return:
        """
        self.initCursor()
        try:
            inputData = [service[:6]
                         for service in serviceData]
            query = (
                "INSERT OR IGNORE INTO SERVICE (ID,DATE,LINE,"
                "TRAIN_SERVICE_PROVIDER,TIME_SLOT,ROLLING_STOCK) "
                "VALUES (?,?,?,?,?,?)")
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Service Sqlite Error SERVICE: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print("Service Error: " + str(e))
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print("Service Sqlite programming Error: " + str(e))
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxServiceData(self, serviceData, testID):
        """
        Inserta los datos auxiliares de los servicios en la tabla AUX_SERVICE
        :param serviceData: Datos del corredor
        :param testID: ID del test del que se están almacenando los datos
        :return:
        """
        self.initCursor()
        try:
            inputData = [[service[0], testID]
                         for service in serviceData]
            query = ("INSERT OR IGNORE INTO AUX_SERVICE (SERVICE_ID,TEST_ID) "
                     "VALUES (?,?)")
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Aux Service Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print("Aux Service Error: " + str(e))
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print("Aux Service Sqlite P. Error: " + str(e))
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertOdtData(self, serviceData, testID):
        """
        Inserta los datos de las tuplas de origen y destino en la tabla
        ORIGIN_DESTINATION_TUPLES
        :param serviceData: Datos de los servicios
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO ORIGIN_DESTINATION_TUPLES (ID,TEST_ID,"
                "SERVICE_ID,ORIGIN,DESTINATION,"
                "SEATS) VALUES (?,?,?,?,?,?)")
            inputData = [[f"{testID}-{service[0]}-{odt[0]}-{odt[1]}",
                          testID,
                          service[0],
                          odt[0],
                          odt[1],
                          json.dumps(str(list(odt[2].keys())))]
                         for service in serviceData
                         for odt in service[6]]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("ODT Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print("ODT Error: " + str(e))
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print("ODT Sqlite P. Error: " + str(e))
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertRestrictionsData(self, serviceData):
        """
        Inserta los datos de las restricciones en la tabla RESTRICTIONS
        :param serviceData: Datos de los servicios
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO RESTRICTIONS (SERVICE_ID,TYPE,"
                     "RESTRICTION) VALUES (?,?,?)")
            inputData = [[service[0],
                          list(restriction.keys())[0],
                          json.dumps(restriction[list(restriction.keys())[0]])]
                         for service in serviceData
                         for restriction in service[7:]]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Restrictions Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print("Restrictions  Error: " + str(e))
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print("Restrictions Sqlite P. Error: " + str(e))
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertSeatsPriceData(self, serviceData, testID):
        """
        Inserta los datos del precio de los asientos por trayecto en la tabla
        SEATS_PRICE
        :param serviceData: Datos de los servicios
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO SEATS_PRICE (ODT_ID,SEAT,PRICE) "
                     "VALUES (?,?,?)")
            inputData = [[f"{testID}-{service[0]}-{odt[0]}-{odt[1]}",
                          key,
                          odt[2].get(key)]
                         for service in serviceData
                         for odt in service[6]
                         for key in list(odt[2].keys())]
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Seats Price Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print("Seats Price Error: " + str(e))
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print("Seats Price Sqlite P. Error: " + str(e))
            self.conector.rollback()
        finally:
            self.cursor.close()

    # Funciones para eliminar un test y lo que cuelgue de este
    def deleteTestEntryOld(self):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
        con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            names, testNames = self.selectTestName()
            if names == "" or testNames == []: raise EmptyTestData
            print(names)
            test = int(
                input("Introduce el numero del test que quieras borrar: ")) - 1
            query = f"""DELETE FROM TESTS
                        WHERE TESTS.NAME = '{testNames[test]}'"""
            self.cursor.execute(query)
            self.conector.commit()

            self.deleteUnusedSeatData()
            self.deleteUnusedServiceData()
            self.deleteUnusedCorridorData()
            self.deleteUnusedStationsData()
            self.deleteUnusedTrainServiceProviderData()
            self.deleteUnusedTimeSlotData()
            self.deleteUnusedRollingStockData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except EmptyTestData as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def deleteTestEntry(self, testList):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
        con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            for testName in testList:
                query = f"""DELETE FROM TESTS WHERE TESTS.NAME = '{testName}'"""
                self.cursor.execute(query)

            self.conector.commit()

            self.deleteUnusedSeatData()
            self.deleteUnusedServiceData()
            self.deleteUnusedCorridorData()
            self.deleteUnusedStationsData()
            self.deleteUnusedTrainServiceProviderData()
            self.deleteUnusedTimeSlotData()
            self.deleteUnusedRollingStockData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except EmptyTestData as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def deleteUnusedCorridorData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla CORRIDOR
        :return:
        """
        try:
            query = f"""DELETE FROM CORRIDOR
                        WHERE CORRIDOR.ID NOT IN (
                        SELECT AUX_CORRIDOR.CORRIDOR_ID FROM AUX_CORRIDOR)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedTimeSlotData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla TIME_SLOT
        :return:
        """
        try:
            query = f"""DELETE FROM TIME_SLOT
                        WHERE TIME_SLOT.ID NOT IN (
                        SELECT AUX_TIME_SLOT.TIME_SLOT_ID FROM AUX_TIME_SLOT)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedSeatData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla SEAT
        :return:
        """
        try:
            query = f"""DELETE FROM SEAT
                        WHERE SEAT.ID NOT IN (
                        SELECT AUX_SEAT.SEAT_ID FROM AUX_SEAT)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedRollingStockData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla ROLLING_STOCK
        :return:
        """
        try:
            query = f"""DELETE FROM ROLLING_STOCK
                        WHERE ROLLING_STOCK.ID NOT IN (
                        SELECT AUX_ROLLING_STOCK.ROLLING_STOCK_ID FROM 
                        AUX_ROLLING_STOCK)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedServiceData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla SERVICE
        :return:
        """
        try:
            query = f"""DELETE FROM SERVICE
                        WHERE SERVICE.ID NOT IN (
                        SELECT AUX_SERVICE.SERVICE_ID FROM AUX_SERVICE)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedStationsData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla STATIONS
        :return:
        """
        try:
            query = f"""DELETE FROM STATIONS
                        WHERE STATIONS.ID NOT IN (
                        SELECT AUX_STATIONS.STATIONS_ID FROM AUX_STATIONS)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def deleteUnusedTrainServiceProviderData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla TRAIN_SERVICE_PROVIDER
        :return:
        """
        try:
            query = f"""DELETE FROM TRAIN_SERVICE_PROVIDER
                        WHERE TRAIN_SERVICE_PROVIDER.ID NOT IN (
                        SELECT 
                        AUX_TRAIN_SERVICE_PROVIDER.TRAIN_SERVICE_PROVIDER_ID 
                        FROM AUX_TRAIN_SERVICE_PROVIDER)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    # Funciones para seleccionar los datos de la base datos para volcarlos en
    # el yaml
    # Funciones auxiliares
    def selectTestName(self):
        """
        Extrae el nombre de los tests que actualmente se encuentran en la
        base de datos
        :return: names, testNames
        """
        names = ""
        testNames = []
        try:
            query = """SELECT TESTS.NAME
                       FROM TESTS"""
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            for key, name in enumerate(data):
                testNames.append(name[0])
                names = names + f"{key + 1}.{name[0]}\n"
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            return names, testNames

    def formatStopsForLine(self, lineID, testName):
        """
        Extrae los datos de la tabla STOPS y los reordena para posteriormente
        agregarlos al archivo yaml de la oferta
        bajo la propiedad line
        :param lineID: ID de la línea de la que se van a extraer las estaciones
        :return: [{"station":<stationID_0>,"arrival_time":<arrivalTime_0>,
        "departure_time":<departureTime_0>},...,
                  {"station":<stationID_n>,"arrival_time":<arrivalTime_n>,
                  "departure_time":<departureTime_n>}]
        """
        try:
            query = f"""SELECT
                            STOPS.STATION,
                            STOPS.ARRIVAL_TIME,
                            STOPS.DEPARTURE_TIME
                        FROM 
                            STOPS
                        WHERE STOPS.LINE_ID = '{lineID}'
                        AND STOPS.TEST_ID = (SELECT TESTS.ID FROM TESTS WHERE 
                        TESTS.NAME = '{testName}')
                        ORDER BY STOPS.ARRIVAL_TIME ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = []
            for element in data:
                formatedData.append({"station": element[0],
                                     "arrival_time": element[1],
                                     "departure_time": element[2]})
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    @staticmethod
    def formatSeatsForRollingStock(seatsData):
        """
        Extrae los datos de los asientos que tienen los diferentes trenes
        dentro de la tabla ROLLING_STOCK y los
        organiza para después introducirlos en el apartado seats dentro de la
        propiedad rollingStock del archivo
        yaml de la oferta
        :param seatsData: Datos de los asientos
        :return: [{"hard_type":<hardType_0>,"quantity":<quantity_0>},...,
                  {"hard_type":<hardType_n>,"quantity":<quantity_n>}]
        """
        formatedData = []
        try:
            for k, e in zip(seatsData.keys(), seatsData.values()):
                formatedData.append({"hard_type": int(k), "quantity": int(e)})
            return formatedData
        except Exception as e:
            print(e)

    def formatOdtForService(self, serviceID, testName):
        """
        Extrae los datos de la tabla ORIGIN_DESTINATION_TUPLES y los reordena
        para introducirlos posteriormente
        en el apartado origin_destination_tuples de la propiedad service
        dentro del archivo de oferta
        :param serviceID: ID del servicio del que se están obteniendo los datos
        :return: [{"origin":<origin_0>,"destination":>destination_0>,
                    "seats":[{"seat":<seat_0>,"price":<price_0>},...,
                    {"seat":<seat_n>,"price":<price_n>}]},...,
                    {"origin":<origin_n>,"destination":>destination_n>,
                    "seats":[{"seat":<seat_0>,"price":<price_0>},...,
                    {"seat":<seat_n>,"price":<price_n>}]}]
        """

        try:
            query = f"""SELECT
                            ORIGIN_DESTINATION_TUPLES.ORIGIN,
                            ORIGIN_DESTINATION_TUPLES.DESTINATION,
                            ORIGIN_DESTINATION_TUPLES.ID
                        FROM
                            ORIGIN_DESTINATION_TUPLES
                        WHERE ORIGIN_DESTINATION_TUPLES.SERVICE_ID = '
{serviceID}'
                        AND ORIGIN_DESTINATION_TUPLES.TEST_ID = (SELECT 
                        TESTS.ID FROM TESTS WHERE TESTS.NAME = '{
            testName}')
                        ORDER BY ORIGIN_DESTINATION_TUPLES.ORIGIN ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"origin": element[0], "destination": element[1],
                             "seats": self.formatSeatsPriceForOdt(element[2])}
                            for element in data]
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def formatSeatsPriceForOdt(self, odtID):
        """
        Extrae los datos del precio de los asientos para cada una de las
        tuplas de origen-destino de la tabla
        SEATS_PRICE y las ordena
        :param odtID: ID de la tupla de origen-destino de la que se quieren
        conocer los precios de los asientos
        :return: [{"seat":<seat_0>,"price":<price_0>},...,{"seat":<seat_n>,
        "price":<price_n>}]
        """
        try:
            query = f"""SELECT
                            SEATS_PRICE.SEAT,
                            SEATS_PRICE.PRICE
                            
                        FROM 
                            SEATS_PRICE
                        WHERE SEATS_PRICE.ODT_ID = '{odtID}'
                        ORDER BY SEATS_PRICE.SEAT ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"seat": element[0], "price": element[1]} for
                            element in data]
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def formatCapacityConstraints(self, serviceID):
        """
        Extrae los datos de la tabla RESTRICTIONS correspondientes a la
        restriccion \"capacity_constraints\"
        :param serviceID: ID del servicio asociado a esa restriccion
        :return: data
        """
        try:
            query = f"""SELECT 
                            RESTRICTIONS.RESTRICTION
                        FROM 
                            RESTRICTIONS
                        WHERE RESTRICTIONS.TYPE = 'capacity_constraints' 
                        AND RESTRICTIONS.SERVICE_ID = '{serviceID}'"""

            self.cursor.execute(query)
            data = json.loads(self.cursor.fetchall()[0][0])
            # if data is None: data = str(data).replace("None","null")
            return data
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def formatCorridorStationsForCorridor(self, corridorID, testName):
        """
        Extrae los datos de la tabla CORRIDOR_STATIONS y los formatea para
        introducirlos a stations dentro de
        corridor
        :param corridorID:
        :return:
        """
        try:
            query = f"""SELECT
                            CORRIDOR_STATIONS.STATIONS
                        FROM
                            CORRIDOR_STATIONS
                        WHERE CORRIDOR_STATIONS.CORRIDOR = '{corridorID}'
                        AND CORRIDOR_STATIONS.TEST_ID = (SELECT TESTS.ID FROM 
                        TESTS WHERE TESTS.NAME = '{testName}')"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatData = [json.loads(element[0]) for element in data]
            return self.buildCorridorStationsFromLines(formatData)
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def buildCorridorStationsFromLines(self, lines):
        """
        Reconstruye la estructura original del corredor a partir de las
        diferentes líneas almacenadas en la
        tabla CORRIDOR_STATIONS
        :param lines: Líneas que forman el corredor
        :return:
        """
        if not lines or not all(
                isinstance(line, list) and len(line) > 1 for line in
                lines):  # si no hay mínimo 2 estaciones no continua
            raise ValueError(
                "No hay suficientes estaciones en alguno de los caminos")

        def buildSubLines(subLines):
            """
            Funcion interna que se encarga de reconstruir la estructura del
            corredor
            :param subLines:
            :return:
            """
            corridorStations = {}
            for line in subLines:
                org = line.pop(
                    0)  # extraemos el primer elemento de la lista line
                if org not in corridorStations:  # Si este elemento no se
                    # encuentra en la variable corridorStations,
                    # añade una lista vacia con org como key al diccionario
                    corridorStations[org] = []
                if line:  # Si line no está vacia, añade al diccionario toda
                    # la variable line a la key org
                    corridorStations[org].append(line)

            outputData = []

            # reconstruimos la estructura empleando para ello el diccionario
            # creado anteriormente
            for org, sub in corridorStations.items():  # recorremos el
                # diccionario extrayendo los pares (key, value)
                if sub:  # Si el diccionario contiene algún value,
                    # introducimos como origen la key y como destino
                    # volvemos a llamar a la función buildSubLines
                    outputData.append({"org": org, "des": buildSubLines(sub)})
                else:  # Si el diccionario no contiene valores en la clave
                    # org, introducimos como origen la clave org
                    # y el destino como una lista vacia qe índica el final
                    # del ramal
                    outputData.append({"org": org, "des": []})

            return outputData

        return buildSubLines(lines)

    # Funciones principales
    def getDataForDumpYamlOld(self):
        """
        (Deprecated)Genera la estructra necesaria para reconstruir el archivo
        de oferta mediante subfunciones para cada
        uno de los apartados dentro del archivo yaml.
        :return: testName, data
        """
        data = {}
        testName = ""
        try:
            self.initCursor()
            names, testNames = self.selectTestName()
            print(names)
            testName = testNames[
                int(input(
                    "Introduce el numero del test que quieres extraer de la "
                    "base de datos: ")) - 1]

            data.update(self.getDataForStations(testName))
            data.update(self.getDataForSeat(testName))
            data.update(self.getDataForCorridor(testName))
            data.update(self.getDataForLine(testName))
            data.update(self.getDataForRollingStock(testName))
            data.update(self.getDataForTrainServiceProvider(testName))
            data.update(self.getDataForTimeSlot(testName))
            data.update(self.getDataForService(testName))

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
            return testName, data

    def getDataForDumpYaml(self, testName):
        """
        Genera la estructra necesaria para reconstruir el archivo de oferta
        mediante subfunciones para cada
        uno de los apartados dentro del archivo yaml.
        :return: testName, data
        """
        data = {}
        try:
            self.initCursor()

            data.update(self.getDataForStations(testName))
            data.update(self.getDataForSeat(testName))
            data.update(self.getDataForCorridor(testName))
            data.update(self.getDataForLine(testName))
            data.update(self.getDataForRollingStock(testName))
            data.update(self.getDataForTrainServiceProvider(testName))
            data.update(self.getDataForTimeSlot(testName))
            data.update(self.getDataForService(testName))

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
            return data

    def getDataForStations(self, testName):
        """
        Obtiene los datos de las estaciones y los formatea para que sigan la
        estructra de stations dentro del archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            STATIONS.ID,
                            STATIONS.NAME,
                            STATIONS.CITY,
                            STATIONS.SHORT_NAME,
                            STATIONS.COORDINATES
                            
                        FROM 
                            STATIONS
                        WHERE STATIONS.ID IN (SELECT AUX_STATIONS.STATIONS_ID 
                        FROM AUX_STATIONS
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_STATIONS.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY STATIONS.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": element[0], "name": element[1], "city": element[2],
                 "short_name": element[3],
                 "coordinates": json.loads(element[4])} for element in data]
            outputData = {"stations": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForTimeSlot(self, testName):
        """
        Obtiene los datos de los slots de tiempo y los formatea para que
        sigan la estructra de timeSlot dentro del
        archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            TIME_SLOT.ID,
                            TIME_SLOT.START,
                            TIME_SLOT.END                            
                        FROM 
                            TIME_SLOT
                        WHERE TIME_SLOT.ID IN (SELECT 
                        AUX_TIME_SLOT.TIME_SLOT_ID FROM AUX_TIME_SLOT
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_TIME_SLOT.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY TIME_SLOT.START ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": element[0], "start": element[1], "end": element[2]}
                for element in data]
            outputData = {"timeSlot": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForLine(self, testName):
        """
        Obtiene los datos de las líneas y los formatea para que sigan la
        estructra de line dentro del archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            LINE.ID,
                            LINE.NAME,
                            LINE.CORRIDOR
                        FROM 
                            LINE
                        WHERE LINE.ID IN (SELECT SERVICE.LINE FROM SERVICE
                                          INNER JOIN TESTS,AUX_SERVICE ON 
                                          TESTS.ID = AUX_SERVICE.TEST_ID
                                          AND AUX_SERVICE.SERVICE_ID = 
                                          SERVICE.ID
                                          WHERE TESTS.NAME = '{testName}')
                        ORDER BY LINE.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": element[0], "name": element[1], "corridor": element[2],
                 "stops": self.formatStopsForLine(element[0], testName)} for
                element in data]
            outputData = {"line": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForSeat(self, testName):
        """
        Obtiene los datos de los asientos y los formatea para que sigan la
        estructra de seat dentro del archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            SEAT.ID_ON_FILE,
                            SEAT.NAME,
                            SEAT.HARD_TYPE,
                            SEAT.SOFT_TYPE
                        FROM 
                            SEAT
                        WHERE SEAT.ID IN (SELECT AUX_SEAT.SEAT_ID FROM AUX_SEAT
                                          INNER JOIN TESTS ON TESTS.ID = 
                                          AUX_SEAT.TEST_ID
                                          WHERE TESTS.NAME = '{testName}')
                        ORDER BY SEAT.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": element[0], "name": element[1],
                             "hard_type": int(element[2]),
                             "soft_type": int(element[3])} for element in data]
            outputData = {"seat": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForCorridor(self, testName):
        """
        Obtiene los datos de los corredores y los formatea para que sigan la
        estructra de corridor dentro del archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            CORRIDOR.ID,
                            CORRIDOR.NAME
                        FROM
                            CORRIDOR
                        WHERE CORRIDOR.ID IN (SELECT AUX_CORRIDOR.CORRIDOR_ID
                                              FROM AUX_CORRIDOR
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_CORRIDOR.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY CORRIDOR.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": element[0], "name": element[1], "stations":
                self.formatCorridorStationsForCorridor(element[0], testName)}
                            for element in data]
            outputData = {"corridor": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForRollingStock(self, testName):
        """
        Obtiene los datos del stock rodante y los formatea para que sigan la
        estructra de rollingStock dentro del
        archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            ROLLING_STOCK.ID_ON_FILE,
                            ROLLING_STOCK.NAME,
                            ROLLING_STOCK.SEATS
                        FROM 
                            ROLLING_STOCK
                        WHERE ROLLING_STOCK.ID IN (SELECT 
                        AUX_ROLLING_STOCK.ROLLING_STOCK_ID
                                                   FROM AUX_ROLLING_STOCK
                                                   INNER JOIN TESTS ON 
                                                   TESTS.ID = 
                                                   AUX_ROLLING_STOCK.TEST_ID
                                                   WHERE TESTS.NAME = '
{testName}')
                        ORDER BY ROLLING_STOCK.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": element[0], "name": element[1],
                 "seats": self.formatSeatsForRollingStock(
                     json.loads(element[2]))}
                for element in data]
            outputData = {"rollingStock": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForTrainServiceProvider(self, testName):
        """
        Obtiene los datos de los proveedores de servicios ferroviarios y los
        formatea para que sigan la estructra de
        trainServiceProvider dentro del archivo yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            TRAIN_SERVICE_PROVIDER.ID_ON_FILE,
                            TRAIN_SERVICE_PROVIDER.NAME,
                            TRAIN_SERVICE_PROVIDER.ROLLING_STOCK
                        FROM 
                            TRAIN_SERVICE_PROVIDER
                        WHERE TRAIN_SERVICE_PROVIDER.ID IN (SELECT 
                        AUX_TRAIN_SERVICE_PROVIDER.TRAIN_SERVICE_PROVIDER_ID 
                        FROM AUX_TRAIN_SERVICE_PROVIDER
                                                            INNER JOIN TESTS 
                                                            ON TESTS.ID = 
                                                            AUX_TRAIN_SERVICE_PROVIDER.TEST_ID
                                                            WHERE TESTS.NAME 
                                                            = '{testName}')
                        ORDER BY TRAIN_SERVICE_PROVIDER.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": element[0], "name": element[1],
                             "rolling_stock": json.loads(element[2])}
                            for element in data]
            outputData = {"trainServiceProvider": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForService(self, testName):
        """
        Obtiene los datos de los servicios y los formatea para que sigan la
        estructra de service dentro del archivo
        yaml de la oferta
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT
                            SERVICE.ID,
                            SERVICE.DATE,
                            SERVICE.LINE,
                            SERVICE.TRAIN_SERVICE_PROVIDER,
                            SERVICE.TIME_SLOT,
                            SERVICE.ROLLING_STOCK
                        FROM
                            SERVICE
                        WHERE SERVICE.ID IN (SELECT AUX_SERVICE.SERVICE_ID
                                             FROM AUX_SERVICE
                                             INNER JOIN TESTS ON TESTS.ID = 
                                             AUX_SERVICE.TEST_ID
                                             WHERE TESTS.NAME = '{testName}')
                        ORDER BY SERVICE.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": element[0], "date": element[1], "line": element[2],
                 "train_service_provider": element[3],
                 "time_slot": element[4], "rolling_stock": element[5],
                 "origin_destination_tuples": self.formatOdtForService(
                     element[0], testName),
                 "capacity_constraints": self.formatCapacityConstraints(
                     element[0])} for element in data]
            outputData = {"service": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

        try:
            query = f"""SELECT
                            TRAIN_SERVICE_PROVIDER.ID,
                            TRAIN_SERVICE_PROVIDER.NAME,
                            TRAIN_SERVICE_PROVIDER.ROLLING_STOCK
                        FROM 
                            TRAIN_SERVICE_PROVIDER
                        WHERE TRAIN_SERVICE_PROVIDER.ID IN (SELECT 
                        AUX_TRAIN_SERVICE_PROVIDER.TRAIN_SERVICE_PROVIDER_ID 
                        FROM AUX_TRAIN_SERVICE_PROVIDER
                                                            INNER JOIN TESTS 
                                                            ON TESTS.ID = 
                                                            AUX_TRAIN_SERVICE_PROVIDER.TEST_ID
                                                            WHERE TESTS.NAME 
                                                            = '{testName}')
                        ORDER BY TRAIN_SERVICE_PROVIDER.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": element[0], "name": element[1],
                             "rolling_stock": json.loads(element[2])}
                            for element in data]
            outputData = {"trainServiceProvider": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)


class SqlDemand:
    """
        Módulo que se encarga de gestionar la entrada y salida de datos de la
        base de datos de la demanda
        :param db: Direccion de la base de datos de la oferta, por defecto será:
        <currentWorkingDirectory>/Database/demandDb.db
    """

    # Inicializacion del objeto SqlDemand, encargado de manejar las
    # interacciones con la base de datos de la oferta
    def __init__(self, db=None):
        self.workingDirectory = os.getcwd()  # Directorio de trabajo
        self.defaultDatabaseFolder = self.workingDirectory + "/Database"  #
        # Directorio para las bases de datos
        Path(self.defaultDatabaseFolder).mkdir(parents=True,
                                               exist_ok=True)  # Generamos la
        # carpeta Database en caso de no existir
        self.defaultDemandPath = self.defaultDatabaseFolder + "/demandDb.db"
        # Direccion de la base de datos por
        # defecto
        self.conector = sqlite3.connect(
            db if db is not None  # Creamos la conexion con la base de datos
            # de la oferta
            else self.defaultDemandPath)  # Si la base de datos no existe,
        # se generara
        # automaticamente
        self.cursor = self.conector.cursor()  # Creamos el cursor para la
        # base de datos
        self.enableForeignKeys()  # Habilitamos el uso de las claves foraneas
        # en la base de datos

        self.generateDatabaseTables()  # Generamos las tablas de la base de
        # datos si estas no existen

    def enableForeignKeys(self):
        self.cursor.execute(
            "PRAGMA foreign_keys = ON")  # Habilita las claves foraneas
        # usando los PRAGMA de sqlite3
        self.conector.commit()

    def initCursor(self):
        """
        Inicializa el cursor de la base de datos, en caso de que se haya
        cerrado anteriormente.
        :return:
        """
        self.cursor = self.conector.cursor()

    def executeSelectTestsIDQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            data = self.cursor.fetchone()[0]
            return data
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
        return -1

    def executeQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            self.conector.commit()

            if query.strip().upper().startswith("SELECT"):
                cols = [item[0] for item in self.cursor.description]
                result = self.cursor.fetchall()
                return cols, result

        except sqlite3.Error as e:
            print(e)
            return -1
        except Exception as e:
            print(e)
            return -1
        except sqlite3.ProgrammingError as e:
            print(e)
            return -1
        finally:
            self.cursor.close()

    def generateDatabaseTables(self):
        """
        Genera las tablas de la base de datos, si estas no existieran
        previamente
        :return:
        """
        self.createTestsTable()
        self.createMarketTable()
        self.createUserPatternTable()
        self.createDemandPatternTable()
        self.createUserPatternDistributionTable()
        self.createMarketsTable()
        self.createVariableTable()
        self.createDayTable()
        self.createAuxUserPatternTable()
        self.createAuxMarketTable()
        self.createAuxDemandPatternTable()
        self.createAuxDayTable()

    # Funciones para la creacion de las tablas de la base de datos
    def createTestsTable(self):
        """
        Genera la tabla TESTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS TESTS (
                            ID           INTEGER PRIMARY KEY AUTOINCREMENT
                                                 UNIQUE
                                                 NOT NULL,
                            NAME         TEXT    UNIQUE
                                                 NOT NULL,
                            OBSERVATIONS TEXT
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createMarketTable(self):
        """
        Genera la tabla MARKET en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS MARKET (
                            ID                       TEXT PRIMARY KEY
                                                          UNIQUE,
                            DEPARTURE_STATION        TEXT,
                            DEPARTURE_STATION_COORDS JSON,
                            ARRIVAL_STATION          TEXT,
                            ARRIVAL_STATION_COORDS   JSON,
                            UNIQUE(ID, DEPARTURE_STATION,ARRIVAL_STATION)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createUserPatternTable(self):
        """
        Genera la tabla USER_PATTERN en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS USER_PATTERN (
                            ID                        TEXT    PRIMARY KEY
                                                              UNIQUE,
                            NAME                      TEXT,
                            RULES                     JSON,
                            ARRIVAL_TIME              TEXT,
                            ARRIVAL_TIME_KWARGS       JSON,
                            PURCHASE_DAY              TEXT,
                            PURCHASE_DAY_KWARGS       JSON,
                            FORBIDDEN_DEPARTURE_HOURS JSON,
                            SEATS                     JSON,
                            TRAIN_SERVICE_PROVIDERS   JSON,
                            EARLY_STOP                REAL,
                            UTILITY_THRESHOLD         INTEGER,
                            ERROR                     TEXT,
                            ERROR_KWARGS              JSON,
                            UNIQUE(ID,NAME,ARRIVAL_TIME,PURCHASE_DAY,
                            EARLY_STOP,UTILITY_THRESHOLD,ERROR)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createDemandPatternTable(self):
        """
        Genera la tabla DEMAND_PATTERN en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS DEMAND_PATTERN (
                            ID   TEXT PRIMARY KEY
                                      UNIQUE,
                            NAME TEXT,
                            UNIQUE(ID,NAME)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createMarketsTable(self):
        """
        Genera la tabla MARKETS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS MARKETS (
                            DEMAND_PATTERN_ID       TEXT REFERENCES 
                            DEMAND_PATTERN (ID) ON DELETE CASCADE
                                                                                        ON UPDATE CASCADE,
                            MARKET                  TEXT REFERENCES MARKET (
                            ID) ON DELETE CASCADE
                                                                                ON UPDATE CASCADE,
                            POTENTIAL_DEMAND        TEXT,
                            POTENTIAL_DEMAND_KWARGS JSON,
                            UNIQUE(DEMAND_PATTERN_ID,MARKET,POTENTIAL_DEMAND)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createUserPatternDistributionTable(self):
        """
        Genera la tabla USER_PATTERN_DISTRIBUTION en la base de datos,
        si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS USER_PATTERN_DISTRIBUTION (
                            MARKET_ID         TEXT REFERENCES MARKET (ID) ON 
                            DELETE CASCADE
                                                                          ON 
                                                                          UPDATE CASCADE,
                            DEMAND_PATTERN_ID TEXT REFERENCES DEMAND_PATTERN 
                            (ID) ON DELETE CASCADE
                                                                                  ON UPDATE CASCADE,
                            USER_PATTERN_ID   TEXT REFERENCES USER_PATTERN (
                            ID) ON DELETE CASCADE
                                                                                ON UPDATE CASCADE,
                            PERCENTAGE        REAL,
                            UNIQUE(MARKET_ID,DEMAND_PATTERN_ID,
                            USER_PATTERN_ID,PERCENTAGE)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createVariableTable(self):
        """
        Genera la tabla VARIABLE en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS VARIABLE (
                            USER_PATTERN_ID TEXT REFERENCES USER_PATTERN (ID) 
                            ON DELETE CASCADE
                                                                              ON UPDATE CASCADE,
                            NAME            TEXT,
                            TYPE            TEXT,
                            SUPPORT         JSON,
                            SETS            JSON,
                            LABELS          JSON,
                            UNIQUE(USER_PATTERN_ID,NAME,TYPE)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxMarketTable(self):
        """
        Genera la tabla AUX_MARKET en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_MARKET (
                            ID        INTEGER PRIMARY KEY AUTOINCREMENT
                                              NOT NULL
                                              UNIQUE,
                            MARKET_ID TEXT    REFERENCES MARKET (ID) ON 
                            DELETE CASCADE
                                                                     ON 
                                                                     UPDATE 
                                                                     CASCADE,
                            TEST_ID   INTEGER REFERENCES TESTS (ID) ON DELETE 
                            CASCADE
                                                                    ON UPDATE 
                                                                    CASCADE,
                            UNIQUE(MARKET_ID,TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxDemandPatternTable(self):
        """
        Genera la tabla AUX_DEMAND_PATTERN en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_DEMAND_PATTERN (
                            ID                INTEGER PRIMARY KEY AUTOINCREMENT
                                                      UNIQUE
                                                      NOT NULL,
                            DEMAND_PATTERN_ID TEXT    REFERENCES 
                            DEMAND_PATTERN (ID) ON DELETE CASCADE
                                                                                     ON UPDATE CASCADE,
                            TEST_ID           INTEGER REFERENCES TESTS (ID) 
                            ON DELETE CASCADE
                                                                            ON UPDATE CASCADE,
                            UNIQUE(DEMAND_PATTERN_ID,TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxUserPatternTable(self):
        """
        Genera la tabla AUX_USER_PATTERN en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_USER_PATTERN (
                            ID              INTEGER PRIMARY KEY AUTOINCREMENT
                                                    NOT NULL
                                                    UNIQUE,
                            USER_PATTERN_ID TEXT    REFERENCES USER_PATTERN (
                            ID) ON DELETE CASCADE
                                                                                 ON UPDATE CASCADE,
                            TEST_ID         INTEGER REFERENCES TESTS (ID) ON 
                            DELETE CASCADE
                                                                          ON 
                                                                          UPDATE CASCADE,
                            UNIQUE(USER_PATTERN_ID,TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createDayTable(self):
        """
        Genera la tabla TESTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """CREATE TABLE IF NOT EXISTS DAY (
                            ID             TEXT PRIMARY KEY
                                                UNIQUE,
                            DATE           DATE,
                            DEMAND_PATTERN TEXT REFERENCES DEMAND_PATTERN (
                            ID) ON DELETE CASCADE
                                                                               ON UPDATE CASCADE,
                            UNIQUE(ID,DATE,DEMAND_PATTERN)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxDayTable(self):
        """
        Genera la tabla AUX_DAY en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_DAY (
                                    ID              INTEGER PRIMARY KEY 
                                    AUTOINCREMENT
                                                            NOT NULL
                                                            UNIQUE,
                                    DAY_ID TEXT    REFERENCES DAY (ID) ON 
                                    DELETE CASCADE
                                                                       ON 
                                                                       UPDATE 
                                                                       CASCADE,
                                    TEST_ID         INTEGER REFERENCES TESTS 
                                    (ID) ON DELETE CASCADE
                                                                                  ON UPDATE CASCADE,
                                    UNIQUE(DAY_ID,TEST_ID));"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    # Funciones para insertar datos en la base de datos de la demanda
    def insertTestData(self, testName, observations=""):
        """
        Inserta los datos del test en la tabla TESTS
        :param testName: Nombre del test actual
        :return:
        """
        self.initCursor()
        try:
            query = f"INSERT OR IGNORE INTO TESTS (NAME) VALUES ('{testName}')"
            self.cursor.execute(query)
            query = (f"UPDATE TESTS SET OBSERVATIONS = '{observations}' WHERE "
                     f"TESTS.NAME = '{testName}'")
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def insertMarketData(self, marketData):
        """
        Inserta los datos del test en la tabla MARKET
        :param marketData: Datos del mercado
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO MARKET (ID,DEPARTURE_STATION,"
                "DEPARTURE_STATION_COORDS,ARRIVAL_STATION,"
                "ARRIVAL_STATION_COORDS) "
                "VALUES (?,?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, marketData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertDemandPatternData(self, demandPatternData):
        """
        Inserta los datos del test en la tabla DEMAND_PATTERN
        :param demandPatternData: Datos del patron de demanda
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO DEMAND_PATTERN (ID,NAME) "
                     "VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [demandPattern[:2]
                         for demandPattern in demandPatternData]
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertUserPatternData(self, userPatternData):
        """
        Inserta los datos del test en la tabla USER_PATTERN
        :param userPatternData: Datos del patron de usuario
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO USER_PATTERN (ID,NAME,RULES,"
                "ARRIVAL_TIME,ARRIVAL_TIME_KWARGS,PURCHASE_DAY,"
                "PURCHASE_DAY_KWARGS,FORBIDDEN_DEPARTURE_HOURS,SEATS,"
                "TRAIN_SERVICE_PROVIDERS,EARLY_STOP,"
                "UTILITY_THRESHOLD,ERROR,ERROR_KWARGS) VALUES (?,?,?,?,?,?,?,"
                "?,?,?,?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [userPattern[:3] + userPattern[4:]
                         for userPattern in userPatternData]
            self.cursor.executemany(query, inputData)

            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertMarketsData(self, demandPatternData):
        """
        Inserta los datos del test en la tabla MARKETS
        :param demandPatternData: Datos del patron de demanda
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO MARKETS (DEMAND_PATTERN_ID,MARKET,"
                "POTENTIAL_DEMAND,POTENTIAL_DEMAND_KWARGS)"
                " VALUES (?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[demandPattern[0]] + market[:3]
                         for demandPattern in demandPatternData
                         for market in demandPattern[2]]
            self.cursor.executemany(query, inputData)

            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertUserPatternDistributionData(self, demandPatternData):
        """
        Inserta los datos del test en la tabla USER_PATTERN_DISTRIBUTION
        :param demandPatternData: Datos del patron de demanda
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO USER_PATTERN_DISTRIBUTION (MARKET_ID,"
                "DEMAND_PATTERN_ID,USER_PATTERN_ID,"
                "PERCENTAGE) "
                "VALUES (?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[data[0], demandPattern[0], uID, per]
                         for demandPattern in demandPatternData
                         for data in demandPattern[2]
                         for uID, per in data[3].items()]
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertVariableData(self, userPatternData):
        """
        Inserta los datos del test en la tabla VARIABLE
        :param userPatternData: Datos del patron de usuario
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO VARIABLE (USER_PATTERN_ID,NAME,TYPE,"
                "SUPPORT,SETS,LABELS)"
                "VALUES (?,?,?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[userPattern[0], data.get("name"), data.get("type"),
                          json.dumps(data.get("support")),
                          json.dumps(data.get("sets")),
                          json.dumps(data.get("labels"))]
                         for userPattern in userPatternData
                         for data in userPattern[3]]
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertDayData(self, dayData):
        """
        Inserta los datos del test en la tabla DAY
        :param dayData: Datos del día del que se va a realizar el test
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO DAY (ID,DATE,DEMAND_PATTERN)"
                     "VALUES (?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, dayData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxDemandPatternData(self, demandPatternData, testID):
        """
        Inserta los datos del test en la tabla AUX_DEMAND_PATTERN
        :param demandPatternData: Datos del patron de demanda
        :param testID: ID del test al que pertenecen los datos
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO AUX_DEMAND_PATTERN (DEMAND_PATTERN_ID,"
                "TEST_ID)"
                "VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[demandPattern[0], testID] for demandPattern in
                         demandPatternData]
            self.cursor.executemany(query, inputData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxMarketData(self, marketData, testID):
        """
        Inserta los datos del test en la tabla AUX_MARKET
        :param marketData: Datos de los mercados
        :param testID: ID del test al que pertenecen los datos
        :return:
        """
        self.initCursor()
        try:
            query = ("INSERT OR IGNORE INTO AUX_MARKET (MARKET_ID,TEST_ID)"
                     "VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[market[0], testID] for market in marketData]
            self.cursor.executemany(query, inputData)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxUserPatternData(self, userPatternData, testID):
        """
        Inserta los datos del test en la tabla AUX_USER_PATTERN
        :param userPatternData: Datos de los mercados
        :param testID: ID del test al que pertenecen los datos
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO AUX_USER_PATTERN (USER_PATTERN_ID,"
                "TEST_ID)"
                "VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[userPattern[0], testID] for userPattern in
                         userPatternData]
            self.cursor.executemany(query, inputData)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def insertAuxDayData(self, dayData, testID):
        """
        Inserta los datos del test en la tabla AUX_DAY
        :param dayData: Datos de los días
        :param testID: ID del test al que pertenecen los datos
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO AUX_DAY (DAY_ID,TEST_ID) VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            inputData = [[day[0], testID] for day in dayData]
            self.cursor.executemany(query, inputData)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    # Funciones para eliminar un test y lo que cuelgue de este
    def deleteTestEntryOld(self):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
        con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            names, testNames = self.selectTestName()
            if names == "" or testNames == []: raise EmptyTestData
            print(names)
            test = int(
                input("Introduce el numero del test que quieras borrar: ")) - 1
            query = f"""DELETE FROM TESTS WHERE TESTS.NAME = '
{testNames[test]}'"""

            self.cursor.execute(query)
            self.conector.commit()

            self.deleteUnusedMarketData()
            self.deleteUnusedUserPatternData()
            self.deleteUnusedDemandPatternData()
            self.deleteUnusedDayData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except EmptyTestData as e:
            print(e)
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def deleteTestEntry(self, testList):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
        con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            for testName in testList:
                query = f"""DELETE FROM TESTS WHERE TESTS.NAME = '{testName}'"""
                self.cursor.execute(query)

            self.conector.commit()

            self.deleteUnusedMarketData()
            self.deleteUnusedUserPatternData()
            self.deleteUnusedDemandPatternData()
            self.deleteUnusedDayData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except EmptyTestData as e:
            print(e)
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            self.cursor.close()

    def deleteUnusedMarketData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
            la tabla MARKET
        :return:
        """
        try:
            query = f"""DELETE FROM MARKET
                           WHERE MARKET.ID NOT IN (
                           SELECT AUX_MARKET.MARKET_ID FROM AUX_MARKET)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()

    def deleteUnusedUserPatternData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
            la tabla USER_PATTERN
        :return:
        """
        try:
            query = f"""DELETE FROM USER_PATTERN
                           WHERE USER_PATTERN.ID NOT IN (
                           SELECT AUX_USER_PATTERN.USER_PATTERN_ID FROM 
                           AUX_USER_PATTERN)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()

    def deleteUnusedDemandPatternData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
            la tabla DEMAND_PATTERN
        :return:
        """
        try:
            query = f"""DELETE FROM DEMAND_PATTERN
                           WHERE DEMAND_PATTERN.ID NOT IN (
                           SELECT AUX_DEMAND_PATTERN.DEMAND_PATTERN_ID FROM 
AUX_DEMAND_PATTERN)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()

    def deleteUnusedDayData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla DAY
        :return:
        """
        try:
            query = f"""DELETE FROM DAY
                           WHERE DAY.ID NOT IN (
                           SELECT AUX_DAY.DAY_ID FROM AUX_DAY)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()

    # Funciones para seleccionar los datos de la base datos para volcarlos en
    # el yaml
    # Funciones auxiliares
    def selectTestName(self):
        """
        Extrae el nombre de los tests que actualmente se encuentran en la
        base de datos
        :return: names, testNames
        """
        names = ""
        testNames = []
        try:
            query = """SELECT TESTS.NAME
                       FROM TESTS"""
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            for key, name in enumerate(data):
                testNames.append(name[0])
                names = names + f"{key + 1}.{name[0]}\n"
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
            self.conector.rollback()
        except sqlite3.ProgrammingError as e:
            print(e)
            self.conector.rollback()
        finally:
            return names, testNames

    def extractSetsFromVariable(self, variableSets):
        try:
            data = {}
            for set, value in variableSets.items():
                data.update({str(set): value})
            return data
        except Exception as e:
            print(e)

    def selectAndFormatVariablesForUserPattern(self, userPatternID):
        """
                Extrae los datos de la tabla VARIABLES y los reordena para
                posteriormente agregarlos al archivo yaml
                de la demanda
                bajo la propiedad userPattern
                :param userPatternID: ID del patron de usuario al que
                pertencen las variables
                :return: Variables de userPattern
                """
        try:
            query = f"""SELECT
                            VARIABLE.NAME,
                            VARIABLE.TYPE,
                            VARIABLE.SUPPORT,
                            VARIABLE.SETS,
                            VARIABLE.LABELS
                        FROM 
                            VARIABLE
                        WHERE VARIABLE.USER_PATTERN_ID = '{userPatternID}'
                        ORDER BY VARIABLE.TYPE DESC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = []
            for element in data:
                variableData = {"name": element[0], "type": element[1]}
                if not json.loads(element[4]):
                    variableData.update(
                        {"support": json.loads(element[2]),
                         "sets": list(json.loads(element[3]).keys())})
                    variableData.update(
                        self.extractSetsFromVariable(json.loads(element[3])))
                else:
                    variableData.update({"labels": json.loads(element[4])})

                formatedData.append(variableData)
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def selectAndExtractUserPatternDistributionForMarkets(self, demandPatternID,
                                                          marketID):
        """
        Extrae los datos de la tabla USER_PATTERN_DISTRIBUTION y los reordena
        para posteriormente agregarlos a la
        propiedad markets
        bajo la propiedad user_pattern_distribution
        :param demandPatternID: ID del patron de demanda al que pertencen los
        mercados
        :param marketID: ID del mercado al que pertenece la distribucion del
        patron de usuario que vamos a obtener
        :return: Variables de userPattern
        """
        try:
            query = f"""SELECT
                            USER_PATTERN_DISTRIBUTION.USER_PATTERN_ID,
                            USER_PATTERN_DISTRIBUTION.PERCENTAGE
                        FROM 
                            USER_PATTERN_DISTRIBUTION
                        WHERE USER_PATTERN_DISTRIBUTION.DEMAND_PATTERN_ID = 
                        '{demandPatternID}'
                        AND USER_PATTERN_DISTRIBUTION.MARKET_ID = '{marketID}'
                        ORDER BY USER_PATTERN_DISTRIBUTION.USER_PATTERN_ID 
                        ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = []
            for element in data:
                formatedData.append(
                    {"id": int(element[0]), "percentage": element[1]})
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def selectAndExtractMarketsForDemandPattern(self, demandPatternID):
        """
        Extrae los datos de la tabla MARKETS y los reordena para
        posteriormente agregarlos al archivo yaml de la demanda
        bajo la propiedad userPattern
        :param demandPatternID: ID del patron de demanda al que pertencen los
mercados
        :return: Variables de userPattern
        """
        try:
            query = f"""SELECT
                            MARKETS.MARKET,
                            MARKETS.POTENTIAL_DEMAND,
                            MARKETS.POTENTIAL_DEMAND_KWARGS
                        FROM 
                            MARKETS
                        WHERE MARKETS.DEMAND_PATTERN_ID = '{demandPatternID}'
                        ORDER BY MARKETS.MARKET ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = []
            for element in data:
                formatedData.append(
                    {"market": element[0], "potential_demand": element[1],
                     "potential_demand_kwargs": json.loads(element[2]),
                     "user_pattern_distribution":
                         self.selectAndExtractUserPatternDistributionForMarkets(
                             demandPatternID, element[0])})
            return formatedData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def formatTspForUserPattern(self, tspData):
        formatedData = []
        try:
            for key, value in tspData.items():
                formatedData.append({"id": int(key), "utility": value})
            return formatedData
        except Exception as e:
            print(e)

    def formatSeatsForUserPattern(self, seatData):
        formatedData = []
        try:
            for key, value in seatData.items():
                formatedData.append({"id": int(key), "utility": value})
            return formatedData
        except Exception as e:
            print(e)

    # Funciones principales
    def getDataForDumpYamlOld(self):
        """
        (Deprecated)Genera la estructra necesaria para reconstruir el archivo
        de demanda mediante subfunciones para cada
        uno de los apartados dentro del archivo yaml.
        :return: testName, data
        """
        data = {}
        testName = ""
        try:
            self.initCursor()
            names, testNames = self.selectTestName()
            print(names)
            testName = testNames[
                int(input(
                    "Introduce el numero del test que quieres extraer de la "
                    "base de datos: ")) - 1]

            data.update(self.getDataForMarket(testName))
            data.update(self.getDataForUserPattern(testName))
            data.update(self.getDataForDemandPattern(testName))
            data.update(self.getDataForDay(testName))

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
            return testName, data

    def getDataForDumpYaml(self, testName):
        """
        Genera la estructra necesaria para reconstruir el archivo de demanda
        mediante subfunciones para cada
        uno de los apartados dentro del archivo yaml.
        :return: testName, data
        """
        data = {}
        try:
            self.initCursor()

            data.update(self.getDataForMarket(testName))
            data.update(self.getDataForUserPattern(testName))
            data.update(self.getDataForDemandPattern(testName))
            data.update(self.getDataForDay(testName))

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
            return data

    def getDataForMarket(self, testName):
        """
        Obtiene los datos de los mercados y los formatea para que sigan la
        estructra de market dentro del archivo
        yaml de la demanda
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            MARKET.ID,
                            MARKET.DEPARTURE_STATION,
                            MARKET.DEPARTURE_STATION_COORDS,
                            MARKET.ARRIVAL_STATION,
                            MARKET.ARRIVAL_STATION_COORDS

                        FROM 
                            MARKET
                        WHERE MARKET.ID IN (SELECT AUX_MARKET.MARKET_ID FROM 
                        AUX_MARKET
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_MARKET.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY MARKET.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [
                {"id": int(element[0]), "departure_station": element[1],
                 "departure_station_coords": json.loads(element[
                                                            2]),
                 "arrival_station": element[3],
                 "arrival_station_coords": json.loads(element[4])} for element
                in data]
            outputData = {"market": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForUserPattern(self, testName):
        """
        Obtiene los datos de los patrones de usuario y los formatea para que
        sigan la estructra de userPattern dentro
        del archivo
        yaml de la demanda
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            USER_PATTERN.ID,
                            USER_PATTERN.NAME,
                            USER_PATTERN.RULES,
                            USER_PATTERN.ARRIVAL_TIME,
                            USER_PATTERN.ARRIVAL_TIME_KWARGS,
                            USER_PATTERN.PURCHASE_DAY,
                            USER_PATTERN.PURCHASE_DAY_KWARGS,
                            USER_PATTERN.FORBIDDEN_DEPARTURE_HOURS,
                            USER_PATTERN.SEATS,
                            USER_PATTERN.TRAIN_SERVICE_PROVIDERS,
                            USER_PATTERN.EARLY_STOP,
                            USER_PATTERN.UTILITY_THRESHOLD,
                            USER_PATTERN.ERROR,
                            USER_PATTERN.ERROR_KWARGS

                        FROM 
                            USER_PATTERN
                        WHERE USER_PATTERN.ID IN (SELECT 
                        AUX_USER_PATTERN.USER_PATTERN_ID FROM AUX_USER_PATTERN
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_USER_PATTERN.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY USER_PATTERN.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": int(element[0]), "name": element[1],
                             "rules": json.loads(element[2]), "variables":
                                 self.selectAndFormatVariablesForUserPattern(
                                     element[0]),
                             "arrival_time": element[3],
                             "arrival_time_kwargs": json.loads(element[4]),
                             "purchase_day": element[5],
                             "purchase_day_kwargs": json.loads(element[6]),
                             "forbidden_departure_hours": json.loads(
                                 element[7]),
                             "seats": self.formatTspForUserPattern(
                                 json.loads(element[8])),
                             "train_service_providers":
                                 self.formatTspForUserPattern(
                                 json.loads(element[9])),
                             "early_stop": element[10],
                             "utility_threshold": element[11],
                             "error": element[12],
                             "error_kwargs": json.loads(element[13])} for
                            element in data]
            outputData = {"userPattern": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForDemandPattern(self, testName):
        """
        Obtiene los datos de los patrones de usuario y los formatea para que
        sigan la estructra de userPattern dentro
        del archivo
        yaml de la demanda
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            DEMAND_PATTERN.ID,
                            DEMAND_PATTERN.NAME

                        FROM 
                            DEMAND_PATTERN
                        WHERE DEMAND_PATTERN.ID IN (SELECT 
                        AUX_DEMAND_PATTERN.DEMAND_PATTERN_ID FROM 
                        AUX_DEMAND_PATTERN
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_DEMAND_PATTERN.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY DEMAND_PATTERN.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": int(element[0]), "name": element[1],
                             "markets":
                                 self.selectAndExtractMarketsForDemandPattern(
                                 element[0])} for element in data]
            outputData = {"demandPattern": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    def getDataForDay(self, testName):
        """
        Obtiene los datos de los días y los formatea para que sigan la
        estructra de day dentro del archivo
        yaml de la demanda
        :param testName: Nombre del test que se está extrayendo
        :return:
        """
        try:
            query = f"""SELECT 
                            DAY.ID,
                            DAY.DATE,
                            DAY.DEMAND_PATTERN
    
                        FROM 
                            DAY
                        WHERE DAY.ID IN (SELECT AUX_DAY.DAY_ID FROM AUX_DAY
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_DAY.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY DAY.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            formatedData = [{"id": int(element[0]), "date": element[1],
                             "demandPattern": element[2]} for element in data]
            outputData = {"day": formatedData}
            return outputData
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)


class SqlResults:
    """
        Módulo que se encarga de gestionar la entrada y salida de datos de la
        base de datos de los resultados
        :param db: Direccion de la base de datos de la oferta, por defecto será:
        <currentWorkingDirectory>/Database/resultsDb.db
    """

    # Inicializacion del objeto SqlDemand, encargado de manejar las
    # interacciones con la base de datos de la oferta
    def __init__(self, db=None):
        self.workingDirectory = os.getcwd()  # Directorio de trabajo
        self.defaultDatabaseFolder = self.workingDirectory + "/Database"  #
        # Directorio para las bases de datos
        Path(self.defaultDatabaseFolder).mkdir(parents=True,
                                               exist_ok=True)  # Generamos la
        # carpeta Database en caso de no existir
        self.defaultResultsPath = (self.defaultDatabaseFolder +
                                   "/resultsDb.db")  # Direccion de la base
        # de datos por
        # defecto
        self.conector = sqlite3.connect(
            db if db is not None  # Creamos la conexion con la base de datos
            # de la oferta
            else self.defaultResultsPath)  # Si la base de datos no existe,
        # se generara
        # automaticamente
        self.cursor = self.conector.cursor()  # Creamos el cursor para la
        # base de datos
        self.enableForeignKeys()  # Habilitamos el uso de las claves foraneas
        # en la base de datos

        self.generateDatabaseTables()  # Generamos las tablas de la base de
        # datos si estas no existen

    def enableForeignKeys(self):
        self.cursor.execute(
            "PRAGMA foreign_keys = ON")  # Habilita las claves foraneas
        # usando los PRAGMA de sqlite3
        self.conector.commit()

    def initCursor(self):
        """
        Inicializa el cursor de la base de datos, en caso de que se haya
        cerrado anteriormente.
        :return:
        """
        self.cursor = self.conector.cursor()

    def executeSelectTestsIDQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            data = self.cursor.fetchone()[0]
            return data
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()
        return -1

    def executeQuery(self, query):
        try:
            self.initCursor()
            self.cursor.execute(query)
            self.conector.commit()

            if query.strip().upper().startswith("SELECT"):
                cols = [item[0] for item in self.cursor.description]
                result = self.cursor.fetchall()
                return cols, result

        except sqlite3.Error as e:
            print(e)
            return -1
        except Exception as e:
            print(e)
            return -1
        except sqlite3.ProgrammingError as e:
            print(e)
            return -1
        finally:
            self.cursor.close()

    def generateDatabaseTables(self):
        """
        Genera las tablas de la base de datos, si estas no existieran
        previamente
        :return:
        """
        self.createTestsTable()
        self.createResultsTable()
        self.createAuxResultsTable()

    # Funciones para la creacion de las tablas de la base de datos
    def createTestsTable(self):
        """
        Genera la tabla TESTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS TESTS (
                            ID           INTEGER PRIMARY KEY AUTOINCREMENT
                                                 UNIQUE
                                                 NOT NULL,
                            NAME         TEXT    UNIQUE
                                                 NOT NULL,
                            OBSERVATIONS TEXT
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createResultsTable(self):
        """
        Genera la tabla RESULTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS RESULTS (
                                ID                     TEXT    PRIMARY KEY
                                                               NOT NULL
                                                               UNIQUE,
                                USER_PATTERN           TEXT,
                                DEPARTURE_STATION      TEXT,
                                ARRIVAL_STATION        TEXT,
                                ARRIVAL_DAY            TEXT,
                                ARRIVAL_TIME           NUMERIC,
                                PURCHASE_DAY           NUMERIC,
                                SERVICE                TEXT,
                                SERVICE_DEPARTURE_TIME NUMERIC,
                                SERVICE_ARRIVAL_TIME   NUMERIC,
                                SEAT                   TEXT,
                                PRICE                  NUMERIC,
                                UTILITY                NUMERIC,
                                BEST_SERVICE           TEXT,
                                BEST_SEAT              TEXT,
                                BEST_UTILITY           NUMERIC
                            );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def createAuxResultsTable(self):
        """
        Genera la tabla AUX_RESULTS en la base de datos, si no existe
        :return:
        """
        self.initCursor()
        try:
            query = """ CREATE TABLE IF NOT EXISTS AUX_RESULTS (
                            ID        INTEGER PRIMARY KEY AUTOINCREMENT
                                              NOT NULL
                                              UNIQUE,
                            RESULTS_ID TEXT    REFERENCES RESULTS (ID) ON 
                            DELETE CASCADE
                                                                     ON 
                                                                     UPDATE 
                                                                     CASCADE,
                            TEST_ID   INTEGER REFERENCES TESTS (ID) ON DELETE 
                            CASCADE
                                                                    ON UPDATE 
                                                                    CASCADE,
                            UNIQUE(RESULTS_ID,TEST_ID)
                        );"""
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    # Funciones para insertar datos en la base de datos de la demanda
    def insertTestData(self, testName, observations=""):
        """
        Inserta los datos del test en la tabla TESTS
        :param testName: Nombre del test actual
        :return:
        """
        self.initCursor()
        try:
            query = f"INSERT OR IGNORE INTO TESTS (NAME) VALUES ('{testName}')"
            self.cursor.execute(query)
            query = (f"UPDATE TESTS SET OBSERVATIONS = '{observations}' WHERE "
                     f"TESTS.NAME = '{testName}'")
            self.cursor.execute(query)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def insertResultsData(self, resultsData):
        """
        Inserta los datos del test en la tabla RESULTS
        :param resultsData: Datos de los resultados
        :return:
        """
        self.initCursor()
        try:
            query = (
                "INSERT OR IGNORE INTO RESULTS (ID,USER_PATTERN,"
                "DEPARTURE_STATION,ARRIVAL_STATION,ARRIVAL_DAY,"
                "ARRIVAL_TIME,PURCHASE_DAY,SERVICE,SERVICE_DEPARTURE_TIME,"
                "SERVICE_ARRIVAL_TIME,SEAT,PRICE,UTILITY,"
                "BEST_SERVICE,BEST_SEAT,BEST_UTILITY) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, resultsData)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print("results data: " + str(e))
        finally:
            self.cursor.close()

    def insertAuxReslutsData(self, resultsData, testID):
        """
        Inserta los datos del test en la tabla AUX_RESULTS
        :param resultsData: Datos de los resultados
        :param testID: ID del test al que pertenecen los datos
        :return:
        """
        self.initCursor()
        try:
            data = [(item[0], testID) for item in resultsData]
            query = ("INSERT OR IGNORE INTO AUX_RESULTS (RESULTS_ID,TEST_ID) "
                     "VALUES (?,?)")

            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.executemany(query, data)
            self.conector.commit()
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
            self.conector.rollback()
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print("aux results data: " + str(e))
        finally:
            self.cursor.close()

    # Funciones para eliminar un test y lo que cuelgue de este
    def deleteTestEntryOld(self):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
        con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            names, testNames = self.selectTestName()
            if names == "" or testNames == []: raise EmptyTestData
            # print(names)
            test = int(
                input("Introduce el numero del test que quieras borrar: ")) - 1
            query = f"""DELETE FROM TESTS WHERE TESTS.NAME = '
{testNames[test]}'"""

            self.cursor.execute(query)
            self.conector.commit()

            self.deleteUnusedResultsData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except EmptyTestData as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def deleteTestEntry(self, testList):
        """
        Borra un test elegido por el usuario y todos los datos relacionados
            con este. Si los datos son comunes a otros
        tests, estos datos no se eliminarán.
        :return:
        """
        try:
            self.initCursor()
            for testName in testList:
                query = f"""DELETE FROM TESTS WHERE TESTS.NAME = '{testName}'"""
                self.cursor.execute(query)

            self.conector.commit()

            self.deleteUnusedResultsData()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except EmptyTestData as e:
            print(e)
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            self.cursor.close()

    def deleteUnusedResultsData(self):
        """
        Borra todos los datos que no se estén utilizando por ningún test en
        la tabla RESULTS
        :return:
        """
        try:
            query = f"""DELETE FROM RESULTS
                           WHERE RESULTS.ID NOT IN (
                           SELECT AUX_RESULTS.RESULTS_ID FROM AUX_RESULTS)"""
            self.cursor.execute(query)
            self.conector.commit()

        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)

    # Funciones para seleccionar los datos de la base datos para volcarlos en
    # el yaml
    # Funciones auxiliares
    def selectTestName(self):
        """
        Extrae el nombre de los tests que actualmente se encuentran en la
 base de datos
        :return: names, testNames
        """
        names = ""
        testNames = []
        try:
            query = """SELECT TESTS.NAME
                       FROM TESTS"""
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            for key, name in enumerate(data):
                testNames.append(name[0])
                names = names + f"{key + 1}.{name[0]}\n"
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            return names, testNames

    # Funciones principales
    def getDataForDumpCsv(self, testName):
        try:
            query = f"""SELECT *
                        FROM 
                            RESULTS
                        WHERE RESULTS.ID IN (SELECT AUX_RESULTS.RESULTS_ID 
                        FROM AUX_RESULTS
                                              INNER JOIN TESTS ON TESTS.ID = 
                                              AUX_RESULTS.TEST_ID
                                              WHERE TESTS.NAME = '{testName}')
                        ORDER BY RESULTS.ID ASC"""

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print("Sqlite Error: " + str(e))
        except Exception as e:
            print(e)
        except sqlite3.ProgrammingError as e:
            print(e)


class SqlTools:
    def __init__(self):
        self.connector = sqlite3.connect(":memory:")

    def validateSyntaxQuery(self, query):
        try:
            self.connector.execute(f"EXPLAIN QUERY PLAN {query}")
            return True

        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                return True
            else:
                print(e)
                return False
        except sqlite3.Error as e:
            print(f"Query invalida: {e}")
            return False

    def validateQueryOnDb(self, query, conn):
        try:
            conn.execute(f"EXPLAIN QUERY PLAN {query}")
            return True, ""

        except sqlite3.OperationalError as e:
            print(f"Query invalida: {e}")
            return False, str(e)
        except sqlite3.Error as e:
            print(f"Query invalida: {e}")
            return False, str(e)
