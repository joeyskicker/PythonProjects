import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from sklearn.impute import KNNImputer


# Función para cargar un archivo CSV
def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return None
    try:
        df = pd.read_csv(file_path)
        return df, file_path
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
        return None, None


# Función para verificar valores faltantes
def check_missing_data(df):
    if df.isna().any().any():
        return True
    else:
        return False


# Imputar datos con diferentes métodos
def impute_data(df, method, file_path, output_list, textbox):
    imputados = df.copy()
    missing_indices = imputados[imputados.isna().any(axis=1)].index.tolist()
    missing_columns = imputados.columns[imputados.isna().any()].tolist()
    details = []

    if method == "media" or method == "mediana":
        # Seleccionar solo columnas numéricas
        numeric_cols = imputados.select_dtypes(include=["number"]).columns
        if method == "media":
            imputados[numeric_cols] = imputados[numeric_cols].fillna(imputados[numeric_cols].mean())
        elif method == "mediana":
            imputados[numeric_cols] = imputados[numeric_cols].fillna(imputados[numeric_cols].median())
    elif method == "moda":
        # Imputar con la moda
        for col in imputados.columns:
            if imputados[col].dtype == "object":  # Categóricas o textuales
                mode_value = imputados[col].mode()[0]  # Moda (más frecuente)
                imputados[col] = imputados[col].fillna(mode_value)
            else:  # Para columnas numéricas
                mode_value = imputados[col].mode()[0]
                imputados[col] = imputados[col].fillna(mode_value)
    elif method == "knn":
        imputer = KNNImputer(n_neighbors=5)
        numeric_cols = imputados.select_dtypes(include=["number"]).columns
        imputados[numeric_cols] = imputer.fit_transform(imputados[numeric_cols])
    else:
        raise ValueError("Método de imputación no soportado.")

    # Registrar los valores imputados
    for row in missing_indices:
        for col in missing_columns:
            if pd.isna(df.at[row, col]):
                new_value = imputados.at[row, col]
                if pd.isna(new_value):
                    details.append(f"Fila: {row}, Columna: {col}, Valor Imputado: No se pudo imputar (NaN)")
                else:
                    details.append(f"Fila: {row}, Columna: {col}, Valor Imputado: {new_value}")

    # Guardar el archivo imputado
    output_file = file_path.replace(".csv", f"_{method}_imputado.csv")
    imputados.to_csv(output_file, index=False)
    messagebox.showinfo("Archivo guardado", f"Archivo guardado como: {output_file}")

    output_list.insert(tk.END, output_file)

    # Mostrar los detalles
    textbox.delete("1.0", tk.END)
    if details:
        textbox.insert(tk.END, f"Detalles de imputación para el método '{method}':\n\n")
        for detail in details:
            textbox.insert(tk.END, detail + "\n")
    else:
        textbox.insert(tk.END, "No se realizaron imputaciones.\n")

def main():
    root = tk.Tk()
    root.title("Imputación de Datos")
    root.geometry("700x500")

    df = None
    file_path = None
    file_label = tk.Label(root, text="", fg="blue")

    # Mostrar archivos generados
    output_list_label = tk.Label(root, text="Archivos generados:", fg="black")
    output_list = tk.Listbox(root, height=5, width=100)

    # Cuadro de texto para mostrar los detalles de imputación
    textbox_label = tk.Label(root, text="Detalles de imputación:", fg="black")
    textbox_frame = tk.Frame(root)
    textbox = tk.Text(textbox_frame, height=15, width=100, wrap="word")
    scrollbar = ttk.Scrollbar(textbox_frame, orient="vertical", command=textbox.yview)
    textbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    textbox.pack(side="left", fill="both", expand=True)

    def load_data():
        nonlocal df, file_path
        df, file_path = load_csv()
        if df is not None:
            if check_missing_data(df):
                file_label.config(text=f"Archivo con datos faltantes: \n{file_path.split('/')[-1]}")
                file_label.pack(pady=10)
                buttons_frame.pack(pady=10)
            else:
                messagebox.showinfo("Datos completos", "El archivo no tiene valores faltantes.")
                file_label.config(text="")
                buttons_frame.pack_forget()

    def impute_and_save(method):
        if df is not None and file_path is not None:
            impute_data(df, method, file_path, output_list, textbox)

    buttons_frame = tk.Frame(root)
    tk.Button(buttons_frame, text="Cargar CSV", command=load_data).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Imputar con Media", command=lambda: impute_and_save("media")).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Imputar con Mediana", command=lambda: impute_and_save("mediana")).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Imputar con KNN", command=lambda: impute_and_save("knn")).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Imputar con Moda", command=lambda: impute_and_save("moda")).pack(side="left", padx=5)

    # Colocar los elementos en la ventana
    file_label.pack(pady=10)
    buttons_frame.pack(pady=10)
    output_list_label.pack(pady=10)
    output_list.pack(pady=10)
    textbox_label.pack(pady=10)
    textbox_frame.pack(pady=10, fill="both", expand=True)

    def show_generated_files():
        generated_files = "\n".join(output_list.get(0, tk.END))
        messagebox.showinfo("Archivos Generados", f"Los archivos generados son:\n{generated_files}")

    # Mostrar archivos generados
    tk.Button(root, text="Ver Archivos Generados", command=show_generated_files).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
