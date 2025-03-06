from dotenv import load_dotenv

from utils import *
import datetime



ruta_origen_dropbox = r"C:\Users\desarrollo.RLPHARMA\Dropbox\Reportes SAP\Cartera de cliente\_BASES\Cartera_de_cliente.xlsx"
ruta_origen_local = r"\\principalsql\RLPharma\CARTERA\Gestion De Cartera\Cartera Actualizada\Cartera_de_cliente.xlsx"
ruta_premium_plus = r"C:\Users\desarrollo.RLPHARMA\OneDrive - 900774610_SALUD SEGURA R Y L SAS\Bionexo\ModeloPremiumPlus.xls"
ruta_stock_inventario= r"C:\Users\desarrollo.RLPHARMA\Dropbox\Reportes SAP\stock de inventario.xlsx"
print(ruta_stock_inventario)

file_dropbox = ProxyFile(ruta=ruta_origen_dropbox, nombre_archivo="Cartera_de_cliente", fecha_archivo="", file_conn=None, destino =r"C:\Users\desarrollo.RLPHARMA\Dropbox\Reportes SAP\Cartera de cliente", is_for_update=True, time_to_update="15:38" )
file_local = ProxyFile(ruta=ruta_origen_local, nombre_archivo="Cartera_de_cliente_local", fecha_archivo="", file_conn=None, destino= r"\\principalsql\RLPharma\CARTERA\Gestion De Cartera\Cartera Actualizada", is_for_update=True,time_to_update="15:40" )
modelo_premium = ProxyFile(ruta=ruta_premium_plus, nombre_archivo="Modelo Premium", fecha_archivo="", file_conn=None, destino =None, is_for_update=False, time_to_update="15:42")
stock_inventario = ProxyFile(ruta=ruta_stock_inventario, nombre_archivo="Stock de Inventario", fecha_archivo="", file_conn=None, destino =None, is_for_update=False, time_to_update="14:44")

file_list = [stock_inventario ,modelo_premium,file_dropbox, file_local]




while True:
    timeNow = datetime.datetime.now().time().strftime("%H:%M")

    for f in file_list:
        if f.time_to_update == timeNow:
            f.open()
            f.update()
            if f.is_for_update:
                f.relocate(f.destino)  # Se pasa la ruta de destino como argumento
            f.close()




