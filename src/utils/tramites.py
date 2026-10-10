from classes.estudiante import Estudiante
from classes.area import Area
from classes.tramite import Tramite
from datetime import datetime

TIPOS_TRAMITE = [
    "Certificado de estudios",
    "Traslado de colegio",
    "Justificacion de inasistencias",
    "Exoneracion de cursos",
    "Reclamo o apelacion",
]

estudiantes = []
areas = []
historial_tramites = []
secuencia_tramites = 1


def cargar_datos_prueba():
    estudiantes.append(Estudiante("70000001", "Maria Flores", "3ro A"))
    estudiantes.append(Estudiante("70000002", "Jorge Paredes", "5to B"))
    estudiantes.append(Estudiante("70000003", "Rosa Medina", "2do C"))

    areas.append(Area("A001", "Secretaria Academica", TIPOS_TRAMITE[0]))
    areas.append(Area("A002", "Direccion", TIPOS_TRAMITE[1]))
    areas.append(Area("A003", "Tutoria", TIPOS_TRAMITE[2]))
    areas.append(Area("A004", "Coordinacion Academica", TIPOS_TRAMITE[3]))
    areas.append(Area("A005", "Subdireccion", TIPOS_TRAMITE[4]))


def buscar_estudiante(dni: str):
    for e in estudiantes:
        if e.dni == dni.strip():
            return e
    return None


def buscar_area(codigo: str):
    for a in areas:
        if a.codigo.lower() == codigo.strip().lower():
            return a
    return None


def buscar_area_por_tramite(tipo: str):
    for a in areas:
        if a.tramite_atendido == tipo:
            return a
    return None


def buscar_tramite(codigo: str):
    for t in historial_tramites:
        if t.codigo.lower() == codigo.strip().lower():
            return t
    return None


def hay_tramite_en_curso(dni: str, tipo: str) -> bool:
    for t in historial_tramites:
        if t.estudiante.dni == dni and t.tipo == tipo and t.esta_en_curso():
            return True
    return False


def elegir_tipo():
    for i, tipo in enumerate(TIPOS_TRAMITE, start=1):
        print(f"  {i}. {tipo}")
    opcion = input(f"Seleccione el tipo de tramite (1-{len(TIPOS_TRAMITE)}): ").strip()
    if not opcion.isdigit() or not (1 <= int(opcion) <= len(TIPOS_TRAMITE)):
        return None
    return TIPOS_TRAMITE[int(opcion) - 1]


def registrar_estudiante_menu():
    print("\n--- REGISTRAR ESTUDIANTE (RF01) ---")
    try:
        dni = input("Ingrese DNI del estudiante (8 digitos): ").strip()
        if not (dni.isdigit() and len(dni) == 8):
            print("[ERROR] El DNI debe tener exactamente 8 digitos.")
            return
        if buscar_estudiante(dni) is not None:
            print(f"[ERROR] El estudiante con DNI {dni} ya existe.")
            return

        nombre = input("Ingrese nombre completo: ").strip()
        grado = input("Ingrese grado y seccion (ej. 3ro A): ").strip()

        nuevo = Estudiante(dni, nombre, grado)
        estudiantes.append(nuevo)
        print(f"[OK]  {nuevo.resumen()}  registrado correctamente.")

    except ValueError as err:
        print(f"[ERROR] {err}")


def registrar_area_menu():
    print("\n--- REGISTRAR AREA (RF02) ---")
    codigo = input("Ingrese codigo del area (ej. A006): ").strip()
    if not codigo:
        print("[ERROR] El codigo no puede estar vacio.")
        return
    if buscar_area(codigo) is not None:
        print(f"[ERROR] El area con codigo {codigo} ya existe.")
        return

    nombre = input("Ingrese nombre del area: ").strip()
    if not nombre:
        print("[ERROR] El nombre no puede estar vacio.")
        return

    print("Que tramite atiende esta area?")
    tipo = elegir_tipo()
    if tipo is None:
        print("[ERROR] Tipo de tramite invalido.")
        return

    nueva_area = Area(codigo, nombre, tipo)
    areas.append(nueva_area)
    print(f"[OK] {nueva_area.resumen()} registrada correctamente.")


