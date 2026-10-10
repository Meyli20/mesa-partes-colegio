from classes.estudiante import Estudiante
from classes.area import Area
from classes.tramite import Tramite
from datetime import datetime

TIPOS_TRAMITE = [
    "Certificado de estudios",
    "Traslado de colegio",
    "Justificación de inasistencias",
    "Exoneración de cursos",
    "Reclamo o apelación",
]

estudiantes = []
areas = []
historial_tramites = []
secuencia_tramites = 1


def cargar_datos_prueba():
    estudiantes.append(Estudiante("70000001", "María Flores", "3ro A"))
    estudiantes.append(Estudiante("70000002", "Jorge Paredes", "5to B"))
    estudiantes.append(Estudiante("70000003", "Rosa Medina", "2do C"))

    areas.append(Area("A001", "Secretaría Académica", TIPOS_TRAMITE[0]))
    areas.append(Area("A002", "Dirección", TIPOS_TRAMITE[1]))
    areas.append(Area("A003", "Tutoría", TIPOS_TRAMITE[2]))
    areas.append(Area("A004", "Coordinación Académica", TIPOS_TRAMITE[3]))
    areas.append(Area("A005", "Subdirección", TIPOS_TRAMITE[4]))


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
    opcion = input(f"Seleccione el tipo de trámite (1-{len(TIPOS_TRAMITE)}): ").strip()
    if not opcion.isdigit() or not (1 <= int(opcion) <= len(TIPOS_TRAMITE)):
        return None
    return TIPOS_TRAMITE[int(opcion) - 1]


def registrar_estudiante_menu():
    print("\n--- REGISTRAR ESTUDIANTE (RF01) ---")
    try:
        dni = input("Ingrese DNI del estudiante (8 dígitos): ").strip()
        if not (dni.isdigit() and len(dni) == 8):
            print("[ERROR] El DNI debe tener exactamente 8 dígitos.")
            return
        if buscar_estudiante(dni) is not None:
            print(f"[ERROR] El estudiante con DNI {dni} ya existe.")
            return

        nombre = input("Ingrese nombre completo: ").strip()
        grado = input("Ingrese grado y sección (ej. 3ro A): ").strip()

        nuevo = Estudiante(dni, nombre, grado)
        estudiantes.append(nuevo)
        print(f"[OK] {nuevo.resumen()} registrado correctamente.")

    except ValueError as err:
        print(f"[ERROR] {err}")


def registrar_area_menu():
    print("\n--- REGISTRAR ÁREA (RF02) ---")
    codigo = input("Ingrese código del área (ej. A006): ").strip()
    if not codigo:
        print("[ERROR] El código no puede estar vacío.")
        return
    if buscar_area(codigo) is not None:
        print(f"[ERROR] El área con código {codigo} ya existe.")
        return

    nombre = input("Ingrese nombre del área: ").strip()
    if not nombre:
        print("[ERROR] El nombre no puede estar vacío.")
        return

    print("¿Qué trámite atiende esta área?")
    tipo = elegir_tipo()
    if tipo is None:
        print("[ERROR] Tipo de trámite inválido.")
        return

    nueva_area = Area(codigo, nombre, tipo)
    areas.append(nueva_area)
    print(f"[OK] {nueva_area.resumen()} registrada correctamente.")


def buscar_por_codigo_menu():
    print("\n--- BUSCAR POR CÓDIGO (RF03) ---")
    codigo = input("Ingrese DNI, código de área o ticket de trámite: ").strip()

    estudiante = buscar_estudiante(codigo)
    area = buscar_area(codigo)
    tramite = buscar_tramite(codigo)

    if estudiante is not None:
        print(f"[ENCONTRADO - ESTUDIANTE]: {estudiante.resumen()}")
    elif area is not None:
        print(f"[ENCONTRADO - ÁREA]: {area.resumen()}")
    elif tramite is not None:
        print("[ENCONTRADO - TRÁMITE]:")
        print(tramite.resumen())
    else:
        print(f"[ERROR] No se encontró nada registrado con el código '{codigo}'.")


