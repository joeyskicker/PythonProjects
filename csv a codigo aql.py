import tkinter as tk
from tkinter import filedialog
import pandas as pd
import customtkinter as ctk
import pyperclip  # Para manejar el portapapeles

#este programa crea mockdata de una lista de alguna base de datos cualquiera, sirve para testear cosas
#cuando se necesiten valores numéricos crea un nuevo archivo csv con una sola columna del rango de números

class CSVDataGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Generador de Datos CSV/SQL")
        self.geometry("800x600")

        # Variables para manejar los CSVs cargados y los ComboBoxes de columnas
        self.csv_files = []
        self.csv_data = []
        self.column_comboboxes = []

        # Crear el layout
        self.create_widgets()

    def create_widgets(self):
        # Crear los botones y campos de carga de CSV
        self.load_csv_buttons = []
        for i in range(10):  # Limitar a 10 botones de carga de CSV
            load_button = ctk.CTkButton(self, text=f"Cargar CSV {i + 1}", command=lambda i=i: self.load_csv(i))
            load_button.grid(row=i, column=0, padx=10, pady=5)
            self.load_csv_buttons.append(load_button)

            # ComboBox para seleccionar columnas
            column_combobox = ctk.CTkComboBox(self, values=["Numero al azar"])
            column_combobox.grid(row=i, column=1, padx=10, pady=5)
            self.column_comboboxes.append(column_combobox)

        # Crear los botones de generar CSV o SQL
        self.generate_csv_button = ctk.CTkButton(self, text="Agregar Texto a CSV", command=self.generate_csv)
        self.generate_csv_button.grid(row=10, column=0, padx=10, pady=5)

        self.generate_sql_button = ctk.CTkButton(self, text="Agregar Código SQL", command=self.generate_sql)
        self.generate_sql_button.grid(row=10, column=1, padx=10, pady=5)

        # Botón para copiar el contenido del TextBox
        self.copy_button = ctk.CTkButton(self, text="Copiar al Portapapeles", command=self.copy_to_clipboard)
        self.copy_button.grid(row=10, column=2, padx=10, pady=5)

        # Botón para limpiar el TextBox
        self.clear_button = ctk.CTkButton(self, text="Limpiar TextBox", command=self.clear_textbox)
        self.clear_button.grid(row=10, column=3, padx=10, pady=5)

        # Crear un TextBox grande con sliders
        self.output_textbox = ctk.CTkTextbox(self, width=600, height=250)
        self.output_textbox.grid(row=11, column=0, columnspan=4, padx=10, pady=5)

        # Añadir sliders al lado del TextBox
        self.v_scrollbar = ctk.CTkScrollbar(self, command=self.output_textbox.yview)
        self.v_scrollbar.grid(row=11, column=4, sticky='ns')
        self.output_textbox.configure(yscrollcommand=self.v_scrollbar.set)

    def load_csv(self, index):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filepath:
            csv_data = pd.read_csv(filepath)
            self.csv_files.append(filepath)
            self.csv_data.append(csv_data)

            # Mostrar las columnas disponibles en el archivo CSV
            print(f"Columnas del CSV {index + 1}: {csv_data.columns.tolist()}")

            # Actualizar el combo box con las columnas del archivo cargado
            self.column_comboboxes[index].configure(values=["Numero al azar"] + csv_data.columns.tolist())

    def generate_csv(self):
        result = "Valores en formato CSV:\n"
        for _ in range(20):
            row = []
            for csv_index, csv in enumerate(self.csv_data):
                column = self.column_comboboxes[csv_index].get()

                # Verificar si la columna existe antes de acceder a ella
                if column != "Numero al azar" and column in csv.columns:
                    row.append(str(csv[column].sample(1).values[0]))
                else:
                    row.append("Columna no encontrada o 'Numero al azar' seleccionado")
            result += ",".join(row) + "\n"

        # Mostrar el resultado en el TextBox
        self.output_textbox.delete(1.0, tk.END)
        self.output_textbox.insert(tk.END, result)

    def generate_sql(self):
        result = "Valores en formato SQL:\n"
        for _ in range(20):
            row = []
            for csv_index, csv in enumerate(self.csv_data):
                column = self.column_comboboxes[csv_index].get()

                # Verificar si la columna existe antes de acceder a ella
                if column != "Numero al azar" and column in csv.columns:
                    row.append(f"({str(csv[column].sample(1).values[0])})")
                else:
                    row.append("(NULL)")
            result += ",".join(row) + ",\n"

        # Mostrar el resultado en el TextBox
        self.output_textbox.delete(1.0, tk.END)
        self.output_textbox.insert(tk.END, result)

    def copy_to_clipboard(self):
        text = self.output_textbox.get(1.0, tk.END)
        pyperclip.copy(text.strip())  # Copiar el contenido al portapapeles

    def clear_textbox(self):
        self.output_textbox.delete(1.0, tk.END)  # Limpiar el TextBox


if __name__ == "__main__":
    app = CSVDataGeneratorApp()
    app.mainloop()
