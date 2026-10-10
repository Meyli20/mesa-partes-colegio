class Area:
    def __init__(self, codigo: str, nombre: str, tramite_atendido: str):
        self._codigo = str(codigo).strip()
        self._nombre = str(nombre).strip()
        self._tramite_atendido = str(tramite_atendido).strip()

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tramite_atendido(self) -> str:
        return self._tramite_atendido

    def resumen(self) -> str:
        return f"Área [Código: {self._codigo}] {self._nombre} - Atiende: {self._tramite_atendido}"
