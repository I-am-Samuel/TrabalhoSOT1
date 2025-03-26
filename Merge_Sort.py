import os
import glob
import time
import matplotlib.pyplot as plt
from multiprocessing import Pool

# Função para ler arquivos dentro das pastas
def carregar_arquivos_da_pasta(pasta):
    arquivos = glob.glob(os.path.join(pasta, "*.txt"))
    listas = []

    for arquivo in arquivos:
        with open(arquivo, 'r') as f:
            dados = [int(linha.strip()) for linha in f.readlines()]
            listas.append(dados)

    return listas

# Função Merge Sort Sequencial
def merge_sort_sequencial(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort_sequencial(left)
        merge_sort_sequencial(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# Função Merge Sort Paralelo
def merge_sort_paralelo(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        with Pool(2) as pool:
            pool.map(merge_sort_sequencial, [left, right])

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# Função para medir o tempo de execução
def medir_tempo(algoritmo, arr):
    start = time.time()
    algoritmo(arr)
    return time.time() - start

# Função principal para rodar as rodadas de testes
def rodar_rodadas(algoritmo, listas, n_rodadas=10):
    tempos = []
    for dados in listas:
        for _ in range(n_rodadas):
            dados_copy = dados.copy()
            tempos.append(medir_tempo(algoritmo, dados_copy))
    return tempos

# Função para gerar Box Plots para listas pequenas e grandes
def gerar_box_plots(tempos_sequencial, tempos_paralelo, arquivos, tipo):
    plt.figure(figsize=(15, 8))

    # Agrupar tempos por arquivo
    tempos_sequencial_agrupados = [tempos_sequencial[i::len(arquivos)] for i in range(len(arquivos))]
    tempos_paralelo_agrupados = [tempos_paralelo[i::len(arquivos)] for i in range(len(arquivos))]

    # Plotar box plots
    posicoes_seq = range(1, len(arquivos) + 1)
    posicoes_par = range(len(arquivos) + 2, 2 * len(arquivos) + 2)

    plt.boxplot(tempos_sequencial_agrupados, labels=arquivos, patch_artist=True, positions=posicoes_seq)
    plt.boxplot(tempos_paralelo_agrupados, labels=arquivos, patch_artist=True, positions=posicoes_par)

    # Adicionar "Sequencial" e "Paralelo" na legenda
    for pos, arq in zip(posicoes_seq, arquivos):
        plt.text(pos, max(tempos_sequencial_agrupados[pos - 1]), f'Seq: {arq}', ha='center', va='bottom', fontsize=8, rotation=45)

    for pos, arq in zip(posicoes_par, arquivos):
        plt.text(pos, max(tempos_paralelo_agrupados[pos - len(arquivos) - 2]), f'Par: {arq}', ha='center', va='bottom', fontsize=8, rotation=45)

    plt.title(f'Comparação entre Merge Sort Sequencial e Paralelo - {tipo}')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.xticks([sum(posicoes_seq) / len(posicoes_seq), sum(posicoes_par) / len(posicoes_par)], ['Sequencial', 'Paralelo'], rotation=0)
    plt.show()

# Bloco principal para execução
if __name__ == "__main__":
    pasta_pequenas = 'listas_pequenas'
    pasta_grandes = 'listas_grandes'

    # Carregar os arquivos das pastas
    listas_pequenas = carregar_arquivos_da_pasta(pasta_pequenas)
    listas_grandes = carregar_arquivos_da_pasta(pasta_grandes)

    # Obter os nomes dos arquivos
    arquivos_pequenas = [os.path.basename(arquivo) for arquivo in glob.glob(os.path.join(pasta_pequenas, "*.txt"))]
    arquivos_grandes = [os.path.basename(arquivo) for arquivo in glob.glob(os.path.join(pasta_grandes, "*.txt"))]

    # Rodar os algoritmos nas listas pequenas e grandes
    tempos_sequencial_pequenas = rodar_rodadas(merge_sort_sequencial, listas_pequenas)
    tempos_sequencial_grandes = rodar_rodadas(merge_sort_sequencial, listas_grandes)
    tempos_paralelo_pequenas = rodar_rodadas(merge_sort_paralelo, listas_pequenas)
    tempos_paralelo_grandes = rodar_rodadas(merge_sort_paralelo, listas_grandes)

    # Gerar gráficos para listas pequenas
    gerar_box_plots(
        tempos_sequencial_pequenas,
        tempos_paralelo_pequenas,
        arquivos_pequenas,
        tipo='Listas Pequenas'
    )

    # Gerar gráficos para listas grandes
    gerar_box_plots(
        tempos_sequencial_grandes,
        tempos_paralelo_grandes,
        arquivos_grandes,
        tipo='Listas Grandes'
    )