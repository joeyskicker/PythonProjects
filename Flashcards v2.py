import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcards con Excel")
        self.root.geometry("800x600")

        self.df = None
        self.current_index = 0
        self.pregunta_count = {}
        self.palabras_aprendidas = 0

        # Botón para cargar Excel
        self.btn_cargar = tk.Button(root, text="Cargar Excel", command=self.cargar_excel)
        self.btn_cargar.pack(pady=10)

        # Contador X/Y
        self.label_progress = tk.Label(root, text="0/0 - Palabras aprendidas", font=("Arial", 20))
        self.label_progress.pack(pady=10)

        # Pregunta
        self.label_pregunta = tk.Label(root, text="", font=("Arial", 24), wraplength=700)
        self.label_pregunta.pack(pady=10)

        # Respuestas
        self.frame_respuestas = tk.Frame(root)
        self.frame_respuestas.pack(pady=10)

        self.botones_respuesta = []
        for i in range(4):
            btn = tk.Button(self.frame_respuestas, text="", font=("Arial", 18), width=40, height=2, command=lambda b=i: self.verificar_respuesta(b))
            btn.pack(pady=5)
            self.botones_respuesta.append(btn)

        # Resultado
        self.label_resultado = tk.Label(root, text="", font=("Arial", 18), fg="green")
        self.label_resultado.pack(pady=20)

    def cargar_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if not archivo:
            return

        try:
            self.df = pd.read_excel(archivo, engine='openpyxl')
            self.df.dropna(inplace=True)
            self.total = len(self.df)
            self.pregunta_count = {}
            self.palabras_aprendidas = 0
            self.label_progress.config(text=f"{self.palabras_aprendidas}/{self.total} - Palabras aprendidas")
            self.siguiente_pregunta()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

    def siguiente_pregunta(self):
        # Seleccionar una palabra que no ha sido aprendida aún
        disponibles = [i for i in range(self.total) if self.pregunta_count.get(i, 0) < 5]
        if not disponibles:
            self.label_pregunta.config(text="¡Has aprendido todas las palabras!")
            for btn in self.botones_respuesta:
                btn.config(text="", state="disabled")
            return

        self.current_index = random.choice(disponibles)
        pregunta = str(self.df.iloc[self.current_index, 0])
        self.respuesta_correcta = str(self.df.iloc[self.current_index, 1])

        # Seleccionar respuestas incorrectas
        todas_respuestas = self.df.iloc[:, 1].tolist()
        incorrectas = list(set(todas_respuestas) - {self.respuesta_correcta})
        opciones = random.sample(incorrectas, k=min(3, len(incorrectas)))
        opciones.append(self.respuesta_correcta)
        random.shuffle(opciones)

        self.label_pregunta.config(text=pregunta)
        for i, btn in enumerate(self.botones_respuesta):
            btn.config(text=opciones[i], state="normal")

    def verificar_respuesta(self, index):
        seleccion = self.botones_respuesta[index].cget("text")
        if seleccion == self.respuesta_correcta:
            # Solo incrementamos si es correcta
            self.pregunta_count[self.current_index] = self.pregunta_count.get(self.current_index, 0) + 1

            if self.pregunta_count[self.current_index] == 5:
                self.palabras_aprendidas += 1

            self.label_progress.config(
                text=f"{self.palabras_aprendidas}/{self.total} - Palabras aprendidas"
            )
            self.mostrar_resultado(f"Correcto: {self.label_pregunta.cget('text')} - {self.respuesta_correcta}", True)
            self.siguiente_pregunta()
        else:
            self.mostrar_resultado("Incorrecto", False)

    def mostrar_resultado(self, mensaje, correcto):
        self.label_resultado.config(text=mensaje, fg="green" if correcto else "red")
        self.root.after(5000, lambda: self.label_resultado.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
