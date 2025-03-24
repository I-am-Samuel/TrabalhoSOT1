from multiprocessing import Process
import os
import math
import time

def tarefa_demorada():
    print("Iniciando Tarefa...")
    time.sleep(5)
    print("Tarefa concluída.")

def mostrar_ids():
    print("Filho: PID = ", os.getpid(), "PPID = ", os.getppid)
    time.sleep(5)
    print("Filho finalizando: PID = ", os.getpid)

def calcular_operacao_intensiva(n):
    for _ in range(100):
        resultado = math.factorial(30000)
    print(f"Processo {n} completou operações intensivas")

if __name__ == "__main__":
    processo1 = Process(target=tarefa_demorada)
    processo2 = Process(target=tarefa_demorada)

    processo1.start()
    processo2.start()

    processo1.join()
    processo2.join()

    print("Todos os processos finalizados.")

if __name__ == "__main__":
    print("Pai: PID = ", os.getpid)
    p1 = Process(target= mostrar_ids)
    p2 = Process(target= mostrar_ids)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Processo Pai finalizado!")

if __name__ == "__main__":
    inicio_paralelo = time.perf_counter()

    b1 = Process(target= calcular_operacao_intensiva, args= (1,))
    b2 = Process(target= calcular_operacao_intensiva, args= (2,))

    b1.start()
    b2.start()

    b1.join()
    b2.join()

    fim_paralelo = time.perf_counter()

    inicio_sequencial = time.perf_counter()

    calcular_operacao_intensiva(3)
    calcular_operacao_intensiva(4)

    fim_sequencial = time.perf_counter()

    print(f"tempo paralelo: {fim_paralelo - inicio_paralelo:.2f} segundos")
    print(f"tempo sequencial: {fim_sequencial - inicio_sequencial:.2f} segundos")

    diferenca = (fim_paralelo - inicio_paralelo) - (fim_sequencial - inicio_sequencial)

    print(f"Diferença: {diferenca:2f} segundos a favor do paralelismo")
