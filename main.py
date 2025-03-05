from utils import *
import datetime


ruta_origen_dropbox = r"C:\Users\desarrollo.RLPHARMA\Dropbox\Reportes SAP\Cartera de cliente\_BASES\Cartera_de_cliente.xlsx"
ruta_origen_local = r"\\principalsql\RLPharma\CARTERA\Gestion De Cartera\Cartera Actualizada\Cartera_de_cliente.xlsx"


file_dropbox = ProxyFile(ruta=ruta_origen_dropbox, nombre_archivo="Cartera_de_cliente", fecha_archivo="", file_conn=None, destino =r"C:\Users\desarrollo.RLPHARMA\Dropbox\Reportes SAP\Cartera de cliente")
file_local = ProxyFile(ruta=ruta_origen_local, nombre_archivo="Cartera_de_cliente", fecha_archivo="", file_conn=None, destino= r"\\principalsql\RLPharma\CARTERA\Gestion De Cartera\Cartera Actualizada")

file_list = [file_dropbox, file_local]




while True:
    time = datetime.datetime.now().time().strftime("%H:%M")

    if time == "10:22" :
        for f in file_list:
            f.open()
            f.update()
            f.relocate(f.destino)  # Se pasa la ruta de destino como argumento
            f.close()
        time.sleep(50)



