import tkinter as tk
from tkinter import ttk
#from model.consultas import crear_tabla, borrar_tabla, insertar_empleado, editar, eliminar, liquidacion_total
from model.empleados import Empleado, Jornalero, Comun
from model.conexion_db import *

def menu_barra(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width = 300, height = 300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    menu_consultas = tk.Menu(barra_menu, tearoff=0)
    menu_configuracion = tk.Menu(barra_menu, tearoff=0)
    menu_ayuda = tk.Menu(barra_menu, tearoff=0)

    barra_menu.add_cascade(label= 'inicio', menu = menu_inicio)
    barra_menu.add_cascade(label= 'consultas', menu = menu_consultas)
    barra_menu.add_cascade(label= 'configuración', menu = menu_configuracion)
    barra_menu.add_cascade(label= 'ayuda', menu = menu_ayuda)

    a = ConexionDB()
    menu_inicio.add_command(label='Agregar un registro', command= a.crear_tabla)
    menu_inicio.add_command(label='Eliminar un registro', command= a.borrar_tabla)
    menu_inicio.add_command(label='Salir', command = root.destroy)


class Frame(tk.Frame):
    def __init__(self, root = None):
        tk.Frame.__init__(self, root) 
        #también se puede heredar con super().__init__(root)
        self.pack()
        self.config(width = 500, height = 500) # bg = 'green'
        self.ci_empleado = None
    

    def campos_emppleado(self):
        #labels
        self.tipo = tk.Label(self, text ='Tipo de empleado: ')
        self.tipo.config(font=('Arial', 12, 'bold'))
        self.tipo.grid(row=0, column=0, padx=10, pady=10)

        self.nombre = tk.Label(self, text =' Nombre: ')
        self.nombre.config(font=('Arial', 12, 'bold'))
        self.nombre.grid(row=1, column=0, padx=10, pady=10)

        self.horas_trabajo = tk.Label(self, text='Horas de Trabajo: ')
        self.horas_trabajo.config(font=('Arial', 12, 'bold'))
        self.horas_trabajo.grid(row=2, column=0, padx=10, pady=10)

        self.valor_horas = tk.Label(self, text='Valor hora: ')
        self.valor_horas.config(font=('Arial', 12, 'bold'))
        self.valor_horas.grid(row=3, column=0, padx=10, pady=10)

        self.sueldo = tk.Label(self, text='Sueldo: ')
        self.sueldo.config(font=('Arial', 12, 'bold'))
        self.sueldo.grid(row=4, column=0, padx=10, pady=10)

        #Entrys
        tipo = ['común', 'jornalero']
        self.emp = tk.StringVar()
        self.entry_tipoEmpleado = ttk.Combobox(self, values=['común', 'jornalero'], textvariable = self.emp)
        self.entry_tipoEmpleado.config(width=50)
        self.entry_tipoEmpleado.grid(row = 0, column= 1, padx = 10, pady = 10, columnspan= 2)

        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable= self.mi_nombre)
        self.entry_nombre.config(width=50)
        self.entry_nombre.grid(row = 1, column= 1, padx=10, pady=10, columnspan= 2)

        self.mi_horas = tk.StringVar()
        self.entry_horasTrabajo = tk.Entry(self, textvariable= self.mi_horas)
        self.entry_horasTrabajo.config(width=50)
        self.entry_horasTrabajo.grid(row = 2, column= 1, padx=10, pady=10, columnspan= 2)

        self.mi_valor = tk.StringVar()
        self.entry_valorHora = tk.Entry(self, textvariable=self.mi_valor)
        self.entry_valorHora.config(width=50)
        self.entry_valorHora.grid(row = 3, column= 1, padx=10, pady=10, columnspan= 2)

        self.mi_sueldo = tk.StringVar()
        self.entry_sueldo = tk.Entry(self, textvariable=self.mi_sueldo)
        self.entry_sueldo.config(width=50)
        self.entry_sueldo.grid(row = 4, column= 1, padx=10, pady=10, columnspan= 2)

        self.liquido_total = tk.StringVar()
        self.entry_liquido = tk.Entry(self, textvariable=self.liquido_total)
        self.entry_liquido.config(width=50, stat='readonly')
        self.entry_liquido.grid(row = 8, column= 1, padx=10, pady=10, columnspan= 1)

        #Buttons
        self.guardar_tipo = tk.Button(self, text='guardar', command=self.habilitar_campos)
        self.guardar_tipo.config(height = 0,font=('Arial', 9, 'bold'), fg='black',cursor='hand2')
        self.guardar_tipo.grid(row=0, column=2, padx=10, pady=10)
         
        self.nuevo_empleado = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.nuevo_empleado.config(width=20, font=('Arial', 12, 'bold'),
        fg='red',cursor='hand2')
        self.nuevo_empleado.grid(row=5, column=0, padx=10, pady=10)

        self.guardar_empleado = tk.Button(self, text='Guardar', command=self.guardar_datos) 
        self.guardar_empleado.config(width=20, font=('Arial', 12, 'bold'),
        fg='black', cursor='hand2')
        self.guardar_empleado.grid(row=5, column=1, padx=10, pady=10)

        self.cancelar_empleado = tk.Button(self, text='Cancelar', command= self.desabilitar_campos)
        self.cancelar_empleado.config(width=20, font=('Arial', 12, 'bold'),
        fg='yellow', cursor='hand2')
        self.cancelar_empleado.grid(row=5, column=2, padx=10, pady=10)
        
        

        

        self.calcular_liquidacion = tk.Button(self, text='Calcular Liquidación', command= self.liquidacion)
        self.calcular_liquidacion.grid(row=8, column=0, padx=10, pady=10)

    def habilitar_campos(self):
        self.entry_tipoEmpleado.config(state='normal')
        self.cancelar_empleado.config(state='normal')
        tipos = self.emp.get()
        if tipos == 'común':
            self.entry_nombre.config(state='normal')
            self.entry_sueldo.config(state='normal')
            self.guardar_empleado.config(state='normal')  
        elif tipos == 'jornalero':
            self.entry_nombre.config(state='normal')
            self.entry_horasTrabajo.config(state='normal')
            self.entry_valorHora.config(state='normal')
            self.guardar_empleado.config(state='normal')
            
       
         
        
    def guardar_datos(self):
        a = ConexionDB()
        if self.emp.get() == 'común':
            empleado = Comun(self.mi_sueldo.get(), self.mi_nombre.get())
            if self.ci_empleado == None:
                a.insertar_empleado(empleado)
            else:
                a.editar(empleado, self.ci_empleado)
        else:
            empleado = Jornalero(self.mi_valor.get(), self.mi_horas.get(), self.mi_nombre.get())
            if self.ci_empleado == None:
                a.insertar_empleado(empleado)
            else:
                a.editar(empleado, self.ci_empleado)
        
        self.tabla_empleados()
        self.desabilitar_campos()


    def desabilitar_campos(self):
       self.mi_nombre.set('')
       self.mi_horas.set('')
       self.mi_sueldo.set('')
       self.mi_valor.set('')
       self.emp.set('')
       self.entry_tipoEmpleado.config(state='disable')
       self.entry_nombre.config(state='disable')
       self.entry_horasTrabajo.config(state='disable')
       self.entry_valorHora.config(state='disable')
       self.entry_sueldo.config(state='disable')

       self.guardar_empleado.config(state='disable')
       self.cancelar_empleado.config(state='disable')


    def tabla_empleados(self):
        self.lista_empleados = ConexionDB()
        e = self.lista_empleados.listar()


        self.tabla = ttk.Treeview(self,
        columns=('tipo','Nombre', 'horas', 'valor de h', 'sueldo'))
        self.tabla.grid(row = 6, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self,
        orient = 'vertical', command= self.tabla.yview)
        self.scroll.grid(row = 6, column= 4, sticky='nse' )

        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text = 'CI')
        self.tabla.heading('#1', text = 'TIPO')
        self.tabla.heading('#2', text = 'NOMBRE')
        self.tabla.heading('#3', text = 'HORAS')
        self.tabla.heading('#4', text = 'VALOR HORA')
        self.tabla.heading('#5', text = 'SUELDO')

        for i in e:
            self.tabla.insert('', 0, text = i[0], values =(i[1], i[2], i[3], i[4], i[5]))
        
        self.eliminar_empleado = tk.Button(self, text='Eliminar', command=self.eliminar_dato)
        self.eliminar_empleado.config(width=20, font=('Arial', 12, 'bold'),
        fg='blue',cursor='hand2')
        self.eliminar_empleado.grid(row=7, column=0, padx=10, pady=10)

        self.editar_empleado = tk.Button(self, text='Editar',command= self.editar_datos)
        self.editar_empleado.config(width=20, font=('Arial', 12, 'bold'),
        fg='green', cursor='hand2')
        self.editar_empleado.grid(row=7, column=1, padx=10, pady=10)
    
    def editar_datos(self):
        try:
            self.ci_empleado = self.tabla.item(self.tabla.selection())['text']
            self.tipo_empleado = self.tabla.item(
              self.tabla.selection())['values'][0]
            self.nombre_empleado = self.tabla.item(
              self.tabla.selection())['values'][1]
            self.horas_empleado = self.tabla.item(
                self.tabla.selection())['values'][2]
            self.valor_empleado = self.tabla.item(
                self.tabla.selection())['values'][3]
            self.sueldo_empleado = self.tabla.item(
                self.tabla.selection())['values'][4]
            
            self.habilitar_campos()

            self.entry_tipoEmpleado.insert(0, self.tipo_empleado)
            self.entry_nombre.insert(0, self.nombre_empleado)
            self.entry_horasTrabajo.insert(0, self.horas_empleado)
            self.entry_valorHora.insert(0, self.valor_empleado)
            self.entry_sueldo.insert(0, self.sueldo_empleado)

        except:
            titulo= 'Edición de datos'
            mensaje = 'No se ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)
     
    def eliminar_dato(self):
        a = ConexionDB()
        ci = self.tabla.item(self.tabla.selection())['text']
        self.tabla.delete(self.tabla.selection())
        a.eliminar(ci)

    def liquidacion(self):
        l = liquidacion_total()
        self.liquido_total.set(l)

        

        
