import sys
import copy
import random
import math
import heapq

custos = {}
maxGer = 0

class vertice:
    def __init__(self, indice, x, y):
        self.indice = indice
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return "indice:% s x:% s y:% s" % (self.indice, self.x, self.y)


class Solucao:
    def __init__(self, caminho = [], custo = -1):
        self.caminho = caminho
        self.custo = custo

    def __lt__(self, other):
        return self.custo < other.custo



def dist_euclidiana(v1, v2):
    return math.sqrt(pow(v1.x - v2.x, 2) + pow(v1.y - v2.y, 2)) 


def custo(vertices):
    global custos

    tupla_vertices = tuple(vertices)
    
    if tupla_vertices not in custos:
        soma = 0

        for i in range(len(vertices)):
            if i != len(vertices) - 1:
                soma += dist_euclidiana(vertices[i], vertices[i+1])
            else:
                soma += dist_euclidiana(vertices[i], vertices[0])

        custos[tupla_vertices] = soma

    return custos[tupla_vertices]

# Pra calcular o custo utilizar distancha euclediana entre cada vertice
# Talvez utilizar tecnica de memo pra salvar os custos ja calculados pra soluções iguais
# calcular o custo de cada vertice para todos os outros

def getCoordenadas(index, arquivo):
    lista = arquivo[index+1:len(arquivo)-1]
    listaVertices = []

    for v in lista:
        coordenada = v.strip().split(" ")
        novaCoordenada = list(filter(("").__ne__,coordenada))
        listaVertices.append(vertice(novaCoordenada[0],novaCoordenada[1],novaCoordenada[2].replace("\n","")))

    return listaVertices


def select(populacao):
    randomIndex1 = random.randint(0, len(populacao)//2)
    randomIndex2 = random.randint(0, len(populacao)//2)
    randomIndex3 = random.randint(0, len(populacao)//2)
    
    if populacao[randomIndex1].custo < populacao[randomIndex2].custo and populacao[randomIndex1].custo < populacao[randomIndex3].custo:
        return populacao[randomIndex1]
    elif populacao[randomIndex2].custo < populacao[randomIndex1].custo and populacao[randomIndex2].custo < populacao[randomIndex3].custo:
        return populacao[randomIndex2]
    else:
        return populacao[randomIndex3]


def crossover(pai1, pai2):
    caminho1 = pai1.caminho
    caminho2 = pai2.caminho

    tamCorte = int(len(caminho1) * 0.7)

    filho1 = caminho1[:tamCorte]
    filho2 = caminho2[:tamCorte]

    aux1 = list(set(caminho1) - set(filho1))
    aux2 = list(set(caminho2) - set(filho2))

    for x in aux1:
        filho1.append(x)

    for x in aux2:
        filho2.append(x)

    filho1 = mutation(filho1)
    filho2 = mutation(filho2)

    solucao1 = firstImprovement(Solucao(filho1, custo(filho1)))
    solucao2 = firstImprovement(Solucao(filho2, custo(filho2)))

    return solucao1, solucao2


def mutation(filho):
    v1 = random.randint(0, len(filho) - 1)
    v2 = random.randint(v1, len(filho) - 1)

    filho[v1], filho[v2] = filho[v2], filho[v1]

    return filho


def generatorNeighboor(solucao, i):
    novaSolucao = copy.deepcopy(solucao)
    novaSolucao.caminho[i], novaSolucao.caminho[i+1] = novaSolucao.caminho[i+1], novaSolucao.caminho[i]
    novaSolucao.custo = custo(novaSolucao.caminho)
    return novaSolucao


def firstImprovement(solucao):
    melhoria = False
    novaSolucao = solucao
    i = 0

    while not melhoria and i < len(solucao.caminho):
        vizinho = generatorNeighboor(solucao, i)

        if (vizinho.custo < solucao.custo):
            novaSolucao = vizinho
            melhoria = True
        
        i += 1

    return novaSolucao


def updatePopulation(populacao, solucao):
    global maxGer
    maiorSolucao = heapq.nlargest(1, populacao)[0]

    if maiorSolucao.custo > solucao.custo:
        heapq.heappush(populacao, solucao)
        maxGer += 1

    return populacao    


def geneticTsp(vertices):
    global maxGer
    populacao = [] ## lista de soluções
    heapq.heapify(populacao)

    heapq.heappush(populacao, Solucao(vertices, custo(vertices)))

    secondSon = copy.deepcopy(vertices)
    random.shuffle(secondSon)

    #populacao.append(Solucao(secondSon, custo(secondSon)))
    heapq.heappush(populacao, Solucao(secondSon, custo(secondSon)))

    while maxGer < 1000: ## condição de parada
        print('maxGer:', maxGer)
        ## toda vez que adicionar uma geração incrementar o maxGer

        # Selecao por Torneio
        pai1 = select(populacao)
        pai2 = select(populacao)
        
        # Cruzamento, mutacao e busca local
        solucao1, solucao2 = crossover(pai1, pai2)

        # att da population
        populacao = updatePopulation(populacao, solucao1)
        populacao = updatePopulation(populacao, solucao2)

    menorSolucao = heapq.nsmallest(1, populacao)[0]
    maiorSolucao = heapq.nlargest(1, populacao)[0]
    print('Maior custo:', maiorSolucao.custo)
    print('Menor custo:', menorSolucao.custo)




def main(arquivoEntrada):
    random.seed()

    f = open(arquivoEntrada, "r")
    arquivo = f.readlines()

    nome = ""
    tipo = ""
    comentario = ""
    dimensao = 0
    tipoVertice = ""
    vertices = []

    for linha in arquivo:
        if "NAME" in linha:
            nome = linha.split(": ")[1]
        elif "TYPE" in linha:
            tipo = linha.split(": ")[1]
        elif "COMMENT" in linha:
            comentario = linha.split(": ")[1]
        elif "DIMENSION" in linha:
            dimensao = linha.split(": ")[1]
        elif "EDGE_WEIGHT_TYPE" in linha:
            tipoVertice = linha.split(": ")[1]
        elif "NODE_COORD_SECTION":
            vertices = getCoordenadas(arquivo.index(linha), arquivo)
            break

    geneticTsp(vertices)


main(sys.argv[1])