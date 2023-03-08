class Evento:
    def __init__(self, tipo, tempo, idFila, destino=None):
        self.tipo = tipo
        self.tempo = tempo
        self.idDaFila = idFila
        self.destino = destino
