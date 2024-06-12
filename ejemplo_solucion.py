# importamos las librerias con abreviaciones para referenciarlas más comodamente en el código
import tkinter as tk
from tkinter import messagebox
from funciones import Juego
import random

root = tk.Tk()  # creamos la ventana principal de Tkinter
root.title("Buscaminas by Xavi and Gerard al descubierto")
root.resizable(False, False)
x = Juego(root)  # asignamos la clase Juego a la variable x

messagebox.showinfo("IMPORTANTE", "Es importante recordar que las celdas marcadas con un -1 hacen referencia a las bombas.\nEl número de bombas totales se indican en los banderines") # importante tener en cuenta

# función para crear y mostrar el mapa aleatorio descubierto
def mapa_revelado(): # aplicamos la función de revelar_boton a todas las filas y columnas del juego
    x.empieza_juego(10, 10, random.randint(10,25), 7)  # valores de mapa pequeño
    for fila in range(x.filas): 
        for columna in range(x.colum): 
            x.revelar_boton(fila, columna)
    
    root.mainloop()  #se ejecuta la ventana

# generamos el mapa descubierto
mapa_revelado()
