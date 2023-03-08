from Simulador import Simulador
import numpy as np
from tabulate import tabulate
import sys

NRO_EXECUCOES = 1
CHEGADA_INICIAL = 1


def main(TAM_FILA, CHEGADAS, ATENDIMENTO, NRO_SERVIDORES, roteamento):
    totalPerdas = []
    nroDeFilas = len(ATENDIMENTO)

    for perdas in range(0, len(TAM_FILA)):
        totalPerdas.append(0)

    resultadosObtidos = []
    for fila in range(0, len(TAM_FILA)):
        resultadosObtidos.append([])

    for result in range(0, len(resultadosObtidos)):
        for estadosDaFila in range(0, TAM_FILA[result] + 1):
            resultadosObtidos[result].append(0)

    for x in range(0, NRO_EXECUCOES):
        simulador = Simulador()
        resultados = simulador.simular(nroDeFilas, TAM_FILA, NRO_SERVIDORES, ATENDIMENTO, CHEGADAS, roteamento)
        for filasObtidas in range(0, len(resultados)):
            resultadosObtidos[filasObtidas] = (
                np.add(resultadosObtidos[filasObtidas], resultados[filasObtidas].estadosDaFila))
            totalPerdas[filasObtidas] += resultados[filasObtidas].totalPerdas

    for aux in range(0, len(resultadosObtidos)):
        exibirResultado(resultadosObtidos[aux], totalPerdas[aux], NRO_EXECUCOES, TAM_FILA[aux], NRO_SERVIDORES[aux],
                        CHEGADAS[aux], ATENDIMENTO[aux])


def exibirResultado(resultadosObtidos, totalPerdas, NRO_EXECUCOES, TAM_FILA, NRO_SERVIDORES, CHEGADAS, ATENDIMENTO):


    mediaAtendimento = (1/((ATENDIMENTO[0] + ATENDIMENTO[1])/2)) * NRO_SERVIDORES
    print(mediaAtendimento, "ATENDIMENTO")
    listaResultados = (resultadosObtidos / NRO_EXECUCOES).tolist()
    z = sum(listaResultados)
    print(z * (1/len(listaResultados)))
    listaProbabilidade = []
    listaFormatada = []
    for x in listaResultados:
        listaProbabilidade.append(round(x / sum(listaResultados) * 100, 2))


    pupulacaomedia = 0
    for aux, x in enumerate(listaProbabilidade):
        pupulacaomedia += (x/100) * (aux+1)

    print(pupulacaomedia, "POP MEDIA")

    utilizacao = 0
    vazao = 0

    for aux, x in enumerate(listaProbabilidade):
        utilizacao += (x/100) * (min(aux, int(NRO_SERVIDORES))/int(NRO_SERVIDORES))
        vazao += (x/100) * (mediaAtendimento * min(aux, NRO_SERVIDORES))

    print(utilizacao, "UTIL")
    print(vazao, "VAZAO")
    print(pupulacaomedia/vazao, "TEMPO")

    for x in range(0, len(listaResultados)):
        listaFormatada.append([x, str(round(listaResultados[x], 2)), listaProbabilidade[x]])

    print(listaFormatada)

    print('Tamanho fila: ', TAM_FILA)
    print('Numero de servidores: ', NRO_SERVIDORES)
    print('Chegadas entre ', CHEGADAS[0], 'e', CHEGADAS[1])
    print('Saidas entre ', ATENDIMENTO[0], 'e', ATENDIMENTO[1])
    print('Chegada incial em', CHEGADA_INICIAL)
    print('====================================================')
    print('\n\nPerdas: ', round(totalPerdas / NRO_EXECUCOES, 2), '\n')
    print('----------------------------------------------------\n')
    print(tabulate(listaFormatada, headers=['Estado', 'Tempo', 'Probabilidade'], tablefmt='pretty'))
    print("\n\n\n\n")


def getMediaPerdas(resultadosObtidos) -> float:
    return resultadosObtidos / NRO_EXECUCOES


def getDescricao(arquivo):
    filas = []
    roteamento = []
    chegouRoteamento = False
    with open(arquivo) as f:
        linhas = f.readlines()
        for x in linhas:
            if x == "ROTEAMENTO\n":
                chegouRoteamento = True
            elif chegouRoteamento and x != "ROTEAMENTO\n":
                roteamento.append(x)
            else:
                filas.append(x.split(" "))

    return filas, roteamento


def formataParaSimulador(filas):
    tamanhoFila = []
    nroServidores = []
    tempoAtendimento = []
    tempoChegada = []

    for fila in filas:
        infos = fila[0].split("/")
        nroServidores.append(int(infos[2]))
        tamanhoFila.append(int(infos[3]))

        tempoChegadaStr = fila[1].split(",")
        tempoChegada.append((float(tempoChegadaStr[0].replace("\n", "")), float(tempoChegadaStr[1].replace("\n", ""))))

        tempoAtendimentoStr = fila[2].split(",")
        tempoAtendimento.append(
            (float(tempoAtendimentoStr[0].replace("\n", "")), float(tempoAtendimentoStr[1].replace("\n", ""))))

    return tamanhoFila, nroServidores, tempoAtendimento, tempoChegada


if __name__ == '__main__':

    filas, roteamento = getDescricao("filas.txt")
    tamanhoFila, nroServidores, tempoAtendimento, tempoChegada = formataParaSimulador(filas)
    for aux, x in enumerate(roteamento):
        roteamento[aux] = x.replace('\n', '')
    # entradas = sys.argv[1:]
    # chegada = list(map(int, entradas[0].split(',')))
    # atendimento = list(map(int, entradas[1].split(',')))
    # nroServidores = int(entradas[2])
    # tamFila = int(entradas[3])
    #

    main(tamanhoFila, tempoChegada, tempoAtendimento, nroServidores, roteamento)
