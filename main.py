from utils import  ProxyFile

ruta_archivo = "C:\\Users\\desarrollo\\Dropbox\\Reportes SAP\\stock de inventario"
stockInventario = ProxyFile(ruta= ruta_archivo, nombre_archivo="stock de inventario", fecha_archivo="", file_conn=None)
ruta_destino = r"C:\Users\desarrollo\Downloads"


stockInventario.open()
stockInventario.update()
stockInventario.relocate()
stockInventario.close()

if __name__ == "__main__":
    import win32com.client
    print(win32com.client)