class Estudiante:
    def __init__(self, dni: str, nombre: str, grado: str):
        dni = str(dni).strip()
        if not (dni.isdigit() and len(dni) == 8):
            raise ValueError("El DNI debe tener exactamente 8 digitos.")
        if not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacio.")
        self._dni = dni
        self._nombre = str(nombre).strip()
        self._grado = str(grado).strip()

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def grado(self) -> str:
        return self._grado

    def resumen(self) -> str:
        return f"Estudiante [DNI: {self._dni}] {self._nombre} - {self._grado}"
