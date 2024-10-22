from database.conexiondb import conexion


class compras:
    def __init__(self) -> None:
        pass

    def constructorCompra(
        self, idcompra, ordencompra, idproveedor, fecharOrden, fechaIngreso
    ):
        self.idcompra = idcompra
        self.ordecompra = ordencompra
        self.idproveedor = idproveedor
        self.fechaOrden = fecharOrden
        self.fechaIngreso = fechaIngreso

    def constructorcompraDetalle(
        self, iddet, idcompra, idproducto, cantidad, precioCostoUnitario
    ):
        self.iddet = iddet
        self.idcompra = idcompra
        self.idproducto = idproducto
        self.cantidad = cantidad
        self.precioCostoUnitario = precioCostoUnitario

    def agregarCompra(self):
        try:
            cn = conexion.cursor()
            query = "insert into compras(noOrdenCompra, idproveedor, fechaOrden, fechaIngreso)\
                    values(?,?,?,?);"
            cn.execute(
                query,
                (self.ordecompra, self.idproveedor, self.fechaOrden, "En Proceso"),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def seleccionarOrdenCompra(self):
        try:
            cn = conexion.cursor()
            query = "select (noOrdenCompra + 1) as nextorder from compras;"
            retorno = cn.execute(query)
            ver = retorno.fetchone()
            return {"orden": ver[0]}

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def seleccionarventa(self, fecha):
        try:
            cn = conexion.cursor()
            query = "select idcompra from compras where fechaOrden ='" + fecha + "'"
            retorno = cn.execute(query)
            ver = retorno.fetchone()
            return {"id": ver[0]}

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def agregarCompraDetalle(self):
        try:
            cn = conexion.cursor()
            query = "insert into comprasDetalle(idcompra, idproducto, cantidad, precioCostoUnitario) values(?,?,?,?);"
            cn.execute(
                query,
                (
                    self.idcompra,
                    self.idproducto,
                    self.cantidad,
                    self.precioCostoUnitario,
                ),
            )
            conexion.commit()
            return 1
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def actualizarStokc(self, cantidad, id):
        try:
            cn = conexion.cursor()
            query = (
                "Update Productos set cantidad = (cantidad + "
                + str(cantidad)
                + ") where idproducto = "
                + id
                + ";"
            )

            cn.execute(query)
            return 1

        except Exception as e:
            print(f"Error al actualizar el stock: {e}")
            return 0

    def verProductosCompras(self):
        try:
            cn = conexion.cursor()
            query = "select p.idproducto, p.nombre, p.descripcion, p.precio, p.cantidad, p.imagen, p.precioVenta, m.ProveedorID,  m.Nombre, c.idCategoria, c.categoria\
                    from Productos p, categoria c, Proveedores m where p.proveedorid = m.ProveedorID and\
                    p.idcategoria = c.idCategoria;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            data = []
            for m in ver:
                item = {}
                item["id"] = m[0]
                item["nombre"] = m[1]
                item["descripcion"] = m[2]
                item["precio"] = m[3]
                item["cantidad"] = m[4]
                item["imagen"] = m[5]
                item["precioVenta"] = m[6]
                item["proveedorid"] = m[7]
                item["nombreProveedor"] = m[8]
                item["idcategoria"] = m[9]
                item["nombreCategoria"] = m[10]
                data.append(item)
            return data
        except Exception as e:
            print(f"Error al ver los productos {e}")
            return 0

    def verCompras(self):
        try:
            cn = conexion.cursor()
            query = "select c.idcompra, c.noOrdenCompra, m.Nombre, c.fechaOrden, c.fechaIngreso from compras c, Proveedores m where c.idproveedor = m.ProveedorID;"
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            data = []
            for m in ver:
                item = {}
                item["id"] = m[0]
                item["ordencomPra"] = m[1]
                item["proveedor"] = m[2]
                item["fechaOrden"] = m[3]
                item["fechaIngreso"] = m[4]
                data.append(item)
            return data
        except Exception as e:
            print(f"Error al ver los productos {e}")
            return 0

    def buscarProductoId(self, id):
        try:
            cn = conexion.cursor()
            query = (
                "select idproducto, nombre, descripcion, precio, cantidad, imagen from Productos where idproducto = "
                + str(id)
                + ";"
            )
            retorno = cn.execute(query)
            ver = retorno.fetchone()
            item = {}
            item["id"] = ver[0]
            item["nombre"] = ver[1]
            item["descripcion"] = ver[2]
            item["precio"] = ver[3]
            item["cantidad"] = ver[4]
            item["imagen"] = ver[5]
            return item
        except Exception as e:
            print(f"Error aql buscar producto {e}")
            return 0

    def seleccionarComprasDetalle(self, idcompra):
        try:
            cn = conexion.cursor()
            query = (
                " select c.icompradetalle, c.idcompra, m.nombre, c.cantidad, c.precioCostoUnitario from comprasDetalle c, Productos m where\
                c.idproducto = m.idproducto and c.idcompra = "
                + str(idcompra)
            )
            retorno = cn.execute(query)
            ver = retorno.fetchall()
            data = []
            for m in ver:
                item = {}
                item["id"] = m[0]
                item["idcompra"] = m[1]
                item["nombre"] = m[2]
                item["cantidad"] = m[3]
                item["preciocosto"] = m[4]
                data.append(item)
            return data
        except Exception as e:
            print(f"Error al ver los productos {e}")
            return 0
