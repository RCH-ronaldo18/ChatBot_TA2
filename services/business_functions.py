import json
import os
import unicodedata
import uuid
from datetime import date, datetime, timedelta


# ============================================================
# DATOS Y CONFIGURACIÓN
# ============================================================

def cargar_destinos():
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "destinos.json"
    )

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


DESTINOS = cargar_destinos()

NIVELES = ["bajo", "medio", "alto"]

MAX_DIAS_COTIZACION = 30

MAX_PERSONAS = 20

TIPOS_VIAJE = [
    "cultura",
    "aventura",
    "naturaleza",
    "playa",
    "gastronomia"
]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def norm(txt: str) -> str:
    """Minúsculas y sin tildes para comparar textos."""
    txt = unicodedata.normalize(
        "NFD",
        str(txt).strip().lower()
    )

    return "".join(
        c for c in txt
        if unicodedata.category(c) != "Mn"
    )


def buscar_destino_key(nombre: str) -> str | None:
    n = norm(nombre)

    for key in DESTINOS:
        if key in n or n in key:
            return key

    return None


# ============================================================
# FUNCIONES DEL NEGOCIO
# ============================================================

def buscar_destino(
    tipo_viaje: str = None,
    presupuesto: str = None,
    dias: int = None,
    personas: int = None,
) -> dict:

    tipo = norm(tipo_viaje) if tipo_viaje else None
    pres = norm(presupuesto) if presupuesto else None

    if tipo and tipo not in TIPOS_VIAJE:
        return {
            "error": f"tipo_viaje no válido. Opciones: {TIPOS_VIAJE}"
        }

    if pres and pres not in NIVELES:
        return {
            "error": f"presupuesto no válido. Opciones: {NIVELES}"
        }

    try:
        dias = int(dias) if dias else None
        personas = int(personas) if personas else None

    except (TypeError, ValueError):
        return {
            "error": "dias y personas deben ser números enteros"
        }

    if dias and not 1 <= dias <= MAX_DIAS_COTIZACION:
        return {
            "error": (
                f"dias debe estar entre 1 y {MAX_DIAS_COTIZACION}. "
                "Para estadías más largas, derivar a un asesor humano."
            )
        }

    if personas and not 1 <= personas <= MAX_PERSONAS:
        return {
            "error": (
                f"personas debe estar entre 1 y {MAX_PERSONAS}. "
                "Para grupos mayores, derivar a un asesor humano."
            )
        }

    niveles = [pres] if pres else NIVELES

    res = []

    for d in DESTINOS.values():

        if tipo and tipo not in d["tipos"]:
            continue

        item = {
            "destino": d["nombre"],
            "tipos": d["tipos"],
            "mejor_epoca": d["mejor_epoca"],
            "clima": d["clima"],
            "lugares_destacados": d["lugares"][:3],
        }

        if dias:

            por_persona = {
                n: d["precio_dia"][n] * dias
                for n in niveles
            }

            item["dias"] = dias

            item["precio_por_persona_PEN"] = por_persona

            if personas:
                item["personas"] = personas

                item["total_estimado_PEN"] = {
                    n: v * personas
                    for n, v in por_persona.items()
                }

        elif pres:

            item[
                "precio_referencial_por_persona_por_dia_PEN"
            ] = d["precio_dia"][pres]

        res.append(item)

    if not res:
        return {
            "resultados": [],
            "mensaje": "No hay destinos con esos criterios en el catálogo.",
        }

    return {
        "resultados": res,
        "nota": "Precios referenciales ficticios, sujetos a cotización.",
    }


