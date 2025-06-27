# Changelog

Todas las versiones importantes de AstroFovTool documentadas aquí.

## [1.2.1] - 2025-06-26

### Corregido
- Se resolvió un error crítico donde la tabla de resultados mostraba entradas duplicadas indefinidamente.
- Corregido `IndexError` al hacer clic sobre un resultado inválido o fuera de rango en el Treeview.
- Se corrigió un fallo que permitía guardar datos sin haber hecho ningún cálculo previo.

### Añadido
- Validación para que no se pueda calcular si no se ha seleccionado una configuración de cámara.
- Validación para evitar guardar objetos si los tamaños son cero o inválidos.
- Advertencias visuales (messagebox) claras para entradas incompletas o inválidas.

### Mejorado
- Ahora el botón de guardar se desactiva automáticamente si se cambia a modo “fija”.
- Refactorización general de las funciones para hacer el flujo de validación más robusto.
- La interfaz de historial ahora incluye una barra de desplazamiento vertical para mejorar la navegación.

---

## [1.2.0] - 2025-06-21

### Añadido
- Implementación del historial de objetos guardados.
- Funcionalidad para exportar el historial a archivo Excel (.xlsx).
- Nuevas etiquetas de color en la tabla de resultados: verde (fotografiable) y rojo (no fotografiable).

### Mejorado
- Organización visual del historial para mostrar la cámara utilizada junto con cada objeto.
- Separación clara entre bloques de objetos guardados.
- Interfaz de entrada mejorada para mayor fluidez al rellenar los valores de ancho y alto del objeto.

---

## [1.1.0] - 2025-06-15

### Añadido
- Cálculo automático del tamaño en píxeles que ocupará un objeto celeste en el sensor, según su tamaño angular y la distancia focal.
- Detección automática de si un objeto es completamente fotografiable en el sensor seleccionado.

---

## [1.0.0] - 2025-06-01

### Añadido
- Primera versión funcional de AstroFovTool.
- Interfaz gráfica en Tkinter para ingresar tamaños y focales.
- Tabla de resultados generada automáticamente según configuración.

---

