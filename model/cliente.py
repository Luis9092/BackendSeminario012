from database.conexiondb import conexion


class Cliente:
    def __init__(self) -> None:
        pass

    def constructorCliente(
        self, id, nombres, apellidos, telefono, email, nit, direccion, fechaCreacion
    ):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.email = email
        self.nit = nit
        self.direccion = direccion
        self.fechaCreacion = fechaCreacion
        
    

    def agregarCliente(self):
        try:
            cn = conexion.cursor()
            query = "insert into Clientes(nombres,apellidos, telefono, email, nit, direccion,fechaCreacion ) values(?,?,?,?,?,?,?);"
            cn.execute(
                query,
                (
                    self.nombres,
                    self.apellidos,
                    self.telefono,
                    self.email,
                    self.nit,
                    self.direccion,
                    self.fechaCreacion
                ),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def modificarCliente(self):
        try:
            cn = conexion.cursor()
            query = "update Clientes set nombres = ?, apellidos =? , telefono = ?, email = ?, nit = ?, direccion = ? where ClienteID = ?;"
            cn.execute(
                query,
                (
                    self.nombres,
                    self.apellidos,
                    self.telefono,
                    self.email,
                    self.nit,
                    self.direccion,
                    self.id,
                ),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def eliminarCliente(self, id):
        try:
            cn = conexion.cursor()
            query = "delete from Clientes where ClienteID = " + str(id)
            cn.execute(query)
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def verClientes(self):
        try:
            cn = conexion.cursor()
            query = "select ClienteID, nombres, apellidos, telefono, email,\
	        nit,direccion, fechaCreacion from    Clientes order by ClienteID desc;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            objecto = []
            for item in ver:
                lista = {}
                lista["id"] = item[0]
                lista["nombres"] = item[1]
                lista["apellidos"] = item[2]
                lista["telefono"] = item[3]
                lista["email"] = item[4]
                lista["nit"] = item[5]
                lista["direccion"] = item[6]
                lista["fechaCreacion"] = item[7]
                objecto.append(lista)
            return objecto
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    