def registrar_tramite_menu():
    global secuencia_tramites
    print("\n--- REGISTRAR TRÁMITE (RF04) ---")

    dni = input("Ingrese DNI del estudiante: ").strip()
    estudiante = buscar_estudiante(dni)
    if estudiante is None:
        print(f"[ERROR] No existe estudiante con DNI '{dni}'. Debe registrarlo primero.")
        return

    tipo = elegir_tipo()
    if tipo is None:
        print("[ERROR] Tipo de trámite inválido.")
        return

    area = buscar_area_por_tramite(tipo)
    if area is None:
        print(f"[ERROR] No hay un área registrada que atienda '{tipo}'.")
        return

    if hay_tramite_en_curso(dni, tipo):
        print("[ERROR] Este estudiante ya tiene ese trámite en curso.")
        return

    fecha = input("Ingrese fecha (o presione Enter para fecha actual): ").strip()
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    motivo = input("Ingrese motivo o detalle del trámite: ").strip()
    if not motivo:
        print("[ERROR] El motivo no puede estar vacío.")
        return

    ticket = f"TR-{secuencia_tramites:03d}"
    nuevo = Tramite(ticket, estudiante, area, tipo, fecha, motivo)
    historial_tramites.append(nuevo)
    secuencia_tramites += 1

    print(f"[OK] Trámite registrado para {estudiante.nombre}.")
    print(f"     Su ticket es: {ticket} | Área destino: {area.nombre}")


def atender_tramite_menu():
    print("\n--- ATENDER TRÁMITE / CAMBIAR ESTADO (RF05) ---")
    codigo = input("Ingrese el ticket del trámite (ej. TR-001): ").strip()

    tramite = buscar_tramite(codigo)
    if tramite is None:
        print(f"[ERROR] No se encontró el trámite con ticket '{codigo}'.")
        return

    print(f"Estado actual: {tramite.estado}")
    for i, estado in enumerate(Tramite.ESTADOS_VALIDOS, start=1):
        print(f"  {i}. {estado}")
    opcion = input(f"Seleccione el nuevo estado (1-{len(Tramite.ESTADOS_VALIDOS)}): ").strip()
    if not opcion.isdigit() or not (1 <= int(opcion) <= len(Tramite.ESTADOS_VALIDOS)):
        print("[ERROR] Estado inválido.")
        return

    respuesta = input("Ingrese la respuesta o nota de atención: ").strip()
    try:
        tramite.cambiar_estado(Tramite.ESTADOS_VALIDOS[int(opcion) - 1], respuesta)
        print(f"[OK] Trámite {tramite.codigo} actualizado a '{tramite.estado}'.")
    except ValueError as err:
        print(f"[ERROR] {err}")


def buscar_areas_por_tramite_menu():
    print("\n--- BÚSQUEDA DE ÁREAS POR TIPO DE TRÁMITE (CONSULTA FUNCIONAL) ---")
    texto = input("Ingrese el trámite a buscar (ej. certificado): ").strip()

    encontradas = list(
        filter(lambda a: texto.lower() in a.tramite_atendido.lower(), areas)
    )

    if not encontradas:
        print(f"No se encontraron áreas que atiendan '{texto}'.")
    else:
        print(f"\nSe encontraron {len(encontradas)} área(s):")
        for a in encontradas:
            print(f" - {a.resumen()}")


def consultar_historial_estudiante_menu():
    print("\n--- CONSULTAR HISTORIAL DE TRÁMITES POR ESTUDIANTE ---")
    dni = input("Ingrese DNI del estudiante a consultar: ").strip()

    tramites_estudiante = list(
        filter(lambda t: t.estudiante.dni == dni, historial_tramites)
    )

    if not tramites_estudiante:
        print(f"No se encontraron trámites para el DNI '{dni}'.")
    else:
        print(f"\nSe encontraron {len(tramites_estudiante)} trámite(s):")
        for t in tramites_estudiante:
            print("----------------------------------------")
            print(t.resumen())
        print("----------------------------------------")
