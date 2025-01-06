


import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Configuración de carpeta y archivos JSON
CARPETA_DATOS = "data"  # Define el nombre del directorio donde se guardan los archivos de datos
USUARIOS_FILE = os.path.join(CARPETA_DATOS, "usuarios.json")  # Ruta al archivo "usuarios.json" dentro de la carpeta "data"
ALQUILERES_FILE = os.path.join(CARPETA_DATOS, "alquileres.json")  # Ruta al archivo "alquileres.json" dentro de la carpeta "data"

# Crear carpeta si no existe
if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)  # Crea la carpeta "data" si no existe

# Diccionario de usuarios registrados {usuario: [contraseña, saldo]}
usuarios = {}

# Diccionario de máquinas y su disponibilidad
maquinarias = {
    "Excavadora": {"precio": 100000, "disponible": True},
    "Retroexcavadora": {"precio": 120000, "disponible": True},
    "Grúa": {"precio": 150000, "disponible": True},
    "Tractor": {"precio": 80000, "disponible": True}
}

# Registro de alquileres
alquileres = []

# Configuración global
VENTANA_ANCHO = 600  # Ancho de la ventana principal
VENTANA_ALTO = 700  # Alto de la ventana principal
FONDO_COLOR = "yellow"  # Color de fondo
FUENTE_TITULO = ("Helvetica", 16, "bold")  # Fuente para los títulos
FUENTE_ESTILO = ("Helvetica", 12, "bold")  # Fuente para el texto
TEXTO_COLOR = "black"  # Color del texto

# Función para cargar datos desde JSON
def cargar_datos():
    global usuarios, alquileres
    try:
        with open(USUARIOS_FILE, "r") as f:  # Abre "usuarios.json" en modo lectura
            usuarios = json.load(f)  # Carga los datos en el diccionario "usuarios"
    except FileNotFoundError:
        usuarios = {}  # Si el archivo no existe, inicializa como un diccionario vacío

    try:
        with open(ALQUILERES_FILE, "r") as f:  # Abre "alquileres.json" en modo lectura
            alquileres = json.load(f)  # Carga los datos en la lista "alquileres"
    except FileNotFoundError:
        alquileres = []  # Si el archivo no existe, inicializa como una lista vacía

# Función para guardar datos en JSON
def guardar_datos():
    with open(USUARIOS_FILE, "w") as f:  # Abre "usuarios.json" en modo escritura
        json.dump(usuarios, f, indent=4)  # Guarda los datos de "usuarios" en formato JSON
    with open(ALQUILERES_FILE, "w") as f:  # Abre "alquileres.json" en modo escritura
        json.dump(alquileres, f, indent=4)  # Guarda los datos de "alquileres" en formato JSON

