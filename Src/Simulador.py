import Tipos
from Escalonador import *
from Evento import *
from FilaEventos import FilaEventos
from FilaClientes import filaClientes
from listaNumerosAleatorios import numeros


CHEGADA_INICIAL: float = 1
LIMITE_NUMEROS_ALEATORIOS: int = 100000
nroAleatoriosGerados: int = 0
estadosDaFila: list[int] = []
perdas: int = 0


class Simulador:
    tempoPassado = 0
    tempoUltimoEvento = 0

    def simular(self, nroDeFilas: int, tamanhoFila: list[int], nroServidores: list[int],
                tempoAtendimento: list[tuple[int, int]], tempoChegada: list[tuple[int, int]], roteamento):
        global nroAleatoriosGerados
        listaDeFilas = []

        for x in range(0, nroDeFilas):
            listaDeFilas.append(FilaClientes.filaClientes(tamanhoFila[x], x + 1,
                                                          tempoAtendimento[x], nroServidores[x],
                                                          tempoChegada[x], roteamento))

        nroAleatoriosGerados = 0
        filaEventos: FilaEventos = FilaEventos()

        escalonador = Escalonador()
        self.tempoPassado = 0
        self.tempoUltimoEvento = 0
        eventoInicial = Evento(Tipos.TiposEventos.CHEGADA, CHEGADA_INICIAL, 1)
        escalonador.adicionarEvento(eventoInicial, filaEventos)

        #while len(numeros) > 0:
        while nroAleatoriosGerados < 100000:
            evento = escalonador.evento(filaEventos)
            idDaFila = evento.idDaFila
            match evento.tipo:
                case TiposEventos.CHEGADA:
                    self.chegada(evento, listaDeFilas, filaEventos, escalonador,
                                 listaDeFilas[idDaFila - 1].nroServidores)
                case TiposEventos.SAIDA:
                    self.saida(evento, listaDeFilas, escalonador, filaEventos)
                case TiposEventos.PARTIDA:
                    self.partida(evento, evento.idDaFila, evento.destino, listaDeFilas, escalonador, filaEventos)

        return listaDeFilas

    def chegada(self, evento: Evento, filasClientes: list[filaClientes], filaEventos: FilaEventos,
                escalonador: Escalonador, nroServidores: int):

        self.tempoPassado = evento.tempo
        for filas in filasClientes:
            filas.contabilizaTempo(self.tempoPassado)

        filaOrigem = filasClientes[evento.idDaFila - 1]
        quantidadeClientes = filaOrigem.getQuantidadeClientes()

        if quantidadeClientes < filaOrigem.tamanhoFila:
            filaOrigem.addCliente()
            if filaOrigem.getQuantidadeClientes() <= nroServidores:
                idFilaDestino = filaOrigem.defineSaida()  # Possibilidade de calcular qual fia será o destino futuramente
                filaDestino = filasClientes[idFilaDestino - 1]
                match idFilaDestino:
                    case 0:
                        escalonador.agendarSaida(filaEventos, self.tempoPassado, filaOrigem.tempoAtendimento, filaOrigem.ID)
                    case _:
                        escalonador.agendarPartida(filaOrigem, filaDestino, self.tempoPassado, filaEventos)
        else:
            filaOrigem.totalPerdas += 1

        escalonador.agendarChegada(filaEventos, self.tempoPassado, filaOrigem.tempoDeChegada, evento.idDaFila)

    def saida(self, evento: Evento, filasDeClientes: list[filaClientes], escalonador: Escalonador,
              filaEventos: FilaEventos):

        self.tempoPassado = evento.tempo
        for fila in filasDeClientes:
            fila.contabilizaTempo(self.tempoPassado)

        filaASerTratada = filasDeClientes[evento.idDaFila - 1]

        filaASerTratada.saidaCliente()
        nroServidores = filaASerTratada.nroServidores
        if filaASerTratada.getQuantidadeClientes() >= nroServidores:

            idFilaDestino = filaASerTratada.defineSaida()  # Possibilidade de calcular qual fia será o destino futuramente
            filaDestino = filasDeClientes[idFilaDestino - 1]

            match idFilaDestino:
                case 0:
                    escalonador.agendarSaida(filaEventos, self.tempoPassado,
                                             filaASerTratada.tempoAtendimento, filaASerTratada.ID)
                case _:
                    escalonador.agendarPartida(filaASerTratada, filaDestino, self.tempoPassado, filaEventos)


    def partida(self, evento: Evento, filaDeSaida: int, filaDeChegada: int, listaFilas: list[filaClientes],
                escalonador: Escalonador, filaEventos: FilaEventos):

        self.tempoPassado = evento.tempo
        for filas in listaFilas:
            filas.contabilizaTempo(self.tempoPassado)
        filaSaida = listaFilas[filaDeSaida - 1]
        filaDestino = listaFilas[filaDeChegada - 1]
        filaSaida.saidaCliente()

        if filaSaida.getQuantidadeClientes() >= filaSaida.nroServidores:
            idPartida = filaSaida.defineSaida()
            partida = listaFilas[idPartida - 1]
            match idPartida:
                case 0:
                    escalonador.agendarSaida(filaEventos, self.tempoPassado, filaSaida.tempoAtendimento, filaDeSaida)
                case _:
                    escalonador.agendarPartida(filaSaida, partida, self.tempoPassado, filaEventos)

        if filaDestino.getQuantidadeClientes() < filaDestino.tamanhoFila:
            filaDestino.addCliente()
        else:
            filaDestino.totalPerdas += 1

        if filaDestino.getQuantidadeClientes() <= filaDestino.nroServidores:
            idFila = filaDestino.defineSaida()  # Possibilidade de calcular qual fia será o destino futuramente
            filaDefinida = listaFilas[idFila - 1]
            match idFila:
                case 0:
                    escalonador.agendarSaida(filaEventos, self.tempoPassado, filaDestino.tempoAtendimento,
                                             filaDestino.ID)
                case _:
                    escalonador.agendarPartida(filaDestino, filaDefinida, self.tempoPassado, filaEventos)
