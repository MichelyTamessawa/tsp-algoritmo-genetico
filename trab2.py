import sys


class vertice:
    def __init__(self, indice, x, y):
        self.indice = indice
        self.x = x
        self.y = y

    def __str__(self):
        return "indice:% s x:% s y:% s" % (self.indice, self.x, self.y)


def getCoordenadas(index, arquivo):
    lista = arquivo[index+1:len(arquivo)-1]
    listaVertices = []

    for v in lista:
        coordenada = v.strip().split(" ")
        novaCoordenada = list(filter(("").__ne__,coordenada))
        listaVertices.append(vertice(novaCoordenada[0],novaCoordenada[1],novaCoordenada[2].replace("\n","")))


def main(arquivoEntrada):
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
            getCoordenadas(arquivo.index(linha), arquivo)
            break


main(sys.argv[1])