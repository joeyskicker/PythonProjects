import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class ExcelToSQLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Excel a SQL")
        self.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        # Botón para seleccionar archivo Excel
        self.select_button = tk.Button(self, text="Seleccionar Archivo Excel\n Nombres de las hojas son importantes", command=self.select_excel)
        self.select_button.pack(pady=20)

        # Etiqueta para mostrar el archivo seleccionado
        self.file_label = tk.Label(self, text="")
        self.file_label.pack()

    def select_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.file_label.config(text=f"Archivo seleccionado:\n{os.path.basename(file_path)}")
            try:
                self.process_excel(file_path)
                messagebox.showinfo("Éxito", f"Archivo SQL generado:\n{os.path.splitext(file_path)[0]}.sql")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo.\n{str(e)}")

    def process_excel(self, file_path):
        sql_output = ""
        # Leer el archivo Excel
        excel_data = pd.ExcelFile(file_path)

        for sheet_name in excel_data.sheet_names:
            df = pd.read_excel(excel_data, sheet_name=sheet_name)

            # Identificar columnas, PK y FK
            columns = []
            primary_keys = []
            foreign_keys = []

            for col in df.columns:
                if "(PK)" in col:
                    clean_col = col.replace("(PK)", "").strip()
                    primary_keys.append(clean_col)
                    columns.append(clean_col)
                elif "(FK)" in col:
                    clean_col = col.replace("(FK)", "").strip()
                    foreign_keys.append(clean_col)
                    columns.append(clean_col)
                else:
                    columns.append(col.strip())

            # Crear declaración CREATE TABLE
            table_name = sheet_name
            sql_output += f"CREATE TABLE {table_name} (\n"
            sql_output += ",\n".join([f"  {col} TEXT" for col in columns])  # TEXT como tipo de datos genérico
            if primary_keys:
                sql_output += f",\n  PRIMARY KEY ({', '.join(primary_keys)})"
            if foreign_keys:
                for fk in foreign_keys:
                    sql_output += f",\n  FOREIGN KEY ({fk}) REFERENCES otro_tabla({fk})"  # Modificar según tu esquema
            sql_output += "\n);\n\n"

            # Crear declaraciones INSERT INTO
            for _, row in df.iterrows():
                values = [f"'{str(row[col])}'" for col in columns]
                sql_output += f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
            sql_output += "\n"

        # Guardar el archivo SQL
        sql_file_path = os.path.splitext(file_path)[0] + ".sql"
        with open(sql_file_path, "w", encoding="utf-8") as sql_file:
            sql_file.write(sql_output)


if __name__ == "__main__":
    app = ExcelToSQLApp()
    app.mainloop()
