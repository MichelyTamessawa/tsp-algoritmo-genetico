import sys
import copy
import random
import math

class vertice:
    def __init__(self, indice, x, y):
        self.indice = indice
        self.x = x
        self.y = y

    def __str__(self):
        return "indice:% s x:% s y:% s" % (self.indice, self.x, self.y)

class Solucao:
    def __init__(self, caminho = [], custo = -1):
        self.caminho = caminho
        self.custo = custo

    # def __lt__(self, other):
    #     return self.custo() < other.custo()

custos = {}

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

def crossover(vertices):
    print('')

def mutation(vertices):
    print('')

def updatePopulation(vertices):
    print('')

def geneticTsp(vertices):
    maxGer = 0
    populacao = [] ## chave é o caminho da solução e valor é o custo

    populacao.append(Solucao(vertices, custo(vertices)))

    secondSon = vertice.deepcopy()
    random.suffle(secondSon)

    populacao.append(Solucao(secondSon, custo(secondSon)))

    while maxGer < 1000: ## condição de parada
        ## toda vez que adicionar uma geração incrementar o maxGer

        # Selecao por Torneio
        pai1 = select(populacao)
        pai2 = select(populacao)
        
        # Cruzamento

        # att da pop

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