import time
from abc import ABC, abstractmethod
import datetime
import os
import win32com.client as win32
import pythoncom  # Módulo para manejar errores COM


import logging

# Configuración del log
log_file = "procesos.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class IFileConn(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class ProxyFile(IFileConn):
    def __init__(self, ruta, nombre_archivo, fecha_archivo, is_for_update, time_to_update,file_conn=None, destino=None ):
        self.ruta = ruta
        self.nombre_archivo = nombre_archivo
        self.fecha_archivo = fecha_archivo
        self.destino =  destino
        self.file_conn = None  # Se inicializa en None
        self.excel_app = None  # Variable para almacenar la aplicación de Excel
        self.is_for_update = is_for_update
        self.time_to_update= time_to_update



    def connect(self):
        """Abre el archivo de Excel y lo conecta a la aplicación."""
        self.excel_app = win32.Dispatch("Excel.Application")
        #self.excel_app.Visible = False  # Mantener Excel en segundo plano
        self.file_conn = self.excel_app.Workbooks.Open(self.ruta)


    def disconnect(self):
        """Cierra el archivo y la aplicación de Excel de forma segura."""
        try:
            if self.file_conn:
                self.file_conn.Close(SaveChanges=False)  # Cierra sin guardar cambios
                self.file_conn = None  # Se libera la referencia

            if self.excel_app:
                self.excel_app.Quit()  # Cierra Excel
                self.excel_app = None  # Se libera la referencia
        except pythoncom.com_error as e:
            print(f"Error al cerrar Excel: {e}")
            logging.info(f"Error al cerrar Excel: {e}")

    def open(self):
        print("Archivo abierto.")
        logging.info(f"Archivo abierto.")
        self.connect()

    def close(self):
        """Cierra la conexión al archivo de Excel."""
        print("Proceso Exitoso")
        logging.info(f"Proceso Exitoso")
        self.disconnect()

    def update(self):
        """Actualiza los datos del archivo de Excel."""

        try:
            self.file_conn.RefreshAll()  # Refresca todas las conexiones de datos
            time.sleep(50)  # Espera para asegurar que se actualice
            self.file_conn.Save()  # Guarda los cambios
        except pythoncom.com_error as e:
            print(f"Error al actualizar el archivo: {e}")
            logging.info(f"Error al actualizar el archivo: {e}")

    def relocate(self, newpath):
        """Guarda una copia del archivo actualizado en otra ubicación."""
        try:
            fecha_hoy = datetime.datetime.now().strftime("%d%m%Y")
            nombre_nuevo = f"Cartera_{fecha_hoy}.xlsx"
            ruta_destino = os.path.join(newpath, nombre_nuevo)

            self.file_conn.SaveAs(ruta_destino)  # Guarda el archivo en la nueva ubicación
            print(f"Reporte actualizado y guardado en: {ruta_destino}")
            logging.info(f"Reporte actualizado en {ruta_destino}")
        except pythoncom.com_error as e:
            print(f"Error al mover el archivo: {e}")
            logging.info(f"Error al mover el archivo: {e}")

    def __str__(self):
        return f'{self.nombre_archivo} - {self.fecha_archivo}'
