from database.conexiondb import conexion


class Proveedor:
    def _init_(self) -> None:
        pass

    def verProveedores(self):
        try:
            cn = conexion.cursor()
            query = "select * from Proveedores order by ProveedorId desc;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            objecto = []
            for item in ver:
                lista = {}
                lista["id"] = item[0]
                lista["nombre"] = item[1]
                lista["telefono"] = item[2]
                lista["email"] = item[3]
                objecto.append(lista)
            return objecto
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def agregarProveedor(self, nombre, telefono, email):
        try:
            cn = conexion.cursor()
            query = "insert into Proveedores(Nombre, Telefono, Email) values(?, ?, ?)"
            cn.execute(
                query,
                (nombre, telefono, email),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
    
    def actualizarProveedor(self, idProveedor, nombre, telefono, email):
        try:
            cn = conexion.cursor()
            query = """
            UPDATE Proveedores
            SET Nombre = ?, Telefono = ?, Email = ?
            WHERE ProveedorID = ?
            """
            cn.execute(query, (nombre, telefono, email, idProveedor))
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
        
    def eliminarProveedor(self, idProveedor):
        try:
            cn = conexion.cursor()
            query = "DELETE FROM Proveedores WHERE ProveedorID = ?"
            cn.execute(query, (idProveedor,))
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

