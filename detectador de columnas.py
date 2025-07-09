import pandas as pd
from tkinter import filedialog, Tk
import os


def detect_keys(column_names):
    """
    Identifica claves primarias (PK) y foráneas (FK) en los nombres de columnas.
    Retorna dos listas: primary_keys y foreign_keys.
    """
    primary_keys = []
    foreign_keys = []

    for column in column_names:
        if "(PK)" in column:
            primary_keys.append(column.replace("(PK)", "").strip())
        elif "(FK)" in column:
            foreign_keys.append(column.replace("(FK)", "").strip())

    return primary_keys, foreign_keys


def excel_to_sql(filepath):
    """
    Procesa un archivo de Excel y genera un archivo SQL.
    """
    output_sql = []
    try:
        # Cargar todas las hojas del Excel
        excel_data = pd.ExcelFile(filepath)

        for sheet_name in excel_data.sheet_names:
            try:
                # Leer cada hoja como DataFrame
                df = excel_data.parse(sheet_name)

                # Obtener nombres de columnas
                column_names = df.columns.tolist()
                primary_keys, foreign_keys = detect_keys(column_names)

                # Limpiar los nombres de columnas
                clean_column_names = [col.replace("(PK)", "").replace("(FK)", "").strip() for col in column_names]

                # Crear sentencia CREATE TABLE
                table_name = sheet_name
                create_table = f"CREATE TABLE {table_name} (\n"
                columns = []

                for col in column_names:
                    column_def = col.replace("(PK)", "").replace("(FK)", "").strip()
                    if "(PK)" in col:
                        column_def += " PRIMARY KEY"
                    elif "(FK)" in col:
                        column_def += " FOREIGN KEY"
                    columns.append(column_def)

                create_table += ",\n".join(f"  {col} VARCHAR(255)" for col in columns)
                create_table += "\n);"
                output_sql.append(create_table)

                # Insertar datos
                for _, row in df.iterrows():
                    values = "', '".join(map(str, row.tolist()))
                    insert_statement = f"INSERT INTO {table_name} ({', '.join(clean_column_names)}) VALUES ('{values}');"
                    output_sql.append(insert_statement)

            except Exception as e:
                print(f"Error procesando la hoja '{sheet_name}': {e}")

        # Escribir a archivo SQL
        output_filepath = os.path.splitext(filepath)[0] + ".sql"
        with open(output_filepath, "w", encoding="utf-8") as file:
            file.write("\n\n".join(output_sql))

        print(f"Archivo SQL generado exitosamente en: {output_filepath}")

    except Exception as e:
        print(f"Error procesando el archivo Excel: {e}")


def main():
    """
    GUI simple para seleccionar un archivo Excel.
    """
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal

    filepath = filedialog.askopenfilename(
        title="Seleccione un archivo Excel",
        filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
    )

    if filepath:
        print(f"Archivo seleccionado: {filepath}")
        excel_to_sql(filepath)
    else:
        print("No se seleccionó ningún archivo.")


if __name__ == "__main__":
    main()
