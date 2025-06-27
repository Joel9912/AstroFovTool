# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from datos import (
    FOCALES_ESTANDAR, RESOLUCIONES_TIPICAS,
    CANVAS_WIDTH, CANVAS_HEIGHT, dms_a_grados, calcular_fov_en_px,
    actualizar_sensor_actual
)
from utils import guardar_objeto_en_csv, leer_historial, exportar_excel_desde_csv


class AstroFovToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AstroFovTool")
        self.geometry("800x600")
        self.modo = tk.StringVar(value="tabla")
        self.crear_widgets()
        self.actualizar_estado_guardado()
        self.resultados = []

    def crear_widgets(self):
        frame_izq = ttk.Frame(self)
        frame_der = ttk.Frame(self, width=500)
        frame_izq.pack(side="left", fill="y", padx=10, pady=10)
        frame_der.pack(side="left", fill="both", padx=10, pady=10)

        # Selector de sensor
        frame_sensor_select = ttk.LabelFrame(frame_izq, text="Seleccionar cámara")
        frame_sensor_select.pack(fill="x", pady=5)

        self.marca_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.mp_var = tk.StringVar()

        ttk.Label(frame_sensor_select, text="Marca:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.combo_marca = ttk.Combobox(frame_sensor_select, textvariable=self.marca_var, state="readonly")
        self.combo_marca["values"] = list(RESOLUCIONES_TIPICAS.keys())
        self.combo_marca.grid(row=0, column=1, padx=5, pady=2)
        self.combo_marca.bind("<<ComboboxSelected>>", self.actualizar_tipos)

        ttk.Label(frame_sensor_select, text="Tipo:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.combo_tipo = ttk.Combobox(frame_sensor_select, textvariable=self.tipo_var, state="readonly")
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=2)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_megapixeles)

        ttk.Label(frame_sensor_select, text="MP:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.combo_mp = ttk.Combobox(frame_sensor_select, textvariable=self.mp_var, state="readonly")
        self.combo_mp.grid(row=2, column=1, padx=5, pady=2)
        self.combo_mp.bind("<<ComboboxSelected>>", lambda event: self.aplicar_config_sensor(mostrar_mensaje=False))

        # Panel de información del sensor
        self.frame_sensor_info = ttk.LabelFrame(frame_izq, text="Información del sensor")
        self.frame_sensor_info.pack(fill="x", pady=5)

        from datos import SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM, RES_X, RES_Y, PIXEL_SIZE_X, PIXEL_SIZE_Y
        self.label_tam_sensor = ttk.Label(self.frame_sensor_info,
                                          text=f"Tamaño sensor: {SENSOR_WIDTH_MM:.1f} mm x {SENSOR_HEIGHT_MM:.1f} mm")
        self.label_tam_sensor.pack(anchor="w", padx=10, pady=2)

        self.label_res_sensor = ttk.Label(self.frame_sensor_info, text=f"Resolución sensor: {RES_X} px x {RES_Y} px")
        self.label_res_sensor.pack(anchor="w", padx=10, pady=2)

        self.label_px_sensor = ttk.Label(self.frame_sensor_info,
                                         text=f"Tamaño pixel: {PIXEL_SIZE_X * 1000:.3f} µm x {PIXEL_SIZE_Y * 1000:.3f} µm")
        self.label_px_sensor.pack(anchor="w", padx=10, pady=2)

        # Resto de interfaz
        frame_objeto = ttk.LabelFrame(frame_izq, text="Tamaño del objeto en cielo (DSO)")
        frame_objeto.pack(fill="x", pady=5)
        self.entries = {}

        ttk.Label(frame_objeto, text="Nombre del objeto:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.nombre_objeto = tk.Entry(frame_objeto)
        self.nombre_objeto.grid(row=2, column=1, columnspan=6, sticky="we")

        for i, label_text in enumerate(["Ancho:", "Alto:"]):
            ttk.Label(frame_objeto, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.entries[i] = []

            for j, simbolo in enumerate(["°", "'", "\""]):
                entry = tk.Entry(frame_objeto, width=4)
                entry.grid(row=i, column=1 + j * 2, padx=1)
                self.entries[i].append(entry)
                entry.bind("<Left>", lambda e, i=i, j=j: self.mover_entre_entradas(e, i, j))
                entry.bind("<Right>", lambda e, i=i, j=j: self.mover_entre_entradas(e, i, j))
                ttk.Label(frame_objeto, text=simbolo).grid(row=i, column=2 + j * 2, sticky="w", padx=(0, 5))

        frame_focal = ttk.LabelFrame(frame_izq, text="Configuración")
        frame_focal.pack(fill="x", pady=5)
        ttk.Radiobutton(frame_focal, text="Modo tabla (focales estándar)", variable=self.modo, value="tabla").pack(anchor="w")
        ttk.Radiobutton(frame_focal, text="Modo focal fija", variable=self.modo, value="fija").pack(anchor="w")

        self.focal_entry = tk.Entry(frame_focal)
        self.focal_entry.pack(anchor="w", padx=20)
        self.focal_entry.insert(0, "50")

        self.boton_calcular = ttk.Button(frame_izq, text="Calcular", command=self.mostrar_resultados)
        self.boton_calcular.pack(pady=10)

        self.boton_guardar = ttk.Button(frame_izq, text="Guardar objeto", command=self.guardar_objeto)
        self.boton_guardar.pack(pady=5)
        ttk.Button(frame_izq, text="Ver historial", command=self.ver_historial).pack(pady=5)

        self.tree = ttk.Treeview(frame_der, columns=("Focal", "Px X", "Px Y", "Total Px", "% Sensor"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(frame_der, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack(pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.tree.tag_configure("verde", background="lightgreen")
        self.tree.tag_configure("rojo", background="lightcoral")


    def actualizar_tipos(self, event=None):
        marca = self.marca_var.get()
        if marca:
            tipos = list(RESOLUCIONES_TIPICAS[marca].keys())
            self.combo_tipo["values"] = tipos
            self.combo_tipo.set("")
            self.combo_mp.set("")
            self.combo_mp["values"] = []

    def actualizar_megapixeles(self, event=None):
        marca = self.marca_var.get()
        tipo = self.tipo_var.get()
        if marca and tipo:
            mp_values = [
                mp for mp, res in RESOLUCIONES_TIPICAS[marca][tipo].items()
                if res is not None
            ]
            self.combo_mp["values"] = mp_values
            self.combo_mp.set("")

    def aplicar_config_sensor(self, mostrar_mensaje=True):
        marca = self.marca_var.get()
        tipo = self.tipo_var.get()
        mp = self.mp_var.get()

        if marca and tipo and mp:
            res = RESOLUCIONES_TIPICAS[marca][tipo].get(mp)
            if res:
                actualizar_sensor_actual(marca, tipo, mp)
                from datos import SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM, RES_X, RES_Y, PIXEL_SIZE_X, PIXEL_SIZE_Y

                # Actualizar etiquetas de info
                self.label_tam_sensor.config(
                    text=f"Tamaño sensor: {SENSOR_WIDTH_MM:.1f} mm x {SENSOR_HEIGHT_MM:.1f} mm")
                self.label_res_sensor.config(
                    text=f"Resolución sensor: {RES_X} px x {RES_Y} px")
                self.label_px_sensor.config(
                    text=f"Tamaño pixel: {PIXEL_SIZE_X * 1000:.3f} µm x {PIXEL_SIZE_Y * 1000:.3f} µm")

                if mostrar_mensaje:
                    messagebox.showinfo("Sensor actualizado", f"Nuevo sensor aplicado:\n{marca} {tipo} {mp}")
        self.resultados = []

    def actualizar_estado_guardado(self):
        self.boton_guardar.state(["!disabled"] if self.modo.get() == "tabla" else ["disabled"])
        self.modo.trace_add("write", lambda *args: self.actualizar_estado_guardado())

    def mover_entre_entradas(self, event, i, j):
        if event.keysym == "Right":
            if j < 2:
                self.entries[i][j + 1].focus()
            elif i == 0:
                self.entries[1][0].focus()
            else:
                self.nombre_objeto.focus()
        elif event.keysym == "Left":
            if j > 0:
                self.entries[i][j - 1].focus()
            elif i == 1:
                self.entries[0][2].focus()

    def mostrar_resultados(self):
        self.boton_calcular.config(state="normal")
        self.aplicar_config_sensor(mostrar_mensaje=False)

        marca = self.marca_var.get()
        tipo = self.tipo_var.get()
        mp = self.mp_var.get()
        if not (marca and tipo and mp):
            messagebox.showwarning("Configuración incompleta",
                                   "Seleccione una configuración de cámara antes de calcular.")
            return

        # 🔁 Importar valores actualizados después de aplicar sensor
        from datos import SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM, RES_X, RES_Y

        for row in self.tree.get_children():
            self.tree.delete(row)
        self.canvas.delete("all")

        deg_x = dms_a_grados(*[e.get() for e in self.entries[0]])
        deg_y = dms_a_grados(*[e.get() for e in self.entries[1]])
        if deg_x is None or deg_y is None:
            messagebox.showwarning("Entrada inválida", "Por favor, ingrese valores válidos para ancho y alto.")
            return
        if deg_x <= 0 or deg_y <= 0:
            messagebox.showwarning("Entrada inválida", "Los tamaños del objeto deben ser mayores a 0.")
            return

        self.resultados = []
        focales = FOCALES_ESTANDAR if self.modo.get() == "tabla" else [float(self.focal_entry.get())]
        for f in focales:
            px_x, px_y, total, pct, fot = calcular_fov_en_px(
                (deg_x, deg_y), f,
                SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM,
                RES_X, RES_Y
            )
            self.resultados.append({
                "f": f, "px_x": px_x, "px_y": px_y,
                "total": total, "porcentaje": pct, "fotografiable": fot
            })

        # SOLO UNA VEZ, no dentro del bucle anterior
        for res in self.resultados:
            tag = "verde" if res["fotografiable"] else "rojo"
            self.tree.insert("", "end",
                             values=(f"{res['f']}mm", f"{res['px_x']:.1f}", f"{res['px_y']:.1f}",
                                     f"{res['total']:.0f}", f"{res['porcentaje']:.3f} %"),
                             tags=(tag,))

            if self.modo.get() == "fija":
                self.dibujar_canvas(self.resultados[0])

    def on_row_select(self, event):
        if self.modo.get() != "tabla":
            return
        selected = self.tree.selection()
        if selected:
            idx = self.tree.index(selected[0])
            self.dibujar_canvas(self.resultados[idx])

    def dibujar_canvas(self, res):
        self.canvas.delete("all")
        escala_x = CANVAS_WIDTH / 6000  # valor base gen\u00e9rico
        escala_y = CANVAS_HEIGHT / 4000
        w = res["px_x"] * escala_x
        h = res["px_y"] * escala_y
        x0 = (CANVAS_WIDTH - w) / 2
        y0 = (CANVAS_HEIGHT - h) / 2
        x1 = x0 + w
        y1 = y0 + h
        color = "green" if res["fotografiable"] else "red"
        self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, outline="gray")
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=2)
        self.canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT + 10, anchor="n", text=f"{res['porcentaje']:.3f}% del sensor", fill=color, font=("Arial", 10))


    def guardar_objeto(self):
        if self.modo.get() != "tabla":
            messagebox.showwarning("Modo incorrecto", "Solo puede guardar en modo 'tabla'.")
            return

        if not self.resultados:
            messagebox.showwarning("Sin cálculos", "Debe calcular primero antes de guardar.")
            return

        nombre = self.nombre_objeto.get().strip()
        if not nombre:
            messagebox.showwarning("Nombre faltante", "Debe ingresar un nombre para el objeto.")
            return

        deg_x = dms_a_grados(*[e.get() for e in self.entries[0]])
        deg_y = dms_a_grados(*[e.get() for e in self.entries[1]])
        if deg_x is None or deg_y is None or deg_x <= 0 or deg_y <= 0:
            messagebox.showwarning("Tamaño inválido", "Los tamaños del objeto deben ser mayores a 0.")
            return

        marca = self.marca_var.get()
        tipo = self.tipo_var.get()
        mp = self.mp_var.get()
        if not all([marca, tipo, mp]):
            messagebox.showwarning("Falta configuración", "Seleccione la cámara utilizada antes de guardar.")
            return

        guardar_objeto_en_csv(self, nombre, deg_x, deg_y, self.resultados, marca, tipo, mp)
        messagebox.showinfo("Guardado", f"Objeto '{nombre}' guardado correctamente.")
    def ver_historial(self):
        datos = leer_historial()
        if not datos:
            messagebox.showinfo("Historial vacío", "No se han guardado objetos aún.")
            return

        popup = tk.Toplevel(self)
        popup.title("Historial de objetos guardados")
        popup.geometry("1100x500")

        columnas = ("Nombre/Marca", "° Ancho/Tipo", "° Alto/MP", "Focal", "Px X", "Px Y", "Total de Pixeles", "% del Sensor",
                    "¿Fotografiable?")

        tree_hist = ttk.Treeview(popup, columns=columnas, show="headings")
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=tree_hist.yview)
        tree_hist.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        for col in columnas:
            tree_hist.heading(col, text=col)
            tree_hist.column(col, width=100, anchor="center")
        tree_hist.pack(fill="both", expand=True, padx=10, pady=10)
        i = 0
        while i < len(datos):
            fila1 = datos[i] if i < len(datos) else []
            fila2 = datos[i + 1] if i + 1 < len(datos) else []
            i += 2
            if not fila1 or not fila2:
                continue

            nombre = fila1[0] if len(fila1) > 0 else ""
            deg_x = fila1[1] if len(fila1) > 1 else ""
            deg_y = fila1[2] if len(fila1) > 2 else ""
            marca = fila2[0] if len(fila2) > 0 else ""
            tipo = fila2[1] if len(fila2) > 1 else ""
            mp = fila2[2] if len(fila2) > 2 else ""

            # Insertar filas de resultados
            index_fila = 0
            while i < len(datos) and any(datos[i]):
                fila = datos[i]
                focal = fila[3] if len(fila) > 3 else ""
                px_x = fila[4] if len(fila) > 4 else ""
                px_y = fila[5] if len(fila) > 5 else ""
                total = fila[6] if len(fila) > 6 else ""
                pct = fila[7] if len(fila) > 7 else ""
                fotogra = fila[8] if len(fila) > 8 else ""

                if index_fila == 0:
                    tree_hist.insert("", "end", values=(
                        nombre, deg_x, deg_y, focal, px_x,
                        px_y, total, pct, fotogra
                    ))
                elif index_fila == 1:
                    tree_hist.insert("", "end", values=(
                        marca, tipo, mp, focal, px_x,
                        px_y, total, pct, fotogra
                    ))
                else:
                    tree_hist.insert("", "end", values=(
                        "", "", "", focal, px_x,
                        px_y, total, pct, fotogra
                    ))

                i += 1
                index_fila += 1

            # 3 filas en blanco para separar bloques
            for _ in range(3):
                tree_hist.insert("", "end", values=("", "", "", "", "", "", "", "", ""))

            # Saltar línea en blanco si la hay
            if i < len(datos) and not any(datos[i]):
                i += 1

        ttk.Button(popup, text="Exportar a Excel", command=exportar_excel_desde_csv).pack(pady=10)
