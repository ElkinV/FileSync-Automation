from dotenv import load_dotenv
from utils import ProxyFile, FileOperationError
import datetime
import time
import logging
import sys
from config import PATHS, DESTINATIONS, UPDATE_TIMES, RETRY_SETTINGS, LOG_SETTINGS

# Configure logging
logging.basicConfig(
    filename=LOG_SETTINGS['log_file'],
    level=getattr(logging, LOG_SETTINGS['log_level']),
    format=LOG_SETTINGS['log_format'],
    datefmt=LOG_SETTINGS['date_format']
)


def create_file_objects():
    """Create file objects with configuration"""
    try:
        file_synology = ProxyFile(
            ruta=PATHS['synology'],
            nombre_archivo="Cartera_de_cliente",
            fecha_archivo="",
            file_conn=None,
            destino=DESTINATIONS['synology'],
            is_for_relocate=True,
            time_to_update=UPDATE_TIMES['synology']
        )

        file_local = ProxyFile(
            ruta=PATHS['nas'],
            nombre_archivo="Cartera_de_cliente",
            fecha_archivo="",
            file_conn=None,
            destino=DESTINATIONS['nas'],
            is_for_relocate=True,
            time_to_update=UPDATE_TIMES['nas']
        )



        stock_inventario = ProxyFile(
            ruta=PATHS['stock'],
            nombre_archivo="Stock de Inventario",
            fecha_archivo="",
            file_conn=None,
            destino=None,
            is_for_relocate=False,
            time_to_update=UPDATE_TIMES['stock']
        )

        file_invcotizar = ProxyFile(
            ruta=PATHS['inv-cotizar'],
            nombre_archivo="Inventario para cotizar",
            fecha_archivo="",
            file_conn=None,
            destino=None,
            is_for_relocate=False,
            time_to_update=UPDATE_TIMES['inv-cotizar']
        )

        return [stock_inventario, file_synology, file_local,file_invcotizar]
    except Exception as e:
        logging.error(f"Error creating file objects: {str(e)}")
        raise

def process_file(file):
    """Process a single file with error handling"""
    try:
        file.open()
        file.update()
        if file.is_for_relocate:
            file.relocate(file.destino)
        file.close()
        return True
    except FileOperationError as e:
        logging.error(f"File operation error for {file.nombre_archivo}: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error processing {file.nombre_archivo}: {str(e)}")
        return False

def main():
    """Main program loop with error handling"""
    logging.info("Starting program")
    file_list = create_file_objects()
    
    while True:
        try:
            timeNow = datetime.datetime.now().time().strftime("%H:%M")
            
            for file in file_list:
                print(file)
                print(file.time_to_update == timeNow)
                if file.time_to_update == timeNow:
                    logging.info(f"Processing file: {file.nombre_archivo}")
                    if process_file(file):
                        logging.info(f"Successfully processed: {file.nombre_archivo}")
                    else:
                        logging.error(f"Failed to process: {file.nombre_archivo}")
            
            time.sleep(RETRY_SETTINGS['check_interval'])
            
        except KeyboardInterrupt:
            logging.info("Program stopped by user")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {str(e)}")
            time.sleep(RETRY_SETTINGS['retry_delay'])

if __name__ == "__main__":
    main()




