import Evento
import FilaClientes
from FilaEventos import FilaEventos
from MCL import numeroAleatorioNoIntervalo as randomNumberGenerator
from Evento import Evento
from Tipos import TiposEventos


class Escalonador:

    def __init__(self):
        self.escalonador = 0

    def adicionarEvento(self, evento: Evento, filaEventos: FilaEventos):
        filaEventos.adicionarEvento(evento)

    def removerEvento(self, evento: Evento, fila: FilaEventos):
        fila.removerEvento(evento)

    def evento(self, filaEventos: FilaEventos):
        eventoAnalisado = filaEventos.fila.pop(0)
        return eventoAnalisado

    def agendarSaida(self, filaEventos: FilaEventos, tempoPassado: float, intervaloAtendimento: tuple[int, int],
                     idFila: int):
        nroAleatorioGerado: float = randomNumberGenerator(intervaloAtendimento)
        eventoNovo = Evento(TiposEventos.SAIDA, nroAleatorioGerado + tempoPassado, idFila)
        filaEventos.adicionarEvento(eventoNovo)

    def agendarChegada(self, filaEventos: FilaEventos, tempoPassado: float, intervaloChegada: tuple[int, int],
                       idFila: int):
        nroAleatorioGerado: float = randomNumberGenerator(intervaloChegada)
        eventoNovo: Evento = Evento(TiposEventos.CHEGADA, nroAleatorioGerado + tempoPassado, idFila)
        filaEventos.adicionarEvento(eventoNovo)

    def agendarPartida(self, filaOrigem: FilaClientes, filaDestino: FilaClientes, tempoPassado: float,
                       filaEventos: FilaEventos):
        nroAleatorioGerado: float = randomNumberGenerator(filaOrigem.tempoAtendimento)
        eventoNovo: Evento = Evento(TiposEventos.PARTIDA, nroAleatorioGerado + tempoPassado, filaOrigem.ID,
                                    filaDestino.ID)
        filaEventos.adicionarEvento(eventoNovo)
