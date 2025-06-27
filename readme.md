# AstroFovTool

AstroFovTool es una aplicación de escritorio en Python para astrónomos aficionados y profesionales, que facilita el cálculo del campo de visión (FoV) de cámaras astronómicas. Esto ayuda a planificar sesiones de astrofotografía y evaluar qué tan grande será el área capturada del cielo con distintas configuraciones de cámara y telescopio.

---

## Características principales

- Selección sencilla de configuraciones típicas de sensores astronómicos (marca, tipo, megapíxeles).
- Cálculo automático del campo de visión en grados y píxeles.
- Visualización gráfica del área fotografiable en un canvas.
- Modos de cálculo: tabla con focales estándar o focal fija personalizada.
- Guardado y gestión de objetos astronómicos con historial.
- Exportación del historial a Excel para análisis externo.
- Interfaz intuitiva basada en Tkinter, ligera y rápida.

---

## Requisitos

- Python 3.7 o superior
- Paquetes listados en `requirements.txt`

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/AstroFovTool.git
cd AstroFovTool
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

Windows:

```bash
python -m venv env
.\env\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv env
source env/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

# USO

Ejecuta la aplicación desde la carpeta raíz:

```bash
python src/main.py
```

# Cómo usar

Selecciona la configuración de tu cámara (marca, tipo y megapíxeles).

Ingresa las dimensiones del DSO en grados, minutos y segundos.

Elige modo tabla para usar focales estándar o modo fija para focal personalizada.

Haz clic en Calcular para obtener el campo de visión y píxeles correspondientes.

Visualiza los resultados y el área en el canvas.

Guarda objetos con nombre y configuración para tu historial.

Usa el historial para revisar objetos guardados y exportarlos a Excel.