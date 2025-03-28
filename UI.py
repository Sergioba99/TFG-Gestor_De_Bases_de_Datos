import tkinter as tk
from os import getcwd
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from copy import deepcopy
import sys


from Modules.SQLHandler import *
from Modules.configManager import Config
from Modules.csvHandler import *
from Modules.dataLoger import *
from Modules.yalmWriter import Writer
class UI:
    """
    Clase encargada de la generacion de la ventana principal de la interfaz grafica, asi como de la logica que rige
    la aplicacion
    """

    def __init__(self):
        self.root = tk.Tk()  # Inicializacion de la ventana
        self.root.withdraw()
        #self.root.geometry("1000x525")  # Ajuste del tamaño de ventana
        self.root.title("TFG - Gestor de base de datos")  # Establecimiento del nombre de la ventana
        self.root.iconbitmap(os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),"icon.ico"))
        self.root.columnconfigure(0, weight=1)  # Activacion del autoajuste de la columna 0
        self.root.resizable(False, False)  # Restriccion del redimensionamiento de la ventana principal
        self.root.protocol("WM_DELETE_WINDOW",
                           self.onCloseEvent)  # Registro de la función a ejecutar al cerrar la aplicacion
        self.supplyLoger = SupplyLoger  # Inicializacion del objeto SupplyLoger
        self.demandLoger = DemandLoger  # Inicializacion del objeto DemandLoger
        self.resultsLoger = ResultsLoger  # Inicializacion del objeto ResultsLoger
        self.ymlParser = Parser()  # Inicializacion del módulo yamlParser
        self.ymlWriter = Writer()  # Inicializacion del módulo yamlWriter
        self.sqlSupply = SqlSupply()  # Inicializacion del objeto SqlSupply del módulo SQLHandler
        self.sqlDemand = SqlDemand()  # Inicializacion del objeto SqlDemand del módulo SQLHandler
        self.sqlResults = SqlResults()  # Inicializacion del objeto SqlResults del módulo SQLHandler
        self.config = Config()  # Inicializacion del módulo configManager
        self.csvReader = csvReader()  # Inicializacion del objeto csvReader del módulo csvHandler
        self.csvWriter = csvWriter  # Inicializacion del objeto csvWriter del módulo csvHandler
        self.init_ui()  # Inicializacion de la interfaz
        self.root.deiconify()

    def init_ui(self):
        """
        Funcion encargada de la inicializacion de la ventana principal de la aplicacion
        :return: None
        """
        # Seccion de importaciones
        # Marco de importacion
        importTitle = tk.Label(self.root, text="Importar a la base de datos")
        importFrame = tk.LabelFrame(self.root, labelwidget=importTitle, labelanchor="n", padx=5, pady=5)
        importFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        importFrame.columnconfigure((0, 1, 2), weight=1)

        # Boton para importar archivos de oferta(.yml)
        tk.Button(importFrame,
                  text="Importar archivo de oferta",
                  command=lambda: self.importSupplyButtonEvent()).grid(row=0,
                                                                       column=0,
                                                                       columnspan=1,
                                                                       padx=10,
                                                                       pady=5,
                                                                       sticky="ewns")

        # Boton para importar archivos de demanda(.yml)
        tk.Button(importFrame,
                  text="Importar archivo de demanda",
                  command=lambda: self.importDemandButtonEvent()).grid(row=0,
                                                                       column=1,
                                                                       columnspan=1,
                                                                       padx=10,
                                                                       pady=5,
                                                                       sticky="ewns")

        # Boton para importar archivos de resultados(.csv)
        tk.Button(importFrame,
                  text="Importar archivo de resultados",
                  command=lambda: self.importResultsButtonEvent()).grid(row=0,
                                                                        column=2,
                                                                        columnspan=1,
                                                                        padx=10,
                                                                        pady=5,
                                                                        sticky="ewns")

        # Seccion de exportaciones
        # Marco de importacion
        exportTitle = tk.Label(self.root, text="Exportar de la base de datos")
        exportFrame = tk.LabelFrame(self.root, labelwidget=exportTitle, labelanchor="n", padx=5, pady=5)
        exportFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        exportFrame.columnconfigure((0, 1, 2), weight=1)

        # Boton para exportar archivos de oferta(.yml)
        tk.Button(exportFrame,
                  text="Exportar archivo de oferta",
                  command=lambda: self.exportSupplyButtonEvent()).grid(row=0,
                                                                       column=0,
                                                                       columnspan=1,
                                                                       padx=10,
                                                                       pady=5,
                                                                       sticky="ewns")

        # Boton para exportar archivos de demanda(.yml)
        tk.Button(exportFrame,
                  text="Exportar archivo de demanda",
                  command=lambda: self.exportDemandButtonEvent()).grid(row=0,
                                                                       column=1,
                                                                       columnspan=1,
                                                                       padx=10,
                                                                       pady=5,
                                                                       sticky="ewns")

        # Boton para exportar archivos de resultados(.csv)
        tk.Button(exportFrame,
                  text="Exportar archivo de resultados",
                  command=lambda: self.exportResultsButtonEvent()).grid(row=0,
                                                                        column=2,
                                                                        columnspan=1,
                                                                        padx=10,
                                                                        pady=5,
                                                                        sticky="ewns")

        # Botones para borrar tests completos
        deleteTitle = tk.Label(self.root, text="Eliminar de la base de datos")
        deleteFrame = tk.LabelFrame(self.root, labelwidget=deleteTitle, labelanchor="n", padx=5, pady=5)
        deleteFrame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        deleteFrame.columnconfigure((0, 1, 2), weight=1)

        # Boton para borrar tests de oferta
        tk.Button(deleteFrame, text="Eliminar test de oferta", command=lambda: self.deleteFromDataBase("oferta")).grid(
            row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Boton para borrar tests de demanda
        tk.Button(deleteFrame, text="Eliminar test de demanda",
                  command=lambda: self.deleteFromDataBase("demanda")).grid(row=2, column=1, padx=5, pady=5,
                                                                           sticky="nsew")

        # Boton para borrar tests de resultados
        tk.Button(deleteFrame, text="Eliminar test de resultados",
                  command=lambda: self.deleteFromDataBase("resultados")).grid(row=2, column=2, padx=5, pady=5,
                                                                              sticky="nsew")

        # Seccion de SQL
        # Marco de SQL
        sqlTitle = tk.Label(self.root, text="SQL")
        sqlFrame = tk.LabelFrame(self.root, labelwidget=sqlTitle, labelanchor="n", padx=5, pady=5)
        sqlFrame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Seleccion de querys guardadas
        tk.Label(sqlFrame, text="Querys almacenadas").grid(row=0, column=0, padx=5, pady=5, sticky="esn")

        # Creacion del selector y sus dependencias
        queryComboboxOption = tk.StringVar()
        queryCombobox = ttk.Combobox(sqlFrame, textvariable=queryComboboxOption, state="readonly", justify="left",
                                     postcommand=lambda: self.updateComboboxQuerys(queryCombobox), width=105)
        queryCombobox.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Boton para ejecutar la query del selector
        tk.Button(sqlFrame, text="Ejecutar", command=lambda: self.executeSqlQuery(queryComboboxOption)).grid(row=0,
                                                                                                             column=2,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="nsew")

        # Boton para borrar la query que aparece en el selector del archivo de configuracion
        tk.Button(sqlFrame, text="Eliminar",
                  command=lambda: self.deleteSqlQuery(queryCombobox, queryComboboxOption)).grid(row=0, column=3, padx=5,
                                                                                                pady=5, sticky="nsew")

        # Manejo de querys introducidas por el usuario
        tk.Label(sqlFrame, text="Entrada de querys").grid(row=1, column=0, padx=5, pady=5, sticky="esn", rowspan=2)

        # Creacion de la entrada de texto para la ejecucion de querys definidas por el usuario y la adicion de estas
        # al archivo de configuracion
        # queryTextOption = tk.StringVar()
        textFrame = tk.Frame(sqlFrame)
        textFrame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew", rowspan=3)

        queryText = tk.Text(textFrame, width=79, height=6)
        queryText.grid(row=0, column=0, sticky="nsew")

        textScrollY = ttk.Scrollbar(textFrame, orient="vertical", command=queryText.yview)
        textScrollY.grid(row=0, column=1, sticky="ns")
        queryText.config(yscrollcommand=textScrollY.set)

        textScrollX = ttk.Scrollbar(textFrame, orient="horizontal", command=queryText.xview)
        textScrollX.grid(row=1, column=0, sticky="ew")
        queryText.config(xscrollcommand=textScrollX.set)

        # Boton para borrar el texto de la entrada de texto
        tk.Button(sqlFrame, text="Borrar", command=lambda: self.clearQueryText(queryText)).grid(row=1, column=2, padx=5,
                                                                                                pady=5, sticky="nsew")

        # Boton para ejecutar la query introducida por el usuario
        tk.Button(sqlFrame, text="Ejecutar", command=lambda: self.executeSqlQuery(queryText)).grid(row=1, column=3,
                                                                                                   padx=5, pady=5,
                                                                                                   sticky="nsew")

        # Boton para añadir la query del usuario a la configuracion
        tk.Button(sqlFrame, text="Añadir", command=lambda: self.addSqlQuery(queryText)).grid(row=1, column=4, padx=5,
                                                                                             pady=5, sticky="nsew")

        # Boton para cargar una query dentro de un archivo SQL
        tk.Button(sqlFrame, text="Cargar desde archivo", command=lambda: self.loadSqlQuery(queryText)).grid(row=2,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky="nsew",
                                                                                                            columnspan=3)

        # Boton para reiniciar la lista de querys a sus valores por defecto
        tk.Button(sqlFrame, text="Reiniciar querys almacenadas", command=lambda: self.resetSqlQuerys()).grid(row=3,
                                                                                                             column=2,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="nsew",
                                                                                                             columnspan=3)

        # Boton de salida
        tk.Button(self.root,
                  text="Salir",
                  command=lambda: self.onCloseEvent(), width=20).grid(row=4,
                                                                      column=0,
                                                                      columnspan=1,
                                                                      padx=10,
                                                                      pady=5,
                                                                      sticky="ns")

        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        screenHeight = self.root.winfo_screenheight()
        screenWidth = self.root.winfo_screenwidth()
        posX = (screenWidth - width) // 2
        posY = (screenHeight - height) // 2
        self.root.geometry(f"{width}x{height}+{posX}+{posY}")


    # Funciones para importar datos
    # Funcion para importar archivos de oferta
    def importSupplyButtonEvent(self):
        """
        Funcion encargada de importar un archivo de oferta a la base de datos al presionar el boton 'Importar archivo de oferta'
        :return: None
        """
        supplyFile = self.ymlParser.loadSupplyFile()
        # print(supplyFile)
        observations = ""
        if supplyFile != -2 and supplyFile != -1:
            if messagebox.askyesno("Añadir observaciones", "¿Desea añadir observaciones al test que se va a importar?"):
                observations = simpledialog.askstring("Observación", "Introduzca la observación para el test")
            self.supplyLoger(self.ymlParser, self.sqlSupply).logSupplyTestData(observations)
            messagebox.showinfo("Importar archivo de oferta", "Se ha importado el archivo " + str(
                self.ymlParser.supplyFileName) + ".yml a la base de datos.")
        elif supplyFile == -1:
            messagebox.showerror(title="Error al importar archivo de oferta",
                                 message="Se ha producido un error al importar el archivo de oferta a la base de datos.")

    # Funcion para importar archivos de demanda
    def importDemandButtonEvent(self):
        """
        Funcion encargada de importar un archivo de demanda a la base de datos al presionar el boton 'Importar archivo de demanda'
        :return: None
        """
        demandFile = self.ymlParser.loadDemandFile()
        # print(demandFile)
        observations = ""
        if demandFile != -2 and demandFile != -1:
            if messagebox.askyesno("Añadir observaciones", "¿Desea añadir observaciones al test que se va a importar?"):
                observations = simpledialog.askstring("Observación", "Introduzca la observación para el test")
            self.demandLoger(self.ymlParser, self.sqlDemand).logDemandTestData(observations)
            messagebox.showinfo("Importar archivo de demanda", "Se ha importado el archivo " + str(
                self.ymlParser.demandFileName) + ".yml a la base de datos")
        elif demandFile == -1:
            messagebox.showerror(title="Error al importar archivo de demanda",
                                 message="Se ha producido un error al importar el archivo de demanda a la base de datos")

    # Funcion para importar archivos de resultados
    def importResultsButtonEvent(self):
        """
        Funcion encargada de importar un archivo de resultados a la base de datos al presionar el boton 'Importar archivo de resultados'
        :return: None
        """
        resultsFile = self.csvReader.loadCsvFile()
        # print(resultsFile)
        observations = ""
        if resultsFile != -2 and resultsFile != -1:
            if messagebox.askyesno("Añadir observaciones", "¿Desea añadir observaciones al test que se va a importar?"):
                observations = simpledialog.askstring("Observación", "Introduzca la observación para el test")
            self.resultsLoger(self.csvReader, self.sqlResults).logResultsTestData(observations)
            messagebox.showinfo("Importar archivo de resultados", "Se ha importado el archivo " + str(
                self.csvReader.csvFileName) + ".csv a la base de datos")
        elif resultsFile == -1:
            messagebox.showerror(title="Error al importar archivo de resultados",
                                 message="Se ha producido un error al importar el archivo de resultados a la base de datos")

    # Funciones para exportar datos
    # Funcion para exportar archivos de oferta
    def exportSupplyButtonEvent(self):
        try:
            self.sqlSupply.initCursor()
            names, testNames = self.sqlSupply.selectTestName()
            if not testNames: raise EmptyTestData
            selectTest = SelectTestFromList(self.root, testNames)
            selectedTests = selectTest.selectedTests[0]
            data = self.sqlSupply.getDataForDumpYaml(selectedTests)
            if data and selectedTests:
                self.ymlWriter.saveFile(selectedTests, data)
                messagebox.showinfo(title="Exportacion finalizada",
                                    message="El archivo " + selectedTests + " ha sido exportado con éxito.")

        except EmptyTestData:
            message = (
                "No existen datos de ningun test dentro de la base de datos, esto puede deberse a un error "
                "o a que la base de datos se encuentra vacia.")
            messagebox.showerror("Error al borrar tests", message=message)

        except Exception as e:
            print(e)

    # Funcion para exportar archivos de demanda
    def exportDemandButtonEvent(self):
        try:
            self.sqlDemand.initCursor()
            names, testNames = self.sqlDemand.selectTestName()
            if not testNames: raise EmptyTestData
            selectTest = SelectTestFromList(self.root, testNames)
            selectedTests = selectTest.selectedTests[0]
            data = self.sqlDemand.getDataForDumpYaml(selectedTests)
            if data and selectedTests:
                self.ymlWriter.saveFile(selectedTests, data)
                messagebox.showinfo(title="Exportacion finalizada",
                                    message="El archivo " + selectedTests + " ha sido exportado con éxito.")

        except EmptyTestData:
            message = (
                "No existen datos de ningun test dentro de la base de datos, esto puede deberse a un error "
                "o a que la base de datos se encuentra vacia.")
            messagebox.showerror("Error al borrar tests", message=message)

        except Exception as e:
            print(e)

    # Funcion para exportar archivos de resultados
    def exportResultsButtonEvent(self):
        try:
            self.sqlResults.initCursor()
            names, testNames = self.sqlResults.selectTestName()
            if not testNames: raise EmptyTestData
            selectTest = SelectTestFromList(self.root, testNames)
            selectedTests = selectTest.selectedTests[0]
            data = self.sqlResults.getDataForDumpCsv(selectedTests)
            if data and selectedTests:
                self.csvWriter(selectedTests, data).saveFile()
                messagebox.showinfo(title="Exportacion finalizada",
                                    message="El archivo " + selectedTests + " ha sido exportado con éxito.")

        except EmptyTestData:
            message = (
                "No existen datos de ningun test dentro de la base de datos, esto puede deberse a un error "
                "o a que la base de datos se encuentra vacia.")
            messagebox.showerror("Error al borrar tests", message=message)

        except Exception as e:
            print(e)

    # Funcion para borrar tests de las bases de datos
    def deleteFromDataBase(self, db):
        """
        Funcion encargada de eliminar los test seleccionados por el usuario de la base de datos seleccionada.
        :param db: Nombre de la base de datos objetivo.
        :return: None
        """
        try:
            if db == "oferta":
                # Inicializacion del cursor de la base de datos
                self.sqlSupply.initCursor()

                # Seleccion de los test para eliminar
                names, testNames = self.sqlSupply.selectTestName()
                if not testNames: raise EmptyTestData
                selectTest = SelectTestFromList(self.root, testNames)
                selectedTests = deepcopy(selectTest.selectedTests)
                del selectTest

                # Si existen test seleccionados para borrar, se eliminan de la base de datos
                if selectedTests:
                    self.sqlSupply.deleteTestEntry(selectedTests)
                    messagebox.showinfo(title="Test eliminados",
                                        message="Los tests seleccionados han sido eliminados de la base de datos de la oferta.")

            elif db == "demanda":
                self.sqlDemand.initCursor()
                names, testNames = self.sqlDemand.selectTestName()
                if not testNames: raise EmptyTestData
                selectTest = SelectTestFromList(self.root, testNames)
                selectedTests = deepcopy(selectTest.selectedTests)
                del selectTest
                if selectedTests:
                    self.sqlDemand.deleteTestEntry(selectedTests)
                    messagebox.showinfo(title="Test eliminados",
                                        message="Los tests seleccionados han sido eliminados de la base de datos de la demanda.")

            elif db == "resultados":
                self.sqlResults.initCursor()
                names, testNames = self.sqlResults.selectTestName()
                if not testNames: raise EmptyTestData
                selectTest = SelectTestFromList(self.root, testNames)
                selectedTests = deepcopy(selectTest.selectedTests)
                del selectTest
                if selectedTests:
                    self.sqlResults.deleteTestEntry(selectedTests)
                    messagebox.showinfo(title="Test eliminados",
                                        message="Los tests seleccionados han sido eliminados de la base de datos de la demanda.")

        except EmptyTestData:
            message = (
                "No existen datos de ningun test dentro de la base de datos, esto puede deberse a un error "
                "o a que la base de datos se encuentra vacia.")
            messagebox.showerror("Error al borrar tests", message=message)

        except Exception as e:
            print(e)

        finally:
            # Cerramos el cursor empleado para eliminar los test de la base de datos correspondiente
            if db == "oferta":
                self.sqlSupply.cursor.close()
            elif db == "demanda":
                self.sqlDemand.cursor.close()
            elif db == "resultados":
                self.sqlResults.cursor.close()

    # Funcion para ejecutar querys de SQL
    def executeSqlQuery(self, query=None):
        """
        Funcion encargada de la ejecucion de las sentencias SQL, tanto las que se encuentren por defecto en la aplicacion,
        las que haya guardado el usuario y las que sean introducidas manualmente por el usuario sin guardarlas.
        :param query: Objeto de entrada para SQL a ejecutar o nombre de la sentencia almacenada
        :return: None
        """
        try:
            cols, results = None, None

            # Si el nombre existe dentro de las sentencias almacenadas, se cargan los datos desde la configuracion, si no,
            # se coge la query del objeto de entrada manual de la ventana principal
            if type(query) is tk.StringVar:
                if query.get() in self.config.getSQLQuerysNames():
                    qname = query.get()
                    db, q = self.config.getSQLQueryValue(qname)

                else:
                    q = query.get()
                    selectDb = SelectDataBase(self.root)
                    db = selectDb.value
                    del selectDb

            elif type(query) is tk.Text:
                if query.get("1.0", tk.END) in self.config.getSQLQuerysNames():
                    qname = query.get("1.0", tk.END)
                    db, q = self.config.getSQLQueryValue(qname)

                else:
                    q = query.get("1.0", tk.END)
                    selectDb = SelectDataBase(self.root)
                    db = selectDb.value
                    del selectDb

            else: raise TypeError
            # Ejecutamos la sentencia en la base de datos objetivo y obtenemos los datos en caso de que sea una sentencia SELECT
            tools = SqlTools()
            if db == "oferta":
                validQuery, error = tools.validateQueryOnDb(q, self.sqlSupply.conector)
                if validQuery:
                    cols, results = self.sqlSupply.executeQuery(q)
                else:
                    messagebox.showerror(title="Error detectado en la query",
                                         message="Se ha detectado un error en la query introducida.\nError: " + error)
            elif db == "demanda":
                validQuery, error = tools.validateQueryOnDb(q, self.sqlDemand.conector)
                if validQuery:
                    cols, results = self.sqlDemand.executeQuery(q)
                else:
                    messagebox.showerror(title="Error detectado en la query",
                                         message="Se ha detectado un error en la query introducida.\nError: " + error)
            elif db == "resultados":
                validQuery, error = tools.validateQueryOnDb(q, self.sqlResults.conector)
                if validQuery:
                    cols, results = self.sqlResults.executeQuery(q)
                else:
                    messagebox.showerror(title="Error detectado en la query",
                                         message="Se ha detectado un error en la query introducida.\nError: " + error)
            # print(cols,results)

            if cols is not None and results is not None:
                TableViewFrame(self.root, cols, results)
        except Exception as e:
            print(e)

    # Funcion para borrar una sentencia del almacenamiento de sentencias
    def deleteSqlQuery(self, queryCombobox, query=None):
        try:
            q = str(query.get())
            opt = messagebox.askyesno(title="Confirmar eliminación",
                                      message="¿Esta seguro de que desea eliminar " + q + " de la lista?")
            if opt:
                self.config.removeSQLQuery(q)
                self.updateComboboxQuerys(queryCombobox)
                messagebox.showinfo(title="Borrar query", message="La query " + q + " ha sido eliminada.")
        except Exception as e:
            print(e)

    # Funcion para añadir una sentencia SQL al almacenamiento de sentencias
    def addSqlQuery(self, query=None):
        try:
            q = str(query.get("1.0", tk.END))
            name = simpledialog.askstring("Nombre de la query", "Escribe un nombre para identificar la query SQL:")
            if name is not None and name != "":
                db = SelectDataBase(self.root).value
                self.config.addSQLQuery(name, db, q)
        except Exception as e:
            print(e)

    # Funcion para borrar el campo de entrada para sentencias SQL
    def clearQueryText(self, queryText):
        queryText.delete("1.0", tk.END)

    # Funcion para añadir una query SQL desde un archivo
    def loadSqlQuery(self, queryText):
        try:
            f = filedialog.askopenfilename(title="Selecciona el archivo con la query",
                                           defaultextension=".sql",
                                           filetypes=[("Archivos SQL", "*.sql"), ("Todos los archivos", "*.*")],
                                           initialdir=getcwd())
            if f:
                with open(file=f, mode="r") as file:
                    query = file.read()
                    tools = SqlTools()
                    if tools.validateSyntaxQuery(query):
                        queryText.delete("1.0", tk.END)
                        queryText.insert("1.0", query)

                    else:
                        messagebox.showerror(title="Error de sintaxis",
                                             message="Se ha detectado un error de sintaxis en la sentencia del archivo.")

        except Exception as e:
            print(e)

    # Funcion que actualiza la lista de sentencias SQL en el objeto combobox que muestra las sentencias guardadas
    def updateComboboxQuerys(self, queryCombobox):
        querysInConfig = self.config.getSQLQuerysNames()
        if querysInConfig != -2 and querysInConfig != -1:
            querysInConfig.insert(0, "")
            # print(querysInConfig)
            queryCombobox['values'] = querysInConfig
            queryCombobox.current(0)

    # Funcion que reinicia la lista de querys almacenadas a sus valores por defecto
    def resetSqlQuerys(self):
        opt = messagebox.askyesno(title="Reiniciar lista de querys",
                                  message="¿Está seguro de que quiere reiniciar la lista de querys almacenadas?\n"
                                          "Esta acción es irreversible.")
        if opt:
            self.config.resetConfig()

    # Funcion para manejar el cierre del programa
    def onCloseEvent(self):
        respuesta = messagebox.askyesno("Salir", "¿Seguro que quieres salir? Se guardaran los datos antes de salir.")
        if respuesta:  # Si el usuario acepta, se cierra la ventana
            print("Guardando datos antes de salir...")
            self.config.saveConfig()
            self.root.destroy()


class SelectDataBase(tk.Toplevel):
    """Clase encargada de generar una ventana personalizada para la seleccion de la base de datos objetivo"""

    def __init__(self, master):
        super().__init__(master)
        self.withdraw()
        self.iconbitmap(
            os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "icon.ico"))
        self.title("Seleccion de base de datos")
        width = 350
        height = 75
        screenHeight = self.winfo_screenheight()
        screenWidth = self.winfo_screenwidth()
        posX = (screenWidth - width) // 2
        posY = (screenHeight - height) // 2
        self.geometry(f"{width}x{height}+{posX}+{posY}")
        self.resizable(False, False)

        self.value = tk.StringVar()  # Almacena la opción seleccionada

        labelFrame = tk.Frame(self)
        # labelFrame.grid(selectedRow=0, column=0, padx=5, pady=5, sticky="nsew")
        labelFrame.pack(anchor="n", padx=5, pady=5)
        tk.Label(labelFrame, text="Selecciona la base de datos en la que se ejecutara la query").pack(anchor="center",
                                                                                                      fill="both",
                                                                                                      pady=5, padx=5)

        buttonsFrame = tk.Frame(self)
        # buttonsFrame.grid(selectedRow=1, column=0, padx=5, pady=5, sticky="nsew")
        buttonsFrame.pack(anchor="s", padx=5, pady=5)
        tk.Button(buttonsFrame, text="Oferta", command=lambda: self.option("oferta")).pack(side="left", anchor="e",
                                                                                           fill="both", padx=10)
        tk.Button(buttonsFrame, text="Demanda", command=lambda: self.option("demanda")).pack(side="left",
                                                                                             anchor="center",
                                                                                             fill="both", padx=10)
        tk.Button(buttonsFrame, text="Resultados", command=lambda: self.option("resultados")).pack(side="left",
                                                                                                   anchor="w",
                                                                                                   fill="both", padx=10)

        self.deiconify()
        self.transient(master)
        self.grab_set()

        self.wait_window(self)

    # Funcion para obtener la base de datos objetivo
    def option(self, opcion):
        self.value = opcion
        self.destroy()


