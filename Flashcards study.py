import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcards con Excel")
        self.root.geometry("800x600")  # Tamaño más grande

        self.df = None
        self.current_index = 0
        self.used_indexes = set()
        self.pregunta_count = {}  # Diccionario para contar repeticiones
        self.palabras_aprendidas = 0  # Contador de palabras aprendidas

        # Cargar archivo Excel
        self.btn_cargar = tk.Button(root, text="Cargar Excel", command=self.cargar_excel)
        self.btn_cargar.pack(pady=10)

        # Progreso
        self.label_progress = tk.Label(root, text="0/0", font=("Arial", 20))
        self.label_progress.pack(pady=10)

        # Pregunta
        self.label_pregunta = tk.Label(root, text="", font=("Arial", 24), wraplength=700)
        self.label_pregunta.pack(pady=10)

        # Respuestas
        self.frame_respuestas = tk.Frame(root)
        self.frame_respuestas.pack(pady=10)

        self.botones_respuesta = []
        for _ in range(4):
            btn = tk.Button(self.frame_respuestas, text="", font=("Arial", 18), width=40, height=2, command=lambda b=_: self.verificar_respuesta(b))
            btn.pack(pady=5)
            self.botones_respuesta.append(btn)

        # Mensaje de respuesta
        self.label_resultado = tk.Label(root, text="", font=("Arial", 18), fg="green")
        self.label_resultado.pack(pady=20)

        # Palabras aprendidas
        self.label_palabras_aprendidas = tk.Label(root, text="Palabras Aprendidas: 0", font=("Arial", 16))
        self.label_palabras_aprendidas.pack(pady=10)

    def cargar_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if not archivo:
            return

        try:
            self.df = pd.read_excel(archivo, engine='openpyxl')
            self.df.dropna(inplace=True)
            self.total = len(self.df)
            self.usadas = 0
            self.used_indexes.clear()
            self.pregunta_count.clear()  # Reiniciar contadores
            self.palabras_aprendidas = 0  # Reiniciar palabras aprendidas
            self.label_progress.config(text=f"{self.usadas}/{self.total}")
            self.label_palabras_aprendidas.config(text=f"Palabras Aprendidas: {self.palabras_aprendidas}")
            self.siguiente_pregunta()
        except Exception as e:
            self.mostrar_resultado("Error al cargar el archivo", is_correct=False)

    def siguiente_pregunta(self):
        if self.usadas >= self.total:
            self.mostrar_resultado("¡Completado! Has respondido todas las preguntas.", is_correct=False)
            self.label_pregunta.config(text="")
            for btn in self.botones_respuesta:
                btn.config(text="", state="disabled")
            return

        # Elegir una fila que no haya sido usada o que se repita menos de 5 veces
        while True:
            self.current_index = random.randint(0, self.total - 1)
            if self.current_index not in self.used_indexes or self.pregunta_count.get(self.current_index, 0) < 5:
                break

        self.used_indexes.add(self.current_index)
        pregunta = str(self.df.iloc[self.current_index, 0])
        respuesta_correcta = str(self.df.iloc[self.current_index, 1])

        # Actualizar contador de repeticiones
        if self.current_index not in self.pregunta_count:
            self.pregunta_count[self.current_index] = 1
        else:
            self.pregunta_count[self.current_index] += 1

        # Obtener 3 respuestas incorrectas
        posibles = self.df.iloc[:, 1].drop(self.current_index).unique().tolist()
        respuestas_incorrectas = random.sample(posibles, k=3) if len(posibles) >= 3 else posibles

        opciones = respuestas_incorrectas + [respuesta_correcta]
        random.shuffle(opciones)

        self.label_pregunta.config(text=pregunta)
        self.respuesta_correcta = respuesta_correcta

        for i, btn in enumerate(self.botones_respuesta):
            if i < len(opciones):
                btn.config(text=opciones[i], state="normal")
            else:
                btn.config(text="", state="disabled")

    def verificar_respuesta(self, index):
        respuesta_elegida = self.botones_respuesta[index].cget("text")
        if respuesta_elegida == self.respuesta_correcta:
            self.usadas += 1
            self.palabras_aprendidas += 1 if self.pregunta_count[self.current_index] == 5 else 0  # Incrementar si es la 5ta respuesta correcta
            self.label_progress.config(text=f"{self.usadas}/{self.total}")
            self.label_palabras_aprendidas.config(text=f"Palabras Aprendidas: {self.palabras_aprendidas}")
            self.mostrar_resultado(f"Correcto: {self.label_pregunta.cget('text')} - {self.respuesta_correcta}", is_correct=True)
            self.siguiente_pregunta()
        else:
            self.mostrar_resultado("Incorrecto", is_correct=False)

    def mostrar_resultado(self, mensaje, is_correct):
        """Mostrar si la respuesta es correcta o incorrecta en el label"""
        self.label_resultado.config(text=mensaje, fg="green" if is_correct else "red")
        # Ocultar el mensaje después de 5 segundos
        self.root.after(5000, lambda: self.label_resultado.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
