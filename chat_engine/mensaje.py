from datetime import datetime

class Mensaje:
    def __init__(self, contenido: str, emisor: str, hora: datetime):
        self.contenido = contenido
        self.emisor = emisor
        self.hora = hora
    def format(self) -> str:
        hora = self.hora.strftime("%H:%M:%S")
        emisor = self.emisor
        contenido = self.contenido
        return(f"{hora} - {emisor}: {contenido}")