def buscar_por_codigo_menu():
    print("\n--- BUSCAR POR CODIGO (RF03) ---")
    codigo = input("Ingrese DNI, codigo de area o ticket de tramite: ").strip()

    estudiante = buscar_estudiante(codigo)
    area = buscar_area(codigo)
    tramite = buscar_tramite(codigo)

    if estudiante is not None:
        print(f"[ENCONTRADO - ESTUDIANTE]: {estudiante.resumen()}")
    elif area is not None:
        print(f"[ENCONTRADO - AREA]: {area.resumen()}")
    elif tramite is not None:
        print("[ENCONTRADO - TRAMITE]:")
        print(tramite.resumen())
    else:
        print(f"[ERROR] No se encontro nada registrado con el codigo '{codigo}'.")


def registrar_tramite_menu():
    global secuencia_tramites
    print("\n--- REGISTRAR TRAMITE (RF04) ---")

    dni = input("Ingrese DNI del estudiante: ").strip()
    estudiante = buscar_estudiante(dni)
    if estudiante is None:
        print(f"[ERROR] No existe estudiante con DNI '{dni}'. Debe registrarlo primero.")
        return

    tipo = elegir_tipo()
    if tipo is None:
        print("[ERROR] Tipo de tramite invalido.")
        return

    area = buscar_area_por_tramite(tipo)
    if area is None:
        print(f"[ERROR] No hay un area registrada que atienda '{tipo}'.")
        return

    if hay_tramite_en_curso(dni, tipo):
        print("[ERROR] Este estudiante ya tiene ese tramite en curso.")
        return

    fecha = input("Ingrese fecha (o presione Enter para fecha actual): ").strip()
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    motivo = input("Ingrese motivo o detalle del tramite: ").strip()
    if not motivo:
        print("[ERROR] El motivo no puede estar vacio.")
        return

    ticket = f"TR-{secuencia_tramites:03d}"
    nuevo = Tramite(ticket, estudiante, area, tipo, fecha, motivo)
    historial_tramites.append(nuevo)
    secuencia_tramites += 1

    print(f"[OK] Tramite registrado para {estudiante.nombre}.")
    print(f"     Su ticket es: {ticket} | Area destino: {area.nombre}")


def atender_tramite_menu():
    print("\n--- ATENDER TRAMITE / CAMBIAR ESTADO (RF05) ---")
    codigo = input("Ingrese el ticket del tramite (ej. TR-001): ").strip()

    tramite = buscar_tramite(codigo)
    if tramite is None:
        print(f"[ERROR] No se encontro el tramite con ticket '{codigo}'.")
        return

    print(f"Estado actual: {tramite.estado}")
    for i, estado in enumerate(Tramite.ESTADOS_VALIDOS, start=1):
        print(f"  {i}. {estado}")
    opcion = input(f"Seleccione el nuevo estado (1-{len(Tramite.ESTADOS_VALIDOS)}): ").strip()
    if not opcion.isdigit() or not (1 <= int(opcion) <= len(Tramite.ESTADOS_VALIDOS)):
        print("[ERROR] Estado invalido.")
        return

    respuesta = input("Ingrese la respuesta o nota de atencion: ").strip()
    try:
        tramite.cambiar_estado(Tramite.ESTADOS_VALIDOS[int(opcion) - 1], respuesta)
        print(f"[OK] Tramite {tramite.codigo} actualizado a '{tramite.estado}'.")
    except ValueError as err:
        print(f"[ERROR] {err}")


def buscar_areas_por_tramite_menu():
    print("\n--- BUSQUEDA DE AREAS POR TIPO DE TRAMITE (CONSULTA FUNCIONAL) ---")
    texto = input("Ingrese el tramite a buscar (ej. certificado): ").strip()

    encontradas = list(
        filter(lambda a: texto.lower() in a.tramite_atendido.lower(), areas)
    )

    if not encontradas:
        print(f"No se encontraron areas que atiendan '{texto}'.")
    else:
        print(f"\nSe encontraron {len(encontradas)} area(s):")
        for a in encontradas:
            print(f" - {a.resumen()}")


def consultar_historial_estudiante_menu():
    print("\n--- CONSULTAR HISTORIAL DE TRAMITES POR ESTUDIANTE ---")
    dni = input("Ingrese DNI del estudiante a consultar: ").strip()

    tramites_estudiante = list(
        filter(lambda t: t.estudiante.dni == dni, historial_tramites)
    )

    if not tramites_estudiante:
        print(f"No se encontraron tramites para el DNI '{dni}'.")
    else:
        print(f"\nSe encontraron {len(tramites_estudiante)} tramite(s):")
        for t in tramites_estudiante:
            print("----------------------------------------")
            print(t.resumen())
        print("----------------------------------------")
