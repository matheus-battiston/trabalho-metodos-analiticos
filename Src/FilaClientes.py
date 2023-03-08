import math
from MCL import numeroAleatorioNoIntervalo


class filaClientes:
    def __init__(self, tamanhoFila: int, idFila: int, tempoAtendimento: tuple[int, int], nroServidores: int,
                 tempoDeChegada: tuple[int, int], roteamento):

        if tamanhoFila == 0:
            self.tamanhoFila = math.inf
        else:
            self.tamanhoFila: int = tamanhoFila
        self.clientesNaFila: int = 0
        self.ID = idFila
        self.totalPerdas = 0
        self.estadosDaFila = self.criarEstadosDaFila(tamanhoFila)
        self.tempoAtendimento = tempoAtendimento
        self.nroServidores = nroServidores
        self.tempoUltimoEvento = 0
        self.tempoDeChegada = tempoDeChegada
        self.roteamento = {}
        self.addRoteamento(roteamento)

    def addCliente(self):
        self.clientesNaFila += 1
        if self.tamanhoFila != math.inf:
            return

        if self.clientesNaFila == len(self.estadosDaFila):
            self.estadosDaFila.append(0)

    def getQuantidadeClientes(self) -> int:
        return self.clientesNaFila

    def saidaCliente(self):
        self.clientesNaFila -= 1

    def getTamanhoFila(self) -> int:
        return self.tamanhoFila

    def criarEstadosDaFila(self, tamanhoFila: int) -> list[int]:
        estadosDaFila = []
        for x in range(0, tamanhoFila + 1):
            estadosDaFila.append(0)

        return estadosDaFila

    def contabilizaTempo(self, tempoPassado: float):
        tempoNoEstado = tempoPassado - self.tempoUltimoEvento
        estadoParaAtualizar = self.getQuantidadeClientes()
        self.estadosDaFila[estadoParaAtualizar] += tempoNoEstado
        self.tempoUltimoEvento = tempoPassado

    def addRoteamento(self, roteamentos):
        soma = 0
        for x in roteamentos:
            xFormatado = x.split(" ")
            if xFormatado[0] == "FILA" + str(self.ID):
                self.roteamento[xFormatado[1]] = float(xFormatado[2]) + soma
                soma += float(xFormatado[2])

    def defineSaida(self):
        nroAleatorio = numeroAleatorioNoIntervalo((0, 1))
        for x in self.roteamento:
            if nroAleatorio < self.roteamento[x]:
                if x == "SAIDA":
                    return 0
                else:
                    return int(x.replace("FILA", ""))

