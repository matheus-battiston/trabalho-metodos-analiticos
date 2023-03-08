# Gera os números, recebendo os parametros de geração e a quantidade de números que devem ser gerados
import time
import Simulador
from listaNumerosAleatorios import numeros


def calculo_mcl() -> float:
    a = 1103515245
    c = 12345
    M = 2 ** 32
    seed = int(time.time() * 10000000.0)

    nroGerado = ((a * seed) + c) % M

    return nroGerado / M


def numeroAleatorioNoIntervalo(intervalo: tuple[int, int]) -> float:
    nroAleatorioGerado = calculo_mcl()
    if len(numeros) == 0:
        return 1000000
    # nroAleatorioGerado = numeros.pop(0)
    nroNoIntervalo = ((intervalo[1] - intervalo[0]) * nroAleatorioGerado) + intervalo[0]
    Simulador.nroAleatoriosGerados += 1

    return nroNoIntervalo
