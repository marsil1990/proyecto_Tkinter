from abc import ABC, abstractclassmethod
from empleado.gui_app import *

class Empleado(ABC):
    def __init__(self, nombre):
        self.__nombre = nombre
    def getNombre(self):
        return self.__nombre
    @abstractclassmethod
    def DarLiquidacion(self):
        pass

class Comun(Empleado):
    def __init__(self, sueldoMensual, nombre):
        self.__sueldoMensual = sueldoMensual
        Empleado.__init__(self,nombre)
    def getSueldoMensual(self):
        print(id(self.__sueldoMensual))
        return self.__sueldoMensual
    def DarLiquidacion(self):
        return self.__sueldoMensual
    #def __del__(self):
     #   print('Se elimina el objeto')

class Jornalero(Empleado):
    def __init__(self, valorHora, horasTrabajo, nombre):
        self.__valorHora = valorHora
        self.__horasTrabajo = horasTrabajo
        Empleado.__init__(self, nombre)
    def getHorasTrabajo(self):
        return self.__horasTrabajo
    def getValorHora(self):
        return self.__valorHora
    def DarLiquidacion(self):
        return self.__valorHora*self.__horasTrabajo

