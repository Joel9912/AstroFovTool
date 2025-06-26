# utils.py

import os
import csv
from pathlib import Path
from tkinter import messagebox
import openpyxl
from openpyxl.utils import get_column_letter

# Ruta de salida por defecto (ajustable desde afuera si se quiere)
ARCHIVO_SALIDA = Path(__file__).resolve().parent.parent / "historial" / "objetos guardados.csv"
ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

def guardar_objeto_en_csv(nombre, deg_x, deg_y, resultados):
    filas_guardadas = []
    if os.path.exists(ARCHIVO_SALIDA):
        with open(ARCHIVO_SALIDA, newline="") as f:
            reader = csv.reader(f)
            filas_guardadas = list(reader)

    # Verificar si ya existe ese nombre
    nombre_existente = any(fila and fila[0].strip() == nombre for fila in filas_guardadas if fila)

    if nombre_existente:
        sobrescribir = messagebox.askyesno("Objeto ya guardado",
                                           f"Ya existe un objeto llamado '{nombre}'.\n¿Desea sobrescribirlo?")
        if not sobrescribir:
            return False

        # Eliminar el bloque anterior
        nuevas_filas_guardadas = []
        i = 0
        while i < len(filas_guardadas):
            fila = filas_guardadas[i]
            if fila and fila[0].strip() == nombre:
                i += 1
                while i < len(filas_guardadas) and filas_guardadas[i] and filas_guardadas[i][0].strip() != "":
                    i += 1
                if i < len(filas_guardadas) and (
                        not filas_guardadas[i] or all(c.strip() == "" for c in filas_guardadas[i])):
                    i += 1
            else:
                nuevas_filas_guardadas.append(fila)
                i += 1
        filas_guardadas = nuevas_filas_guardadas

    nuevas_filas = []
    for res in resultados:
        nuevas_filas.append([
            nombre,
            f"{deg_x:.6f}",
            f"{deg_y:.6f}",
            f"{res['f']}mm",
            f"{res['px_x']:.1f}",
            f"{res['px_y']:.1f}",
            f"{res['total']:.0f}",
            f"{res['porcentaje']:.3f}",
            "Sí" if res['fotografiable'] else "No"
        ])
    nuevas_filas.append([])

    with open(str(ARCHIVO_SALIDA), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(filas_guardadas + nuevas_filas)
    return True

def leer_historial():
    if not os.path.exists(ARCHIVO_SALIDA):
        return []
    with open(ARCHIVO_SALIDA, newline="") as f:
        reader = csv.reader(f)
        return list(reader)

def exportar_excel_desde_csv():
    if not os.path.exists(ARCHIVO_SALIDA):
        messagebox.showerror("Error", "No hay datos para exportar.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial DSO"

    headers = ["Nombre", "Ancho (°)", "Alto (°)", "Focal", "Px X", "Px Y", "Total px", "% Sensor", "¿Fotografiable?"]
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)

    with open(ARCHIVO_SALIDA, newline="") as f:
        reader = csv.reader(f)
        for row_idx, fila in enumerate(reader, start=2):
            for col_idx, valor in enumerate(fila, start=1):
                ws.cell(row=row_idx, column=col_idx, value=valor)

    for i in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 16

    ruta_excel = str(ARCHIVO_SALIDA).replace(".csv", ".xlsx")
    wb.save(ruta_excel)
    messagebox.showinfo("Éxito", f"Historial exportado a:\n{ruta_excel}")
