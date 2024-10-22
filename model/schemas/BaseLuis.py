from pydantic import BaseModel


class BaseProductos(BaseModel):
    idproducto: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    proveedorid: int
    fechaingreso: str
    imagen: str
    idcategoria: int
    precioventa: float


class BaseCategoria(BaseModel):
    id: int
    categoria: str


class BaseProveedores(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str


class BaseCliente(BaseModel):
    id: int
    nombres: str
    apellidos: str
    telefono: str
    email: str
    nit: str
    direccion: str
    fechaCreacion: str


class BaseCompra(BaseModel):
    id: int
    ordencomPra: int
    idproveedor: int
    fechaOrden: str
    fechaIngreso: str


class BaseCompraview(BaseModel):
    id: int
    ordencomPra: int
    proveedor: str
    fechaOrden: str
    fechaIngreso: str


class BaseCompraDetalle(BaseModel):
    id: int
    idcompra: int
    idproducto: int
    cantidad: int
    preciocostoUnitario: float


class BaseverProductosCompras(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    imagen: str
    precioVenta: float
    proveedorid: int
    nombreProveedor: str
    idcategoria: int
    nombreCategoria: str


class Baseproductoid(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    imagen: str
    
class verCompraDetalle(BaseModel):
    id: int
    idcompra: int
    nombre: str
    cantidad: int
    preciocosto: float
