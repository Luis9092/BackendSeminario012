from database.conexiondb import conexion
from werkzeug.security import generate_password_hash, check_password_hash
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)


class Usuario:
    def __init__(self) -> None:
        pass

    def constructorUsuario(
        self, id, nombres, apellidos, correo, password, fecha, idrol
    ):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.password = password
        self.fecha = fecha
        self.idrol = idrol

    def crearUsuario(self):
        cn = conexion.cursor()
        query = "INSERT INTO Login(nombres, apellidos, correo, Contrasenia, fechacreacion, Rol)\
                VALUES(?,?,?,?,?,?)"
        cn.execute(
            query,
            (
                self.nombres,
                self.apellidos,
                self.correo,
                self.password,
                self.fecha,
                self.idrol,
            ),
        )
        conexion.commit()
        return HTTP_201_CREATED

    def autenticarUsuario(self, correo, passw):
        retorno = ""
        seleccionar = conexion.cursor()
        resultado = seleccionar.execute(
            "select * from Login where correo ='" + correo + "'"
        )
        usuario = resultado.fetchone()
        if usuario is not None:
            contra = usuario[4]
            check_pass = check_password_hash(contra, passw)
            if check_pass:
                # retorno = HTTP_201_CREATED
                retorno = self.construirMenu(
                    usuario[6], usuario[0], usuario[1], usuario[2], usuario[3]
                )
            else:
                retorno = HTTP_400_BAD_REQUEST
        else:
            retorno = HTTP_400_BAD_REQUEST
        return retorno

    def verificarSiexiste(self):
        retorno = ""
        seleccionar = conexion.cursor()
        resultado = seleccionar.execute(
            "select * from Login where correo = '" + self.correo + "'"
        )
        usuario = resultado.fetchone()
        if usuario is not None:
            retorno = HTTP_200_OK
        else:
            retorno = HTTP_400_BAD_REQUEST
        return retorno
 

    def construirMenu(self, role, id, nombres, apellidos, correo):
        ss = conexion.cursor()
        query = "select * from menu where idRole = " + str(role) + ""
        retorno = ss.execute(query)
        ver = retorno.fetchall()
        dictPerfil = {}
        item = ""
        for m in ver:
            item += (
                '<li title="'
                + m[1]
                + '" id="'
                + m[1]
                + '"> <a href="'
                + m[2]
                + '">' +m[5] + '<span class ="text">'
                + m[1]
                + " </span> </a></li> \n"
            )
        item += '<li title="Cerrar Sesion" id="salir">\
        <a href="/salir">\
        <i class="bx bx-log-out-circle"></i>\
        <span class="text">Cerrar Sesion</span>\
        </a>\
        </li>'
        print(item)
        dictPerfil["id"] = id
        dictPerfil["nombres"] = nombres
        dictPerfil["apellidos"] = apellidos
        dictPerfil["correo"] = correo
        dictPerfil["password"] = ""
        dictPerfil["fecha"] = ""
        dictPerfil["idrol"] = 0
        dictPerfil["menu"] = item
        return dictPerfil
