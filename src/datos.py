# datos.py
import math

# ========================
# CONFIGURACIÓN DEL SENSOR
# ========================
TIPOS_SENSOR = {
    "Canon Full-Frame": (36.0, 24.0),
    "Nikon Full-Frame": (35.9, 24.0),
    "Sony Full-Frame": (35.8, 23.9),
    "Canon APS-C": (22.3, 14.9),
    "Nikon APS-C": (23.5, 15.6),
    "Sony APS-C": (23.5, 15.6),
}

RESOLUCIONES_TIPICAS = {
    "Nikon": {
        "APS-C": {
            "12MP": (4288, 2848),
            "24MP": (6016, 4016)
        },
        "Full-Frame": {
            "12MP": (4256, 2832),
            "24MP": (6048, 4024),
            "45MP": (8256, 5504)
        }
    },
    "Canon": {
        "APS-C": {
            "12MP": (4272, 2848),
            "24MP": (6000, 4000)
        },
        "Full-Frame": {
            "12MP": None,
            "24MP": (6000, 4000),
            "45MP": (8192, 5464)
        }
    },
    "Sony": {
        "APS-C": {
            "12MP": (4272, 2848),
            "24MP": (6000, 4000)
        },
        "Full-Frame": {
            "12MP": (4240, 2832),
            "24MP": (6000, 4000),
            "61MP": (9504, 6336)
        }
    }
}

# ======================
# PARÁMETROS DE CÁLCULO
# ======================
FOCALES_ESTANDAR = [18, 24, 35, 50, 70, 85, 100, 150, 200, 300, 500, 650, 750, 900, 1000, 1250, 1500, 1800]
UMBRAL_PIXELES = 15000
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 200

# Variables globales iniciales (valores por defecto)
SENSOR_WIDTH_MM = 36.0
SENSOR_HEIGHT_MM = 24.0
RES_X = 6000
RES_Y = 4000
PIXEL_SIZE_X = SENSOR_WIDTH_MM / RES_X
PIXEL_SIZE_Y = SENSOR_HEIGHT_MM / RES_Y

# =======================
# FUNCIONES AUXILIARES
# =======================
def dms_a_grados(d, m, s):
    try:
        d_val = float(d) if d.strip() != "" else 0.0
        m_val = float(m) if m.strip() != "" else 0.0
        s_val = float(s) if s.strip() != "" else 0.0
        return abs(d_val) + m_val / 60 + s_val / 3600
    except:
        return None

def calcular_fov_en_px(obj_deg, focal, sensor_width_mm, sensor_height_mm, res_x, res_y):
    fov_sensor_x = (sensor_width_mm / focal) * (180 / math.pi)
    fov_sensor_y = (sensor_height_mm / focal) * (180 / math.pi)
    px_por_grado_x = res_x / fov_sensor_x
    px_por_grado_y = res_y / fov_sensor_y
    pixeles_x = obj_deg[0] * px_por_grado_x
    pixeles_y = obj_deg[1] * px_por_grado_y
    total_pixeles = pixeles_x * pixeles_y
    porcentaje = (total_pixeles / (res_x * res_y)) * 100
    fotografiable = total_pixeles >= UMBRAL_PIXELES
    return pixeles_x, pixeles_y, total_pixeles, porcentaje, fotografiable


def actualizar_sensor_actual(marca, tipo, mp):
    global SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM, RES_X, RES_Y, PIXEL_SIZE_X, PIXEL_SIZE_Y

    res = RESOLUCIONES_TIPICAS.get(marca, {}).get(tipo, {}).get(mp)
    if not res:
        raise ValueError(f"No se encontró resolución para {marca} {tipo} {mp}")

    if tipo == "APS-C":
        SENSOR_WIDTH_MM = 23.5
        SENSOR_HEIGHT_MM = 15.6
    else:
        SENSOR_WIDTH_MM = 36.0
        SENSOR_HEIGHT_MM = 24.0

    RES_X, RES_Y = res
    PIXEL_SIZE_X = SENSOR_WIDTH_MM / RES_X
    PIXEL_SIZE_Y = SENSOR_HEIGHT_MM / RES_Y

