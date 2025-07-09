import tkinter as tk
from tkinter import filedialog, messagebox
import os
import csv


def limpiar_linea(linea):
    original = linea
    # Correcciones simples
    linea = linea.replace('\"', '')  # elimina comillas dobles
    linea = linea.replace(',', ' ')  # cambia comas por punto y coma

    if original != linea:
        return linea, f"Original: {original.strip()}\nLimpio: {linea.strip()}\n"
    else:
        return linea, None


def limpiar_csv(ruta_archivo):
    cambios = []
    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    ruta_salida = os.path.join(os.path.dirname(ruta_archivo), nombre_base + "_limpio.csv")

    with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as entrada, \
            open(ruta_salida, "w", newline='', encoding="utf-8") as salida:

        lector = csv.reader(entrada)
        escritor = csv.writer(salida)

        for fila in lector:
            fila_limpia = []
            for campo in fila:
                limpio, cambio = limpiar_linea(campo)
                fila_limpia.append(limpio)
                if cambio:
                    cambios.append(cambio)
            escritor.writerow(fila_limpia)

    return cambios, ruta_salida


def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if archivo:
        entrada.set(archivo)


def procesar_archivo():
    ruta = entrada.get()
    if not ruta:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo.")
        return

    cambios, salida = limpiar_csv(ruta)
    messagebox.showinfo("Proceso completado", f"Archivo limpio guardado en:\n{salida}")
    texto_cambios.delete(1.0, tk.END)
    if cambios:
        texto_cambios.insert(tk.END, "".join(cambios))
    else:
        texto_cambios.insert(tk.END, "No se realizaron cambios.")


# GUI
ventana = tk.Tk()
ventana.title("Limpieza de CSV")
ventana.geometry("1000x600")  # Aumentar tamaño de la ventana

entrada = tk.StringVar()

tk.Label(ventana, text="Archivo CSV:").pack(pady=5)
tk.Entry(ventana, textvariable=entrada, width=80).pack()
tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack(pady=5)
tk.Button(ventana, text="Limpiar y Guardar", command=procesar_archivo).pack(pady=5)

tk.Label(ventana, text="Cambios realizados:").pack(pady=5)

# Frame para text y scrollbar
frame_texto = tk.Frame(ventana)
frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

texto_cambios = tk.Text(frame_texto, height=25, width=120, yscrollcommand=scrollbar.set)
texto_cambios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=texto_cambios.yview)

ventana.mainloop()