def _paquetes_de(d: dict) -> list:

    res = []

    for n_dias in d["duraciones"]:

        for nivel in NIVELES:

            res.append(
                {
                    "paquete": (
                        f"{d['nombre']}, "
                        f"{n_dias} días y "
                        f"{n_dias - 1} "
                        f"{'noche' if n_dias == 2 else 'noches'}, "
                        f"nivel {nivel}"
                    ),

                    "dias": n_dias,

                    "nivel": nivel,

                    "precio_por_persona_PEN":
                        d["precio_dia"][nivel] * n_dias,

                    "incluye": [
                        "Alojamiento",
                        "Traslados",
                        "Tours principales"
                    ]
                    + (
                        ["Guía privado"]
                        if nivel == "alto"
                        else []
                    ),
                }
            )

    return res


def consultar_paquetes(
    destino: str,
    dias: int = None,
    presupuesto: str = None,
    presupuesto_max_pen: float = None,
) -> dict:

    key = buscar_destino_key(destino or "")

    if not key:
        return {
            "error": f"Destino '{destino}' no está en el catálogo.",
            "destinos_disponibles": [
                d["nombre"]
                for d in DESTINOS.values()
            ],
        }

    d = DESTINOS[key]

    pres = norm(presupuesto) if presupuesto else None

    if pres and pres not in NIVELES:
        return {
            "error": f"presupuesto no válido. Opciones: {NIVELES}"
        }

    if dias:

        try:
            dias = int(dias)

        except (TypeError, ValueError):
            return {
                "error": "dias debe ser un número entero"
            }

        if not 1 <= dias <= MAX_DIAS_COTIZACION:
            return {
                "error": (
                    f"dias debe estar entre 1 y {MAX_DIAS_COTIZACION}. "
                    "Para estadías más largas, derivar a un asesor humano."
                )
            }

    max_pen = None

    if presupuesto_max_pen:

        try:
            max_pen = float(presupuesto_max_pen)

        except (TypeError, ValueError):
            return {
                "error": (
                    "presupuesto_max_pen debe ser un número "
                    "(soles por persona)"
                )
            }

        if max_pen <= 0:
            return {
                "error": "presupuesto_max_pen debe ser mayor a 0"
            }

    todos = _paquetes_de(d)

    paquetes = [
        p
        for p in todos
        if (not pres or p["nivel"] == pres)
        and (not dias or p["dias"] == dias)
        and (not max_pen or p["precio_por_persona_PEN"] <= max_pen)
    ]

    if paquetes:
        return {
            "destino": d["nombre"],
            "paquetes": paquetes,
            "nota": (
                "Precios referenciales ficticios, "
                "sujetos a cotización."
            ),
        }

    resp = {
        "destino": d["nombre"],
        "paquetes": [],
        "mensaje": "No hay paquete estándar con esos filtros.",
        "duraciones_estandar": d["duraciones"],
    }

    if max_pen:
        resp["paquete_mas_economico"] = min(
            todos,
            key=lambda p: p["precio_por_persona_PEN"]
        )

    if dias and dias not in d["duraciones"]:

        niveles = [pres] if pres else NIVELES

        resp["opcion_a_medida"] = {
            "disponible": True,

            "detalle": (
                f"Se puede cotizar a medida de 1 a "
                f"{MAX_DIAS_COTIZACION} días con "
                "solicitar_cotizacion_viaje."
            ),

            "precio_referencial_por_persona_PEN": {
                n: d["precio_dia"][n] * dias
                for n in niveles
            },
        }

    return resp


