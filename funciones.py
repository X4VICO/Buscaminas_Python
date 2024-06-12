# ------------------importamos modulos------------------
import tkinter as tk
from tkinter import messagebox
import random

# ------------------creamos clase Juego------------------
# creamos todo dentro de una clase para tener todos los objetos que se generen, atributos y metodos en un mismo lugar 
class Juego:

    # ------------------en el metodo "init" definiremos el espacio de juego------------------    
    def __init__(self, master): 
        self.master = master # referenciamos al widget principal del juego
        self.botones = [] # creamos una lista para almacenar los botones del juego
        self.cronometro_id = None  # almacenamos el ID del cronómetro por si perdemos o ganamos, podamos detenerlo
        self.tiempo_final = "0.00" # creamos una variable para poder reiniciar el cronometro
        self.banderas_disponibles = 0 # creamos una variable para poder reiniciar banderas

        # --------------------------------estilo del marco superior-----------------------------
        self.marco_superior = tk.Frame(self.master, width=500, height=80, bg='LightSteelBlue1')
        self.marco_superior.pack(fill="x")
        # creamos y damos estilo al cronometro
        self.cronometro = tk.Label(self.marco_superior, text="0.00", font=("Arial", 30), bg='LightSteelBlue1')
        self.cronometro.pack(expand=False, side='right', ipadx=50, pady=15)
        # creamos y damos estilo al contador de banderines
        self.banderas_marcador = tk.Label(self.marco_superior, text=f"Banderas: {self.banderas_disponibles}", font=("Arial", 30), bg='LightSteelBlue1')
        self.banderas_marcador.pack(expand=False, side='left', padx=15)

        # --------------------------------estilo del marco central-----------------------------
        self.marco_central = tk.Frame(self.master, bg='#CDB38B')
        self.marco_central.pack(expand=False, fill=tk.BOTH) 
        
        # --------------------------------estilo del marco inferior-----------------------------   
        self.marco_inferior = tk.Frame(self.master, width=500, height=80, bg='LightSteelBlue3')
        self.marco_inferior.pack(fill='x', ipady=5)
        # espacio para instrucciones
        self.instruccion = tk.Label(self.marco_inferior, text="Selecciona la dificultad en el menú superior", font=("Arial", 14), bg='LightSteelBlue3')
        self.instruccion.pack(expand=False)
        self.create_menu()


    # ------------------creamos función para que actualice el texto del cronometro------------------
    def actualizar_crono(self):
        tiempo = float(self.cronometro["text"])
        tiempo += 0.05 # añade 0.05 al tiempo
        self.tiempo_final= f"{tiempo:.2f}" #creamos variable para guardar el tiempo jugado, para mostrar mas tarde
        self.cronometro["text"] = f"{tiempo:.2f}" # decimos que maximo use 2 numeros decimales
        self.cronometro_id = self.master.after(50, self.actualizar_crono) #actualizamos
    
    menuDIFICULTAD = {"10 Bombas": (10, 10, 10, 7), "15 Bombas": (10, 10, 15, 7), "20 Bombas": (10, 10, 20, 7), "25 Bombas": (10, 10, 25, 7),"99 Bombas ¡Te faltan ****!": (10, 10, 99, 7)}
    # {dificultad: (filas, columnas, minas, tamaño de botones)}


    # ------------------creamos función para tener un menú superior, y poder elegir la dificultad------------------
    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu) #para llamar al menu predeterminado de tkinter

        dificultad_menu = tk.Menu(menu, tearoff=0) # para que no cree la opcion de menu flotante automaticamente
        menu.add_cascade(label="¿A qué misión quieres enfrentarte?", menu=dificultad_menu) # le añadimos el texto deseado
            
        for dificultad in Juego.menuDIFICULTAD:
            dificultad_menu.add_command(label=dificultad, command=lambda d=dificultad: self.empieza_juego(*Juego.menuDIFICULTAD[d])) # lambda = función anonima que llama a self.empieza_juego para guardar parametros de dificutad escogida
            # llenamos empieza_juego con los valores de menuDIFICULTAD, de esta forma asignamos la dificultad escogida


    # -----------------creamos funcion para definir las variables principales que usamos durante el codigo----------------------
    # guardamos los parametros según la dificultad escogida en cada variable
    def empieza_juego(self, filas, colum, minas, tamaño_boton):
        self.filas = filas
        self.colum = colum
        self.minas = minas
        self.tamaño_boton = tamaño_boton
        self.minas_coor = [] # lista vacía de cordenadas de minas
        self.revel = set() # seteamos un objeto nuevo
        self.marca = set()
        self.campo = set()
        self.reiniciar_cronometro()  # llamamos a la funcion que detiene el cronometro
        self.banderas_disponibles = minas # numero de banderines disponibles segun las minas en cada dificultad
        self.actualizar_banderas() # llamamos a la funcion que nos dirá las banderas disponibles al empezar el juego
        self.crear_tabla() # llamamos a la funcion que creará el tablero de juego


    #-----------------------------funcion para crear el tablero ------------------------
    def crear_tabla(self):
        for i in self.botones: # creamos un bucle "for" para asegurarnos de que al generar una nueva tabla, todos los botones que ya estén creados, sean eliminados
            for boton in i:
                boton.grid_forget() # grid_forget para eliminar el botón
        self.botones = [] # asignamos una lista vacía de botones
        self.tabla = [[0] * self.colum for x in range(self.filas)] # generamos una matriz según la dificultad, con sus filas y columnas pertinentes. A cada boton le asignamos el valor de 0
        self.añadir_mina() # añadimos las minas
        self.añadir_nums() # añadimos la funcion que nos dirá cúantas minas hay al rededor de cada botón

        self.botones_restantes = self.filas * self.colum - self.minas # guardamos el valor de botones que no tienen minas

        for y in range(self.filas): # hacemos una matriz con bucle "for" para crear la nueva tabla
            fila = [] # cramos una lista vacía para almacenar las filas del tablero
            for j in range(self.colum): # dentro de este "for", se crean los botones para cada columna por fila, a demás le damos el formato de cada botón y asignamos el botón 3 del ratón para poner banderas
                boton = tk.Button(self.marco_central, width=self.tamaño_boton, height=self.tamaño_boton // 2, command=lambda fila=y, col=j: self.click(fila, col), bg='#CDB38B')
                boton.bind("<Button-3>", lambda event, row=y, column=j: self.banderin(row, column))
                boton.grid(row=y, column=j)
                fila.append(boton) # añadimos a la lista "fila", todas las filas con botones generadas previemente en "boton"
            self.botones.append(fila) # con todas las filas llenas de botones gracias al bucle, ya podemos almacenarlas en la variable "self.botones"


    #-----------------------------funcion para añadir minas------------------------
    def añadir_mina(self):
        self.minas_coor=random.sample([(f, c) for f in range(self.filas) for c in range(self.colum)], self.minas) # generamos unas cordenadas aleatorias para ubicar las minas
        for fila, col in self.minas_coor: # una vez tenemos todas las cordenadas generadas, le añadimos el valor de -1, para indicar de que hay una mina en dicha posición
            self.tabla[fila][col] = -1


    #-----------------------------funcion para añadir números------------------------
    # para añadir los números que nos indican cuantas minas hay adyacentes en cada botón, hemos creado un bucle que recorre como una matriz de 3x3 sobre los botones que se encuentran al lado de una cordenada de mina
    # cada vez que el bucle se tope con un boton cuyo valor es de -1, significa que hay una mina y al botón actual al que se le está aplicando el bucle, se le sumará +1 en su valor
    def añadir_nums(self):
        for fila, col in self.minas_coor:
            for f in range(fila - 1, fila + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= f < self.filas and 0 <= c < self.colum and self.tabla[f][c] != -1: # con el 0 nos aseguramos de que estemos dentro del tablero, ya que a los botones se les asignó ese valor previamente
                        self.tabla[f][c] += 1       


    #-----------------------------funcion para actualizar banderas------------------------
    # cambiamos el texto de "banderas_marcador" por uno que contenga el valor de "banderas_disponibles"
    def actualizar_banderas(self):
        self.banderas_marcador.config(text=f"Banderas: {self.banderas_disponibles}")


    #-----------------------------funcion para cuando realicemos un clik con el ratón------------------------
    def click(self, fila, col):
        if not self.cronometro_id: # primero comprobamos si el cronometro está activo. De no ser así, lo activamos con la función "actualizar_crono()"
            self.actualizar_crono()

        if (fila, col) in self.marca: # comprobamos si al botón que se está haciendo click tiene bandera. De ser el caso no pasará nada
            return
        
        if self.tabla[fila][col] == -1: # comprobamos si al botón que se está haciendo click contiene una mina. 
            self.mostrar_minas() # si hay mina, la mostramos con la función "mostrar_minas"
            self.botones[fila][col].config(bg='VioletRed2') # resaltamos la mina que ha hecho perder el juego de otro color
            self.reiniciar_cronometro()  # llamamos a la funcion que detiene el cronometro
            messagebox.showinfo("¡Has perdido!", "¡Oh no, las bombas han explotado!\nLos terroristas te han vencido en: " + str(self.tiempo_final)+ " s") # mostramos al usuario una ventana nueva con un mensaje y el tiempo que ha durado la partida
        else:
            self.revelar_boton(fila, col) # de no ser una mina, simplemente se revela el botón con la función "revelar_boton"
        

    #-----------------------------funcion para revelar botón------------------------
    def revelar_boton(self, fila, col):
        self.botones[fila][col].config(bg='#4EEE94') # ponemos de color verde el botón que se revela

        if self.tabla[fila][col] == 0: # en el caso de que el botón revelado tenga valor de 0, se mostrará con un tono de verde distinto y sin mostrar el número 0
            self.botones[fila][col].config(text="", state='disabled', bg='#43CD80')
        else:
            self.botones[fila][col].config(text=str(self.tabla[fila][col]), state='disabled') # de no ser así, el botón muestra el numeró de minas que tiene alrededor
        self.revel.add((fila, col)) # guardamos el botón como revelado dentro del objeto que seteamos al principio

        if self.tabla[fila][col] == 0: # si el botón pulsado tiene el valor de 0, busca en los botones adyacentes para revelar aquellos que también tengan el valor de 0 y mostrarlos
            for f in range(fila - 1, fila + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= f < self.filas and 0 <= c < self.colum and (f, c) not in self.revel:
                        self.revelar_boton(f, c)

        self.botones_restantes -= 1 # reducimes el número de botones que se han revelado dentro de "botones_restantes"
        if self.botones_restantes == 0: # si se llega a 0 en "botones_restantes"
            self.reiniciar_cronometro()  # llamamos a la funcion que detiene el cronometro
            messagebox.showinfo("¡Has ganado!", "¡Felicidades, nos has salvado a todos! \nHas tardado en derrotar a los terroristas: " + str(self.tiempo_final)+ " s") # mostramos al usuario una ventana nueva con un mensaje y el tiempo que ha durado la partida


    #-----------------------------funcion para añadir o quitar banderas------------------------
    def banderin(self, fila, col):
        if (fila, col) in self.revel: # comprobamos si al botón que se está haciendo click está revelado. De ser el caso no pasará nada
            return

        if (fila, col) in self.marca: # si en el botón seleccionado ya hay bandera, la quitará y actualizará el contador
            self.botones[fila][col].config(text="")
            self.botones[fila][col].config(bg='#CDB38B')
            self.marca.remove((fila, col))
            self.banderas_disponibles += 1
            self.actualizar_banderas()
        else: # de no ser el caso, añadirá el icono de bandera con un fondo amarillo y se añadirá al contador de marcas, actualizando el texto del contador
            self.botones[fila][col].config(text="🚩")
            self.botones[fila][col].config(bg='yellow')
            self.marca.add((fila, col))
            self.banderas_disponibles -= 1
            self.actualizar_banderas()


    #-----------------------------funcion para mostrar minas------------------------
    def mostrar_minas(self): # esta función mostrará en las cordenadas de minas, un icono de bomba cuando sea llamada, es decir, cuando se pierda la partida
        for fila, col in self.minas_coor:
            self.botones[fila][col].config(text="💣", state='disabled', bg='red')


    #-----------------------------reinicio de etiquetas------------------------------
    def reiniciar_cronometro(self):
        if self.cronometro_id:
            self.master.after_cancel(self.cronometro_id) # utilizamos una funcion de tkinter para llamar al ID previemente creado
            self.cronometro_id = None
            self.cronometro.config(text="0.00")
            self.reiniciar_banderin()
            
    def reiniciar_banderin(self):
        self.banderas_colocadas = 0
        self.banderas_marcador.config(text=f"Banderas: {self.banderas_colocadas}")