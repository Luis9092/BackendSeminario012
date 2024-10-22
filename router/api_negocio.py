import pytz
from model.schemas import BaseLuis
from model.productos import Producto
from model.categoria import Categoria
from model.proveedores import Proveedor


import os
from fastapi import APIRouter, Response, Form, File, UploadFile
from fastapi import APIRouter, Response, HTTPException, Query
from pydantic import BaseModel
from typing import List
from database import conexiondb
from model.schemas import baseUsuario
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from model.usuarios import Usuario

# ----------- FOR SELLS MODULE ------------#
from model.ventas import Venta
from model.schemas import BaseVentas
from model.schemas.BaseVentas import Model_Venta
from model.cliente import Cliente
from model.compras import compras

# ----------- FOR SELLS MODULE ------------#

api = APIRouter()
user = Usuario()
venta = Venta()

role_map = {1: "SuperAdmin", 2: "Administrador", 3: "Empleado", 4: "Auditor"}

reverse_role_map = {"SuperAdmin": 1, "Administrador": 2, "Empleado": 3, "Auditor": 4}


class BaseUsuario(BaseModel):
    UsuarioID: int
    nombres: str
    fechacreacion: str
    rol: str

    class Config:
        orm_mode = True


class Rol(BaseModel):
    nombre: str


class RolUpdate(BaseModel):
    nuevo_rol: str


@api.get("/")
def root():
    seleccionar = conexiondb.conexion.cursor()
    resultado = seleccionar.execute("select * from role;")
    r = resultado.fetchall()
    print(r)

    return {"Iniciando": "Bienvenido"}


@api.post("/crearUsuario")
def crearUsuario(listau: baseUsuario.baseUser):
    tiempo = datetime.now()
    horaActual = tiempo.strftime("%d/%m/%Y %H:%M:%S")
    contra = generate_password_hash(listau.password, "pbkdf2:sha256:30", 30)
    user.constructorUsuario(
        0, listau.nombres, listau.apellidos, listau.correo, contra, horaActual, 3
    )

    verificar = user.verificarSiexiste()
    if verificar != HTTP_200_OK:
        retorno = user.crearUsuario()
    else:
        retorno = HTTP_400_BAD_REQUEST

    return Response(status_code=retorno)


@api.get("/autenticarUsuario/<correo><pasw>", response_model=baseUsuario.baseUser)
def autenticarUsuario(correo: str, pasw: str):

    retorno1 = user.autenticarUsuario(correo, pasw)
    if retorno1 != HTTP_400_BAD_REQUEST:
        return retorno1
    else:
        return Response(status_code=HTTP_400_BAD_REQUEST)


# ------- SELLS SECTIONS IS BEING DEVELOPED HERE -start- ------- #


@api.post("/crearVenta")
def crearVenta(venta: BaseVentas.Model_Venta):
    # Crear la instancia de Venta
    venta_model = Venta()

    # Asignar los datos de la venta principal
    venta_model.constructorVenta(
        venta.ClienteID, venta.FechaVenta, venta.Total, venta.Detalles
    )

    # Crear la venta y obtener el ID de la venta creada
    try:
        venta_id = venta_model.crearVenta()
        # Solo se envía un mensaje de éxito
        return {"message": "Venta creada con éxito", "VentaID": venta_id}
    except Exception as e:
        return {"message": "Ocurrió un error al crear la venta", "error": str(e)}, 400


@api.get("/obtenerVenta/{venta_id}")
def obtenerVenta(venta_id: int):
    venta_info = venta.obtenerVentaPorId(venta_id)
    if venta_info:
        return venta_info
    else:
        return Response(status_code=HTTP_400_BAD_REQUEST)


@api.delete("/eliminarVenta/{venta_id}")
def eliminarVenta(venta_id: int):
    venta_model = Venta()
    resultado = venta_model.eliminarVenta(venta_id)

    if "error" in resultado:
        return {"message": "Error al eliminar la venta", "error": resultado["error"]}

    return {"message": "Venta eliminada con éxito", "VentaID": resultado["VentaID"]}


