import time
from abc import ABC, abstractmethod
import shutil
import datetime
import os
import win32com.client as win32

class IFileConn(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class ProxyFile(IFileConn):
    def __init__(self, ruta, nombre_archivo, fecha_archivo, file_conn):
        self.ruta = ruta
        self.nombre_archivo= nombre_archivo
        self.fecha_archivo = fecha_archivo
        self.file_conn =file_conn

        self.connect()

    def connect(self):
        file = win32.Dispatch("Excel.Application")
        file.Visible = False
        self.file_conn = file.Workbooks.Open(self.ruta)


    def disconnect(self):
        self.file_conn.Quit()

    def open(self):
        self.file_conn.Workbooks.Open(self.ruta)



    def close(self):
        self.file_conn.Workbooks.Close()
        self.disconnect()



    def update(self):
        self.file_conn.Workbooks.RefresAll()
        time.sleep(50)




    def relocate(self, newpath):

        fecha_hoy = datetime.datetime.now().strftime("%Y%m%d")
        nombre_nuevo = f"Cartera_{fecha_hoy}.xlsx"
        ruta_destino = os.path.join(newpath, nombre_nuevo)
        shutil.copy(self.file_conn, ruta_destino)
        print(f"Reporte actualizado y guardado en: {ruta_destino}")


    def __str__(self):
        return f'{self.nombre_archivo} - {self.fecha_archivo}'