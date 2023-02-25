import mysql.connector
from tkinter import messagebox
from .empleados import *


class ConexionDB:
    def __init__(self):
        self.conexion = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="aquí la contraseña",
                                                database="empleados",
                                                buffered=True)

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()


    def crear_tabla(self):
        cursor = self.conexion.cursor()

        sql = """CREATE TABLE emp(
             ci INT AUTO_INCREMENT PRIMARY KEY,
             tipo ENUM('común', 'jornalero') DEFAULT 'común',
             nombre VARCHAR(100),
             horas INT,
             valor_hora FLOAT,
             sueldo FLOAT) """
        try:
            cursor.execute(sql)
            self.cerrar()
            titulo = 'Crear Registro'
            mensaje ='Se creo la tabla en la base de datos'
            messagebox.showinfo(titulo, mensaje)
        except:
            titulo = 'Crear registro'
            mensaje = 'La tabla ya esta creada'
            messagebox.showwarning(titulo, mensaje)

    def listar(self):
        cursor = self.conexion.cursor()
        e = []
        sql = "SELECT * FROM emp "
        try:
            cursor.execute(sql)
            e = cursor.fetchall()
            self.cerrar()
        except:
            titulo = 'listar registro'
            mensaje = 'NO exitste el registro'
            messagebox.showerror(titulo, mensaje)
        return e[::-1]

    def insertar_empleado(self, empleado):
        cursor = self.conexion.cursor()
        if type(empleado) == Jornalero:
            sql = f"""INSERT INTO emp (tipo, nombre, horas, valor_hora, sueldo) VALUES 
           ("jornalero", "{empleado.getNombre()}", "{empleado.getHorasTrabajo()}", "{empleado.getValorHora()}", "{float(empleado.getHorasTrabajo())*float(empleado.getValorHora())}")"""
        else:
            sql = f"""INSERT INTO emp (tipo, nombre, horas, valor_hora, sueldo) VALUES 
           ("común", "{empleado.getNombre()}","{0}","{0}", "{empleado.getSueldoMensual()}")"""

        try:
            cursor.execute(sql)
            self.cerrar()
        except:
            titulo = 'conexión a db'
            mensaje = 'no existe base de dato creada'
            messagebox.showerror(titulo, mensaje)

    def borrar_tabla(self):
        cursor = self.conexion.cursor()
        sql = """DROP TABLE emp"""

        try:
            cursor.execute(sql)
            self.cerrar()
            titulo = 'Borrar registro'
            mensaje = 'El registro ha sido borrado'
            messagebox.showinfo(titulo, mensaje)
        except:
            titulo = 'Borrar registro'
            mensaje = 'El registro no existe'
            messagebox.showerror(titulo, mensaje)

    def editar(self, empleado, ci):
        cursor = self.conexion.cursor()
        if type(empleado) == Jornalero:
            sql = f""" UPDATE emp SET tipo ="{'jornalero'}",nombre ="{empleado.getNombre()}", 
                  horas = "{empleado.getHorasTrabajo()}",
                  valor_hora="{empleado.getValorHora()}", sueldo ="{float(empleado.getHorasTrabajo())*float(empleado.getValorHora())}" WHERE ci ='{ci}' """
        else:
            sql = f""" UPDATE emp SET tipo ="{'común'}", nombre ="{empleado.getNombre()}", 
               horas = "{0}",
                valor_hora="{0}",
                   sueldo ="{empleado.getSueldoMensual()}" WHERE ci ='{ci}' """

        try:
            cursor.execute(sql)
            self.cerrar()
        except:
            titulo = 'Editar registro'
            mensaje = 'Error'
            messagebox.showerror(titulo, mensaje)

    def eliminar(self, ci):
        cursor = self.conexion.cursor()
        sql = f"""  DELETE FROM emp WHERE ci = "{ci}" """
        try:
            cursor.execute(sql)
            self.cerrar()
        except:
            titulo = 'Eliminar dato'
            mensaje = 'El dato no se encontraba'
            messagebox(titulo, mensaje)

def liquidacion_total ():
    l = ConexionDB()
    lista_empleados = l.listar()
    coleccion_empleados = []
    for e in lista_empleados:
        if e[1]=='jornalero':
            coleccion_empleados.append(Jornalero(e[4], e[3], e[2]))
        else:
            coleccion_empleados.append(Comun(e[5], e[2]))
    total_liquidacion = 0
    for e in coleccion_empleados:
        total_liquidacion = total_liquidacion + e.DarLiquidacion()
    return total_liquidacion