@api.put("/actualizarVenta/{venta_id}")
def actualizarVenta(venta_id: int, venta: BaseVentas.Model_Venta):
    venta_model = Venta()

    # Llamar al método actualizarVenta del modelo y pasarle los datos
    response = venta_model.actualizarVenta(
        venta_id=venta_id,
        cliente_id=venta.ClienteID,
        fecha_venta=venta.FechaVenta,
        total=venta.Total,
        detalles=[
            {
                "ProductoId": detalle.ProductoId,
                "Cantidad": detalle.Cantidad,
                "PrecioUnitario": detalle.PrecioUnitario,
                "EmpleadoId": detalle.EmpleadoId,
            }
            for detalle in venta.Detalles
        ],
    )

    return response


@api.get("/ventas")
def obtenerSoloVentas():
    venta_model = Venta()

    # Llamamos al método que obtiene las ventas
    ventas = venta_model.obtenerSoloVentas()

    return {"ventas": ventas}


@api.get("/ClienteDropDown")
def ClienteDropDownList():
    Clientes = venta.obtenerClientes()
    return {"clientes": Clientes}


@api.get("/ProductoDropDown")
def ProductoDropDownList(q: str = Query("", min_length=0, max_length=50)):
    productos = venta.obtenerProductos(q)
    return {"productos": productos}


# ------- SELLS SECTIONS IS BEING DEVELOPED HERE -finish- ------- #


@api.get("/usuarios", response_model=List[BaseUsuario])
def obtener_usuarios():
    seleccionar = conexiondb.conexion.cursor()
    resultado = seleccionar.execute(
        "SELECT UsuarioID, nombres, fechacreacion, rol FROM Login;"
    )
    usuarios = resultado.fetchall()

    if usuarios:
        lista_usuarios = [
            {
                "UsuarioID": usuario[0],
                "nombres": usuario[1],
                "fechacreacion": usuario[2],
                "rol": role_map.get(usuario[3], "Desconocido"),
            }
            for usuario in usuarios
        ]
        return lista_usuarios
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------------#


@api.get("/roles", response_model=List[dict])
async def obtener_roles():
    # Suponiendo que tus roles están en la base de datos
    roles = [
        {"id": 1, "nombre": "SuperAdmin"},
        {"id": 2, "nombre": "Administrador"},
        {"id": 3, "nombre": "Empleado"},
        {"id": 4, "nombre": "Auditor"},
    ]
    return roles


# -------------------------------------------------------------------------------------- #


@api.put("/usuarios/{usuario_id}/rol", response_model=BaseUsuario)
def actualizar_rol(usuario_id: int, rol_update: RolUpdate):
    nuevo_rol = rol_update.nuevo_rol  # Obtener el nuevo rol del cuerpo
    print(f"Rol recibido: {nuevo_rol}")  # Imprimir el rol recibido

    # Convertir el nuevo rol a su valor numérico
    rol_numero = reverse_role_map.get(nuevo_rol)
    if not rol_numero:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Rol inválido."
        )

    # Actualizar el rol en la base de datos
    actualizar = conexiondb.conexion.cursor()
    actualizar.execute(
        "UPDATE Login SET rol = ? WHERE UsuarioID = ?", (rol_numero, usuario_id)
    )
    conexiondb.conexion.commit()

    # Obtener los detalles actualizados del usuario
    resultado = actualizar.execute(
        "SELECT UsuarioID, nombres, fechacreacion, rol FROM Login WHERE UsuarioID = ?",
        (usuario_id,),
    )
    usuario_actualizado = resultado.fetchone()

    if usuario_actualizado:
        return {
            "UsuarioID": usuario_actualizado[0],
            "nombres": usuario_actualizado[1],
            "fechacreacion": usuario_actualizado[2],
            "rol": role_map.get(usuario_actualizado[3], "Desconocido"),
        }
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado."
        )


# -------------------------------------------------------------------------#


@api.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    eliminar = conexiondb.conexion.cursor()
    eliminar.execute("DELETE FROM Login WHERE UsuarioID = ?", (usuario_id,))
    conexiondb.conexion.commit()

    return {"message": f"Usuario {usuario_id} eliminado correctamente"}