def solicitar_cotizacion_viaje(
    destino: str = None,
    dias: int = None,
    personas: int = None,
    fecha_salida: str = None,
    nombre_cliente: str = None,
    presupuesto: str = "medio",
) -> dict:

    faltantes = [
        k
        for k, v in {
            "destino": destino,
            "dias": dias,
            "personas": personas,
            "fecha_salida": fecha_salida,
            "nombre_cliente": nombre_cliente,
        }.items()
        if not v
    ]

    if faltantes:
        return {
            "error": "Faltan datos",
            "faltantes": faltantes
        }

    key = buscar_destino_key(destino)

    if not key:
        return {
            "error": f"Destino '{destino}' no está en el catálogo.",
            "destinos_disponibles": [
                d["nombre"]
                for d in DESTINOS.values()
            ],
        }

    try:
        dias, personas = int(dias), int(personas)

    except (TypeError, ValueError):
        return {
            "error": "dias y personas deben ser números enteros"
        }

    if not 1 <= dias <= MAX_DIAS_COTIZACION:
        return {
            "error": (
                f"dias debe estar entre 1 y {MAX_DIAS_COTIZACION}. "
                "Para estadías más largas, derivar a un asesor humano."
            )
        }

    if not 1 <= personas <= MAX_PERSONAS:
        return {
            "error": (
                f"personas debe estar entre 1 y {MAX_PERSONAS}. "
                "Para grupos mayores, derivar a un asesor humano."
            )
        }

    nombre = str(nombre_cliente).strip()

    if (
        not 2 <= len(nombre) <= 60
        or any(c.isdigit() for c in nombre)
    ):
        return {
            "error": (
                "nombre_cliente no parece válido; "
                "pedirle al cliente su nombre nuevamente"
            )
        }

    pres = norm(presupuesto or "medio")

    if pres not in NIVELES:
        return {
            "error": f"presupuesto no válido. Opciones: {NIVELES}"
        }

    try:
        fecha = datetime.strptime(
            str(fecha_salida),
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return {
            "error": "fecha_salida debe tener formato YYYY-MM-DD"
        }

    if fecha < date.today():
        return {
            "error": "fecha_salida no puede estar en el pasado"
        }

    if fecha > date.today() + timedelta(days=730):
        return {
            "error": (
                "fecha_salida no puede superar "
                "los 2 años desde hoy"
            )
        }

    d = DESTINOS[key]

    por_persona = d["precio_dia"][pres] * dias

    res = {
        "codigo_cotizacion":
            "COT-" + uuid.uuid4().hex[:6].upper(),

        "cliente": nombre,

        "destino": d["nombre"],

        "dias": dias,

        "personas": personas,

        "fecha_salida": str(fecha),

        "nivel": pres,

        "precio_por_persona_PEN": por_persona,

        "total_estimado_PEN":
            por_persona * personas,

        "estado":
            "Cotización registrada (simulada). "
            "Un asesor confirmará disponibilidad.",
    }

    if dias > 15:
        res["nota"] = (
            "Viaje extendido: un asesor evaluará "
            "combinar destinos y confirmará disponibilidad."
        )

    return res


def consultar_itinerario(
    destino: str,
    dias: int
) -> dict:

    key = buscar_destino_key(destino or "")

    if not key:
        return {
            "error": f"Destino '{destino}' no está en el catálogo."
        }

    try:
        dias = int(dias)

    except (TypeError, ValueError):
        return {
            "error": "dias debe ser un número entero"
        }

    if not 1 <= dias <= 15:
        return {
            "error": (
                "dias debe estar entre 1 y 15. "
                "Para viajes más largos, sugerir combinar "
                "destinos con un asesor."
            )
        }

    d = DESTINOS[key]

    lugares = d["lugares"]

    plan = [
        {
            "dia": i + 1,
            "actividad": (
                lugares[i]
                if i < len(lugares)
                else "Día libre o excursión opcional"
            ),
        }
        for i in range(dias)
    ]

    res = {
        "destino": d["nombre"],
        "itinerario_sugerido": plan
    }

    if dias > len(lugares):
        res["nota"] = (
            "Los días adicionales quedan libres u opcionales; "
            "un asesor puede sugerir excursiones extra."
        )

    return res


# ============================================================
# MAPEO DE FUNCIONES
# ============================================================

FUNCIONES = {
    "buscar_destino": buscar_destino,
    "consultar_paquetes": consultar_paquetes,
    "solicitar_cotizacion_viaje": solicitar_cotizacion_viaje,
    "consultar_itinerario": consultar_itinerario,
}