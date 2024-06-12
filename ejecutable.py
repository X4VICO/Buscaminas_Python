# importamos las librerias con abreviaciones para referenciarlas más comodamente en el código
import tkinter as tk
import funciones as fn 

#definimos las caracteristicas principales de la ventana
root = tk.Tk()
root.title("Buscaminas by Xavi and Gerard")
root.resizable(False, False)

#llamamos a las funciones que hay dentro de la clase Juego
juego = fn.Juego(root)

#se ejecuta la ventana
root.mainloop()