class TableViewFrame(tk.Toplevel):
    """Clase encargada de generar las ventanas para representar los datos obtenidos mediante SELECT"""

    def __init__(self, master, cols, data):
        super().__init__(master)
        self.withdraw()
        self.cols = cols
        self.data = data
        self.attributes("-topmost", True)
        self.iconbitmap(
            os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "icon.ico"))
        self.title("Datos seleccionados")
        self.protocol("WM_DELETE_WINDOW",
                           self.onCloseEvent)
        self.init_ui()

    def init_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        trvFrame = tk.Frame(self)
        trvFrame.grid(row=0, column=0, sticky="nsew")
        trvFrame.grid_rowconfigure(1, weight=1)
        trvFrame.grid_columnconfigure(1, weight=1)

        self.trv = ttk.Treeview(
            trvFrame,
            selectmode="browse",
            columns=self.cols,
            show="headings",
            height=20,
            style="Treeview",
            padding=10
        )
        self.trv.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.trv.tag_configure("heading", background="#999")

        self.contextMenu = tk.Menu(self,tearoff=0)
        self.contextMenu.add_command(label="Copiar", command=lambda:self.cellCopy())

        self.trv.bind("<Button-3>",self.showContextMenu)

        minW = self.minWidthCalculator(deepcopy(self.data), deepcopy(self.cols))
        if minW != -1:
            for col in self.cols:
                index = self.cols.index(col)
                self.trv.column(col, anchor="c", minwidth=minW[index])
                self.trv.heading(col, text=col)

        for i, d in enumerate(self.data):
            self.trv.insert("", "end", iid=str(i + 1), text=str(i + 1), values=d)

        verticalScroll = ttk.Scrollbar(trvFrame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=verticalScroll.set)
        verticalScroll.grid(row=1, column=2, sticky='ns')

        horizontalScroll = ttk.Scrollbar(trvFrame, orient="horizontal", command=self.trv.xview)
        self.trv.configure(xscrollcommand=horizontalScroll.set)
        horizontalScroll.grid(row=2, column=1, sticky="ew")

        buttonsFrame = tk.Frame(self)
        buttonsFrame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        buttonsFrame.grid_columnconfigure(0, weight=1)

        exportButton = tk.Button(
            buttonsFrame,
            text="Exportar",
            command=lambda: self.exportarDatos(self.cols, self.data)
        )
        exportButton.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        cerrarButton = tk.Button(
            buttonsFrame,
            text="Cerrar",
            command=lambda: self.onCloseEvent()
        )
        cerrarButton.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # Ajustar dimensiones y centrar la ventana
        self.update_idletasks()
        width = self.winfo_reqwidth()
        if width > 1000:
            width = 1000
        height = self.winfo_reqheight()
        screenHeight = self.winfo_screenheight()
        screenWidth = self.winfo_screenwidth()
        posX = (screenWidth - width) // 2
        posY = (screenHeight - height) // 2
        self.geometry(f"{width}x{height}+{posX}+{posY}")
        self.deiconify()
        self.lift()
        self.after(100, lambda: self.attributes("-topmost", False))

    def exportarDatos(self,cols,data):
        fileName = simpledialog.askstring("Exportar vista", "Nombre del archivo de datos",parent=self)
        if fileName is None or fileName == "": return -1
        csv = csvWriter(fileName,data,cols)
        csv.saveFile()
        del csv

    def showContextMenu(self,event):
        self.selectedRow = self.trv.identify_row(event.y)
        self.selectedColumn = self.trv.identify_column(event.x)
        if self.selectedRow and self.selectedColumn:
            self.contextMenu.post(event.x_root,event.y_root)

    def cellCopy(self):
        if self.selectedRow and self.selectedColumn:
            columnIndex = int(self.selectedColumn.replace("#","")) - 1
            cellValue = self.trv.item(self.selectedRow)["values"][columnIndex]
            self.clipboard_clear()
            self.clipboard_append(cellValue)
            self.update()

    # Funcion para intentar calcular el ancho mínimo de las diferentes columnas del treeview
    def minWidthCalculator(self, data, cols):
        try:
            data.append(cols)
            minW = [20] * len(data[0])
            for d in data:
                minW = [max(minW[d.index(item)], len(str(item)) * 8) for item in d]
            return minW
        except Exception as e:
            print(e)
            return -1

    def onCloseEvent(self):
        self.destroy()
        del self