# Función para centrar ventanas
def centrar_ventana(ventana):
    pantalla_ancho = ventana.winfo_screenwidth()  # Ancho de la pantalla
    pantalla_alto = ventana.winfo_screenheight()  # Alto de la pantalla
    x = (pantalla_ancho // 2) - (VENTANA_ANCHO // 2)  # Calcula la posición X
    y = (pantalla_alto // 2) - (VENTANA_ALTO // 2)  # Calcula la posición Y
    ventana.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}+{x}+{y}")  # Ajusta el tamaño y posición de la ventana

# Función para agregar encabezado a la ventana
def agregar_encabezado(ventana):
    logo = tk.Label(ventana, text="🛠️ HeavyMachine", font=("Helvetica", 18, "bold"), bg=FONDO_COLOR, fg=TEXTO_COLOR)
    logo.pack(pady=10)  # Muestra el logo en la parte superior
    titulo = tk.Label(ventana, text="Tu tienda de maquinaria pesada", font=FUENTE_TITULO, bg=FONDO_COLOR, fg=TEXTO_COLOR)
    titulo.pack(pady=5)  # Muestra el título principal

# Función para registrar usuario
def registrar_usuario():
    username = entry_usuario.get()  # Obtiene el nombre de usuario ingresado
    password = entry_contraseña.get()  # Obtiene la contraseña ingresada
    if username in usuarios:  # Verifica si el usuario ya está registrado
        messagebox.showerror("Error", "Usuario ya registrado.")
    else:
        usuarios[username] = [password, 0]  # Agrega el usuario con contraseña y saldo inicial 0
        guardar_datos()  # Guarda los datos actualizados
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        ventana_registro.destroy()  # Cierra la ventana de registro
        ventana_inicio_sesion()  # Abre la ventana de inicio de sesión

# Función para iniciar sesión
def iniciar_sesion():
    username = entry_usuario.get()  # Obtiene el nombre de usuario ingresado
    password = entry_contraseña.get()  # Obtiene la contraseña ingresada
    if username in usuarios and usuarios[username][0] == password:  # Verifica usuario y contraseña
        messagebox.showinfo("Bienvenido", f"Bienvenido, {username}.")
        ventana_inicio.destroy()  # Cierra la ventana de inicio de sesión
        ingresar_saldo(username)  # Llama a la función para ingresar saldo
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para ingresar saldo
def ingresar_saldo(username):
    saldo = simpledialog.askinteger("Saldo disponible", "¿Cuánto dinero deseas ingresar en tu cuenta?", minvalue=80000)  # Solicita saldo al usuario
    if saldo is not None:
        if saldo >= 80000:  # Verifica que el saldo sea mayor o igual a 80,000
            usuarios[username][1] = saldo  # Actualiza el saldo del usuario
            guardar_datos()  # Guarda los datos actualizados
            messagebox.showinfo("Saldo actualizado", f"Tu saldo es de ${saldo}.")
            ventana_principal(username)  # Abre la ventana principal
        else:
            messagebox.showerror("Monto insuficiente", "El monto debe ser al menos $80,000.")

# Función para alquilar maquinaria
def alquilar_maquinaria(maquinaria, dias, username):
    saldo_usuario = usuarios[username][1]  # Obtiene el saldo del usuario
    costo_diario = maquinarias[maquinaria]["precio"]  # Obtiene el precio diario de la maquinaria
    total = costo_diario * dias  # Calcula el costo total del alquiler
    if saldo_usuario >= total:  # Verifica si el usuario tiene saldo suficiente
        saldo_usuario -= total  # Resta el costo del saldo del usuario
        usuarios[username][1] = saldo_usuario  # Actualiza el saldo del usuario
        maquinarias[maquinaria]["disponible"] = False  # Marca la maquinaria como no disponible
        alquileres.append({
            "usuario": username,
            "maquinaria": maquinaria,
            "dias": dias,
            "costo": total
        })  # Agrega el alquiler al registro
        guardar_datos()  # Guarda los datos actualizados
        messagebox.showinfo("Alquiler Exitoso", f"Has arrendado una {maquinaria} por {dias} días.\nCosto total: ${total}. Saldo restante: ${saldo_usuario}.")
    else:
        messagebox.showerror("Saldo Insuficiente", "No tienes suficiente saldo para alquilar esta maquinaria.")

# Ventana Principal
def ventana_principal(username):
    ventana = tk.Tk()
    ventana.title("HeavyMachine - Alquiler de Maquinaria Pesada")
    ventana.config(bg=FONDO_COLOR)
    centrar_ventana(ventana)

    agregar_encabezado(ventana)

    saldo = usuarios[username][1]  # Obtiene el saldo del usuario
    label_saldo = tk.Label(ventana, text=f"Saldo disponible: ${saldo}", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_saldo.pack(pady=20)

    label_maquinaria = tk.Label(ventana, text="Elige una maquinaria para arrendar:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_maquinaria.pack(pady=10)

    def obtener_dias(maquinaria):
        if maquinarias[maquinaria]["disponible"]:
            dias = simpledialog.askinteger("Días de alquiler", "¿Cuántos días deseas alquilar?", minvalue=1)
            if dias:
                alquilar_maquinaria(maquinaria, dias, username)
                ventana.destroy()
                ventana_principal(username)
        else:
            messagebox.showerror("No disponible", f"La {maquinaria} ya no está disponible para alquiler.")

    for maquinaria in maquinarias:
        disponibilidad = "Disponible" if maquinarias[maquinaria]["disponible"] else "No disponible"
        texto = f"{maquinaria}\nPrecio: ${maquinarias[maquinaria]['precio']}\nEstado: {disponibilidad}"
        boton = tk.Button(ventana, text=texto, bg="white", fg="black", font=FUENTE_ESTILO, command=lambda m=maquinaria: obtener_dias(m))
        boton.pack(pady=10)

    ventana.mainloop()

# Ventana de inicio de sesión
def ventana_inicio_sesion():
    global entry_usuario, entry_contraseña, ventana_inicio
    ventana_inicio = tk.Tk()
    ventana_inicio.title("HeavyMachine - Iniciar sesión")
    ventana_inicio.config(bg=FONDO_COLOR)
    centrar_ventana(ventana_inicio)

    agregar_encabezado(ventana_inicio)

    label_usuario = tk.Label(ventana_inicio, text="Usuario:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_usuario.pack(pady=10)
    entry_usuario = tk.Entry(ventana_inicio)
    entry_usuario.pack(pady=10)

    label_contraseña = tk.Label(ventana_inicio, text="Contraseña:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_contraseña.pack(pady=10)
    entry_contraseña = tk.Entry(ventana_inicio, show="*")
    entry_contraseña.pack(pady=10)

    boton_iniciar = tk.Button(ventana_inicio, text="Iniciar sesión", bg="white", fg="black", font=FUENTE_ESTILO, command=iniciar_sesion)
    boton_iniciar.pack(pady=20)

    boton_registro = tk.Button(ventana_inicio, text="¿No tienes cuenta? Regístrate", bg="white", fg="black", font=FUENTE_ESTILO, command=lambda: [ventana_inicio.destroy(), ventana_registro()])
    boton_registro.pack(pady=10)

    ventana_inicio.mainloop()

# Ventana de registro
def ventana_registro():
    global entry_usuario, entry_contraseña, ventana_registro
    ventana_registro = tk.Tk()
    ventana_registro.title("HeavyMachine - Registro")
    ventana_registro.config(bg=FONDO_COLOR)
    centrar_ventana(ventana_registro)

    agregar_encabezado(ventana_registro)

    label_usuario = tk.Label(ventana_registro, text="Nuevo Usuario:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_usuario.pack(pady=10)
    entry_usuario = tk.Entry(ventana_registro)
    entry_usuario.pack(pady=10)

    label_contraseña = tk.Label(ventana_registro, text="Nueva Contraseña:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_contraseña.pack(pady=10)
    entry_contraseña = tk.Entry(ventana_registro, show="*")
    entry_contraseña.pack(pady=10)

    boton_registrar = tk.Button(ventana_registro, text="Registrar", bg="white", fg="black", font=FUENTE_ESTILO, command=registrar_usuario)
    boton_registrar.pack(pady=20)

# Funciones adicionales

# Función para borrar los datos almacenados
def borrar_datos():
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas borrar todos los datos almacenados?")
    if respuesta:
        global usuarios, alquileres
        usuarios = {}  # Reinicia el diccionario de usuarios
        alquileres = []  # Reinicia el registro de alquileres
        guardar_datos()  # Guarda los cambios
        messagebox.showinfo("Datos borrados", "Se han eliminado todos los datos almacenados.")
        ventana_inicio_sesion()  # Regresa a la ventana de inicio de sesión

# Función para cerrar sesión
def cerrar_sesion(ventana_actual):
    ventana_actual.destroy()  # Cierra la ventana actual
    ventana_inicio_sesion()  # Regresa a la ventana de inicio de sesión

# Ventana principal con funcionalidades adicionales
def ventana_principal(username):
    ventana = tk.Tk()
    ventana.title("HeavyMachine - Alquiler de Maquinaria Pesada")
    ventana.config(bg=FONDO_COLOR)
    centrar_ventana(ventana)

    agregar_encabezado(ventana)

    saldo = usuarios[username][1]  # Obtiene el saldo del usuario
    label_saldo = tk.Label(ventana, text=f"Saldo disponible: ${saldo}", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_saldo.pack(pady=20)

    label_maquinaria = tk.Label(ventana, text="Elige una maquinaria para arrendar:", bg=FONDO_COLOR, fg=TEXTO_COLOR, font=FUENTE_ESTILO)
    label_maquinaria.pack(pady=10)

    def obtener_dias(maquinaria):
        if maquinarias[maquinaria]["disponible"]:  # Verifica si la maquinaria está disponible
            dias = simpledialog.askinteger("Días de alquiler", "¿Cuántos días deseas alquilar?", minvalue=1)
            if dias:
                alquilar_maquinaria(maquinaria, dias, username)
                ventana.destroy()
                ventana_principal(username)
        else:
            messagebox.showerror("No disponible", f"La {maquinaria} ya no está disponible para alquiler.")

    for maquinaria in maquinarias:
        disponibilidad = "Disponible" if maquinarias[maquinaria]["disponible"] else "No disponible"
        texto = f"{maquinaria}\nPrecio: ${maquinarias[maquinaria]['precio']}\nEstado: {disponibilidad}"
        boton = tk.Button(ventana, text=texto, bg="white", fg="black", font=FUENTE_ESTILO, command=lambda m=maquinaria: obtener_dias(m))
        boton.pack(pady=10)
    # Botón para cerrar sesión 
    boton_cerrar_sesion = tk.Button(  # Crea un botón dentro de la ventana principal
        ventana,  # El botón será agregado a la ventana actual
        text="Cerrar sesión",  # Texto que aparecerá en el botón
        bg="darkblue",  # Color de fondo del botón
        fg="white",  # Color del texto del botón
        font=FUENTE_ESTILO,  # Estilo de fuente definido globalmente
        command=lambda: cerrar_sesion(ventana)  # Acción que se ejecutará al presionar el botón:
                                            # Llama a la función `cerrar_sesion` pasando la ventana actual como argumento
    )
    boton_cerrar_sesion.pack(pady=10)  # Ubica el botón en la ventana con un espacio vertical (padding) de 10 píxeles
    # Botón para cerrar sesión
    boton_borrar_datos = tk.Button(
        ventana,
        text="Borrar datos almacenados",
        bg="darkred",
        fg="white",
        font=FUENTE_ESTILO,
        command=lambda: [ventana.destroy(), borrar_datos()]
    )
    boton_borrar_datos.pack(pady=10)

    ventana.mainloop()
    ventana_registro.mainloop()

# Ejecutar aplicación
cargar_datos()
ventana_inicio_sesion()
