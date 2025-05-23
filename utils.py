import time
from abc import ABC, abstractmethod
import datetime
import os
import win32com.client as win32
import pythoncom
import logging
from config import LOG_SETTINGS, RETRY_SETTINGS

# Configure logging
logging.basicConfig(
    filename=LOG_SETTINGS['log_file'],
    level=getattr(logging, LOG_SETTINGS['log_level']),
    format=LOG_SETTINGS['log_format'],
    datefmt=LOG_SETTINGS['date_format']
)

class FileOperationError(Exception):
    """Custom exception for file operations"""
    pass

class IFileConn(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class ProxyFile(IFileConn):
    def __init__(self, ruta, nombre_archivo, fecha_archivo, is_for_relocate, time_to_update, file_conn=None, destino=None):
        self.ruta = ruta
        self.nombre_archivo = nombre_archivo
        self.fecha_archivo = fecha_archivo
        self.destino = destino
        self.file_conn = None
        self.excel_app = None
        self.is_for_relocate = is_for_relocate
        self.time_to_update = time_to_update
        self.retry_count = 0

    def validate_path(self):
        """Validate if the file path exists"""
        print(self.ruta)
        if not os.path.exists(self.ruta):
            raise FileOperationError(f"File not found: {self.ruta}")
        if self.destino and not os.path.exists(self.destino):
            raise FileOperationError(f"Destination directory not found: {self.destino}")

    def connect(self):
        """Open Excel file and connect to application with retry logic"""
        try:
            self.validate_path()
            self.excel_app = win32.Dispatch("Excel.Application")
            self.excel_app.Visible = True
            self.file_conn = self.excel_app.Workbooks.Open(self.ruta)
            self.retry_count = 0  # Reset retry count on successful connection
        except Exception as e:
            self.retry_count += 1
            if self.retry_count >= RETRY_SETTINGS['max_retries']:
                raise FileOperationError(f"Failed to connect after {RETRY_SETTINGS['max_retries']} attempts: {str(e)}")
            logging.warning(f"Connection attempt {self.retry_count} failed: {str(e)}")
            time.sleep(RETRY_SETTINGS['retry_delay'])
            self.connect()  # Retry connection

    def disconnect(self):
        """Safely close file and Excel application"""
        try:
            if self.file_conn:
                self.file_conn.Close(SaveChanges=False)
                self.file_conn = None

            if self.excel_app:
                self.excel_app.Quit()
                self.excel_app = None
        except pythoncom.com_error as e:
            logging.error(f"Error closing Excel: {e}")
            raise FileOperationError(f"Error closing Excel: {e}")

    def open(self):
        """Open file with logging"""
        try:
            logging.info(f"Opening file: {self.nombre_archivo}")
            self.connect()
        except Exception as e:
            logging.error(f"Error opening file {self.nombre_archivo}: {str(e)}")
            raise

    def close(self):
        """Close file connection with logging"""
        try:
            logging.info(f"Closing file: {self.nombre_archivo}")
            self.disconnect()
            logging.info(f"Successfully closed: {self.nombre_archivo}")
        except Exception as e:
            logging.error(f"Error closing file {self.nombre_archivo}: {str(e)}")
            raise

    def update(self):
        """Update file with retry logic"""
        try:
            logging.info(f"Updating {self.nombre_archivo}")
            self.file_conn.RefreshAll()
            time.sleep(50)  # Wait for refresh to complete
            logging.info(f"Saving {self.nombre_archivo}")
            self.file_conn.Save()
        except Exception as e:
            logging.error(f"Error updating file {self.nombre_archivo}: {str(e)}")
            raise FileOperationError(f"Error updating file: {str(e)}")

    def relocate(self, newpath):
        """Save updated file to new location with error handling"""
        try:
            fecha_hoy = datetime.datetime.now().strftime("%Y%m%d")
            nombre_nuevo = f"Cartera_de_cliente_{fecha_hoy}.xlsx"
            ruta_destino = os.path.join(newpath, nombre_nuevo)

            self.file_conn.SaveAs(ruta_destino)
            logging.info(f"File saved to: {ruta_destino}")
        except Exception as e:
            logging.error(f"Error relocating file {self.nombre_archivo}: {str(e)}")
            raise FileOperationError(f"Error relocating file: {str(e)}")

    def __str__(self):
        return f'{self.nombre_archivo} - {self.fecha_archivo}'