class SelectTestFromList(tk.Toplevel):
    """Clase encargada de generar una ventana para la seleccion de los test de una lista"""

    def __init__(self, master, testNames):
        super().__init__(master)
        self.withdraw()
        self.iconbitmap(
            os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "icon.ico"))
        self.selectedTests = []
        self.title("Selecciona un test")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frameTrv = tk.Frame(self)
        frameTrv.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.trv = ttk.Treeview(frameTrv, selectmode="extended", columns="Tests", show="headings", height=10,
                                style="Treeview", padding=10)
        self.trv.pack(side="left", fill="both", expand=True)
        self.trv.tag_configure("heading", background="#999")

        self.trv.column("Tests", anchor="c")
        self.trv.heading("Tests", text="Tests")

        for i, test in enumerate(testNames):
            self.trv.insert("", "end", iid=str(i + 1), text=str(i + 1), values=test)

        verticalScroll = ttk.Scrollbar(frameTrv, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=verticalScroll.set)
        verticalScroll.pack(side="right", fill="y")

        frameButtons = tk.Frame(self)
        frameButtons.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.okButton = tk.Button(frameButtons, text="Aceptar", command=lambda: self.getTestsNames())
        self.okButton.pack(side="left", padx=5)
        self.cancelButton = tk.Button(frameButtons, text="Cancelar", command=lambda: self.destroy())
        self.cancelButton.pack(side="left", padx=5)

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        screenHeight = self.winfo_screenheight()
        screenWidth = self.winfo_screenwidth()
        posX = (screenWidth - width) // 2
        posY = (screenHeight - height) // 2
        self.geometry(f"{width}x{height}+{posX}+{posY}")

        self.deiconify()

        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    # Funcion para obtener los nombres de los tests seleccionados por el usuario
    def getTestsNames(self):
        selected = self.trv.selection()
        if selected:
            for test in selected:
                self.selectedTests.append(self.trv.item(test, "values")[0])
            self.update_idletasks()
            self.destroy()

class PersonalizedAskstring(tk.Toplevel):
    def __init__(self,master,title:str="",prompt:str=""):
        super().__init__(master)

if __name__ == "__main__":
    app = UI()
    app.root.mainloop()