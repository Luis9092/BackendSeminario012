import pyodbc

# server = 'DESKTOP-LNOKM7P\SQLEXPRESS'

server = 'ARMAGEDON12'
bd = 'FerreteriaDB'
user = 'usuarioFerreteria'
password = 'casa_12345'

try:
    conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=' +
                              server + ';DATABASE=' + bd + ';UID=' + user+';PWD=' + password)
    print('conexion exitosa')
except:
    print('Error al intentar conectarse')
    