@api.post("/agregarProducto")
async def agregarProducto(
    file: UploadFile = File(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    proveedorid: int = Form(...),
    idcategoria: int = Form(...),
):

    pro = Producto()

    tiempo = datetime.now()
    horaActual = tiempo.strftime("%d/%m/%Y %H:%M:%S")
    precioVenta = precio + (precio * 1) / 150

    ruta = os.path.join(os.getcwd(), "imagenServer", file.filename)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # Abre el archivo para escribir
    with open(ruta, "wb") as myfile:
        content = await file.read()
        myfile.write(content)

    # Aquí puedes realizar acciones adicionales con el archivo cerrado
    retorno = pro.subir_imagen(nombre_imagen=file.filename, ruta_imagen=ruta)
    if retorno != 0:
        pro.ConsProducto(
            idproducto=0,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=0,
            proveedorid=proveedorid,
            fechaingreso=horaActual,
            imagen=retorno,
            idcategoria=idcategoria,
            precioventa=precioVenta,
        )
        retorno2 = pro.crearProducto()
        if retorno2 == 1:
            return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_204_NO_CONTENT)


@api.put("/modificarProducto")
async def modificarProducto(
    file: UploadFile = File(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    proveedorid: int = Form(...),
    idcategoria: int = Form(...),
    idproducto: int = Form(...),
    NombreImagen: str = Form(...),
):
    pro = Producto()

    precioVenta = precio + (precio * 1.24) / 100
    if file.filename == "empty_file.txt":
        retorno = NombreImagen
        pass
    else:
        pro.eliminarArchivoServercloud(NombreImagen)
        ruta = os.path.join(os.getcwd(), "imagenServer", file.filename)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)

        # Abre el archivo para escribir
        with open(ruta, "wb") as myfile:
            content = await file.read()
            myfile.write(content)
        retorno = pro.subir_imagen(nombre_imagen=file.filename, ruta_imagen=ruta)

    if retorno != 0:
        pro.ConsProducto(
            idproducto=idproducto,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=0,
            proveedorid=proveedorid,
            fechaingreso="",
            imagen=retorno,
            idcategoria=idcategoria,
            precioventa=precioVenta,
        )
        retorno2 = pro.ModificarProducto()
        if retorno2 == 1:
            return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_204_NO_CONTENT)


@api.get("/verProductor", response_model=list[BaseLuis.BaseProductos])
def verProductos():
    pr = Producto()
    retorno = pr.VerProductos()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.delete("/eliminarproducto/{id}/{nombreimagen}")
def eliminarProducto(id: int, nombreimagen: str):
    pr = Producto()
    retorno = pr.eliminarProducto(id=id)
    if retorno == 1:
        retorno2 = pr.eliminarArchivoServercloud(ruta_archivo=nombreimagen)
        if retorno2 == 1:
            return Response(status_code=HTTP_200_OK)
        else:
            return Response(status_code=HTTP_400_BAD_REQUEST)

    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.delete("/eliminarimagenServer/{name_file}")
def eliminarResultadoServer(name_file: str):
    ruta = "imagenServer/" + name_file
    try:
        if os.path.isfile(ruta):
            os.remove(ruta)
            # print(f"Archivo eliminado: {ruta}")
            return Response(status_code=HTTP_200_OK)
        else:
            # print(f"Error: El archivo no existe: {ruta}")
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as e:
        # print(f"Error al eliminar el archivo: {e}")
        return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/vercategoria", response_model=list[BaseLuis.BaseCategoria])
def verCategoria():
    ca = Categoria()
    retorno = ca.vercategorias()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.post("/crearCategoria")
def crearCategoria(lista: BaseLuis.BaseCategoria):
    ca = Categoria()
    retorno = ca.agregarCategoria(categoria=lista.categoria)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.get("/verProveedores", response_model=list[BaseLuis.BaseProveedores])
def verProveedores():
    pr = Proveedor()

    retorno = pr.verProveedores()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.post("/crearProveedor")
def crearProveedor(lista: BaseLuis.BaseProveedores):
    pr = Proveedor()
    retorno = pr.agregarProveedor(
        nombre=lista.nombre, telefono=lista.telefono, email=lista.email
    )
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.put("/actualizarProveedor/{proveedor_id}")
def actualizarProveedor(proveedor_id: int, lista: BaseLuis.BaseProveedores):
    pr = Proveedor()
    retorno = pr.actualizarProveedor(
        idProveedor=proveedor_id,
        nombre=lista.nombre,
        telefono=lista.telefono,
        email=lista.email,
    )
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)
    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.delete("/eliminarProveedor/{proveedor_id}")
