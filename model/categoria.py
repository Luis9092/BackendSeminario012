from database.conexiondb import conexion


class Categoria:
    def _init_(self) -> None:
        pass

    def agregarCategoria(self, categoria):
        try:
            cn = conexion.cursor()
            query = "insert into categoria(cateogoria) values(?)"
            cn.execute(
                query,
                (categoria),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def vercategorias(self):
        try:
            cn = conexion.cursor()
            query = "select * from categoria order by idCategoria desc;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            objecto = []
            for item in ver:
                lista = {}
                lista["id"] = item[0]
                lista["categoria"] = item[1]
                objecto.append(lista)
            return objecto
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0