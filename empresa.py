import tkinter as tk
from empleado.gui_app import Frame, menu_barra

def main():
    root = tk.Tk()
    root.title("Empleados")
    app = Frame(root=root)
    menu_barra(root)
    app.campos_emppleado()
    app.desabilitar_campos()
    app.tabla_empleados()
    app.mainloop()


if __name__ =='__main__':
    main()