def eliminarProveedor(proveedor_id: int):
    pr = Proveedor()
    retorno = pr.eliminarProveedor(proveedor_id)
    if retorno == 1:
        return {"message": f"Proveedor {proveedor_id} eliminado correctamente"}
    return Response(status_code=HTTP_404_NOT_FOUND)


# OPERACIONES CLIENTES


@api.post("/agregarCliente")
def agregarCliente(lista: BaseLuis.BaseCliente):
    cl = Cliente()
    guatemala_timezone = pytz.timezone("America/Guatemala")
    horaGuatemala = datetime.now(guatemala_timezone)
    horaActual = horaGuatemala.strftime("%Y/%m/%d %H:%M:%S")

    cl.constructorCliente(
        id=0,
        nombres=lista.nombres,
        apellidos=lista.apellidos,
        telefono=lista.telefono,
        email=lista.email,
        nit=lista.nit,
        direccion=lista.direccion,
        fechaCreacion=horaActual,
    )
    retorno = cl.agregarCliente()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    Response(status_code=HTTP_400_BAD_REQUEST)


@api.put("/modificarCliente")
def modificarCliente(lista: BaseLuis.BaseCliente):
    cl = Cliente()
    cl.constructorCliente(
        id=lista.id,
        nombres=lista.nombres,
        apellidos=lista.apellidos,
        telefono=lista.telefono,
        email=lista.email,
        nit=lista.nit,
        direccion=lista.direccion,
        fechaCreacion="",
    )
    retorno = cl.modificarCliente()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    Response(status_code=HTTP_400_BAD_REQUEST)


@api.delete("/eliminarCliente/{id}")
def eliminarCliente(id: int):
    cl = Cliente()
    retorno = cl.eliminarCliente(id=id)

    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_400_BAD_REQUEST)


@api.get("/verClientes", response_model=List[BaseLuis.BaseCliente])
def verClientes():
    cl = Cliente()
    retorno = cl.verClientes()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_400_BAD_REQUEST)


# COMPRAS


@api.post("/crearCompra")
def crearCompra(lista: BaseLuis.BaseCompra):
    c = compras()
    # guatemala_timezone = pytz.timezone("America/Guatemala")
    # horaGuatemala = datetime.now(guatemala_timezone)
    # horaActual = horaGuatemala.strftime("%Y/%m/%d %H:%M:%S")
    c.constructorCompra(
        idcompra=0,
        ordencompra=lista.ordencomPra,
        idproveedor=lista.idproveedor,
        fecharOrden=lista.fechaOrden,
        fechaIngreso="",
    )

    retorno = c.agregarCompra()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/seleccionarOrden")
def seleccionarOrden():
    c = compras()
    retorno = c.seleccionarOrdenCompra()
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/seleccionarVenta/<fecha>")
def seleccionarVenta(fecha: str):
    c = compras()
    retorno = c.seleccionarventa(fecha=fecha)
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.post("/crearCompraDetalle")
def crearCompraDetalle(data: BaseLuis.BaseCompraDetalle):
    c = compras()
    c.constructorcompraDetalle(
        0, data.idcompra, data.idproducto, data.cantidad, data.preciocostoUnitario
    )
    retorno = c.agregarCompraDetalle()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verProductosCompras", response_model=list[BaseLuis.BaseverProductosCompras])
def verProductosCompras():
    c = compras()
    retorno = c.verProductosCompras()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/obtenerproductoId/<id>", response_model=BaseLuis.Baseproductoid)
def verproductoId(id: int):
    c = compras()
    retorno = c.buscarProductoId(id)

    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verCompras", response_model=list[BaseLuis.BaseCompraview])
def verCompras():
    c = compras()
    retorno = c.verCompras()
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verComprasDetalle/<id>", response_model=list[BaseLuis.verCompraDetalle])
def verComprasDetalle(id: int):
    c = compras()
    retorno = c.seleccionarComprasDetalle(idcompra=id)
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)
