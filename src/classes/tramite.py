from .estudiante import Estudiante
from .area import Area


class Tramite:
    ESTADOS_VALIDOS = ["Pendiente", "En revisión", "Aprobado", "Rechazado"]

    def __init__(
        self,
        codigo: str,
        estudiante: Estudiante,
        area: Area,
        tipo: str,
        fecha: str,
        motivo: str = "",
    ):
        self._codigo = str(codigo).strip()
        self._estudiante = estudiante
        self._area = area
        self._tipo = str(tipo).strip()
        self._fecha = str(fecha).strip()
        self._motivo = str(motivo).strip()
        self._estado = "Pendiente"
        self._respuesta = ""

    @property
    def codigo(self):
        return self._codigo

    @property
    def estudiante(self):
        return self._estudiante

    @property
    def area(self):
        return self._area

    @property
    def tipo(self):
        return self._tipo

    @property
    def fecha(self):
        return self._fecha

    @property
    def estado(self):
        return self._estado

    def esta_en_curso(self) -> bool:
        return self._estado == "Pendiente" or self._estado == "En revisión"

    def cambiar_estado(self, nuevo_estado: str, respuesta: str = ""):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"'{nuevo_estado}' no es un estado válido.")
        self._estado = nuevo_estado
        self._respuesta = respuesta

    def resumen(self) -> str:
        info = (
            f"Trámite [{self._codigo}] - {self._tipo} | Estado: {self._estado}\n"
            f"  Estudiante: {self._estudiante.nombre} (DNI: {self._estudiante.dni})\n"
            f"  Área      : {self._area.nombre}\n"
            f"  Fecha     : {self._fecha}"
        )
        if self._motivo:
            info += f"\n  Motivo    : {self._motivo}"
        if self._respuesta:
            info += f"\n  Respuesta : {self._respuesta}"
        return info
