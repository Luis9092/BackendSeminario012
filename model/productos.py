from database.conexiondb import conexion
from database.conexionCloud import bucket


class Producto:
    def _init_(self) -> None:
        pass

    def ConsProducto(
        self,
        idproducto,
        nombre,
        descripcion,
        precio,
        cantidad,
        proveedorid,
        fechaingreso,
        imagen,
        idcategoria,
        precioventa,
    ):
        self.idproducto = idproducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.proveedorid = proveedorid
        self.fechaingreso = fechaingreso
        self.imagen = imagen
        self.idcategoria = idcategoria
        self.precioventa = precioventa

    def crearProducto(self):
        try:
            cn = conexion.cursor()
            query = "insert into Productos(nombre, descripcion, precio, cantidad, proveedorid, fechaingreso, imagen, idcategoria, precioVenta)\
            values(?,?,?,?,?,?,?,?,?)"
            cn.execute(
                query,
                (
                    self.nombre,
                    self.descripcion,
                    self.precio,
                    self.cantidad,
                    self.proveedorid,
                    self.fechaingreso,
                    self.imagen,
                    self.idcategoria,
                    self.precioventa,
                ),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def subir_imagen(self, ruta_imagen, nombre_imagen):

        try:
            bkt = bucket
            blob = bkt.blob(nombre_imagen)
            # Sube la imagen al bucket
            blob.upload_from_filename(ruta_imagen)

            # Opcionalmente, puedes hacer la imagen pública
            blob.make_public()
            # importante para poder almacenarlo
            pathpublica = blob.public_url
            print(f"Imagen subida a: {blob.public_url}")
            return pathpublica
        except Exception as e:
            print(f"Ocurrió un error al subir la imagen: {e}")
            return 0

    def VerProductos(self):
        try:
            cn = conexion.cursor()
            query = "select * from Productos order by idproducto desc;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            objecto = []
            for item in ver:
                lista = {}
                lista["idproducto"] = item[0]
                lista["nombre"] = item[1]
                lista["descripcion"] = item[2]
                lista["precio"] = item[3]
                lista["cantidad"] = item[4]
                lista["proveedorid"] = item[5]
                lista["fechaingreso"] = item[6]
                lista["imagen"] = item[7]
                lista["idcategoria"] = item[8]
                lista["precioventa"] = item[9]
                objecto.append(lista)
            return objecto
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def ModificarProducto(self):
        try:
            cn = conexion.cursor()
            query = "update Productos set nombre = ?, descripcion = ? , precio = ?,   proveedorid = ?,  imagen = ?, idcategoria = ?, precioVenta = ?\
            where idproducto = ?;"
            cn.execute(
                query,
                (
                    self.nombre,
                    self.descripcion,
                    self.precio,
                    self.proveedorid,
                    self.imagen,
                    self.idcategoria,
                    self.precioventa,
                    self.idproducto,
                ),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def eliminarArchivoServercloud(self, ruta_archivo):

        try:

            blob = bucket.blob(ruta_archivo)
            generation_match_precondition = None
            blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
            generation_match_precondition = blob.generation

            blob.delete(if_generation_match=generation_match_precondition)
            print(f"Archivo {ruta_archivo} eliminado exitosamente.")
            return 1
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
            return 0

    def eliminarProducto(self, id):
        try:
            cn = conexion.cursor()
            query = "delete from Productos where idproducto = " + str(id) 
            cn.execute(query)
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
