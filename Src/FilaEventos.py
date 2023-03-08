import Evento


class FilaEventos:
    def __init__(self):
        self.fila: list[Evento] = []

    def adicionarEvento(self, evento: Evento):
        self.fila.append(evento)
        self.fila.sort(key=lambda x: x.tempo)

    def removerEvento(self, evento: Evento):
        self.fila.remove(evento)

    def getTamanho(self) -> int:
        return len(self.fila)

    def toString(self):
        for x in self.fila:
            print(x.tipo, x.tempo, x.idDaFila, x.destino)

