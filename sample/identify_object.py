import numpy as np
import random
import matplotlib.pyplot as plt

# funcao limpa comentarios


def clearComment(matriz_img):
    cont = 0
    comentarios = []
    for linha in matriz_img:
        if '#' in linha:
            cont = 0
            comentarios.append(linha)
        elif cont >= 4:
            break
        else:
            cont += 1

    for comentario in comentarios:
        matriz_img.remove(comentario)

    return matriz_img

# funcao para obtenção de imagem em matriz


def getImageP1(nome_img):

    arquivo_img = open(nome_img, 'r')
    matriz_img = arquivo_img.readlines()

    matriz_img = clearComment(matriz_img)

    # tipo de arquivo
    tipo_img = matriz_img[0][0:2]

    # obtenção de largura e altura da imagem
    linha_tam = matriz_img[1].replace('\n', '').split()
    larg, alt = int(linha_tam[0]), int(linha_tam[1])

    # obtenção de matriz imagem pura sem cabeçalho e em lista
    imagem = []
    ini = 2
    for i in range(alt):
        linha = []
        for j in range(ini, ini+larg):
            linha.append(int(matriz_img[j]))
        imagem.append(linha)
        ini += larg

    imagem_np = np.array(imagem)
    arquivo_img.close()

    return (tipo_img, larg, alt, imagem_np)

# funcao que salva uma matriz como imagem


def saveImage(tipo_img, larg, alt, imagem):
    nome_img = "imagem"+str(random.randint(0, 10000))+".pgm"
    tipo_img = tipo_img+"\n"
    tam = str(larg)+" "+str(alt)+"\n"
    cabecalho = [tipo_img, tam]

    arq_imagem = open('result/'+nome_img, 'w')

    # escrever cabeçalho
    for conteudo in cabecalho:
        arq_imagem.write(conteudo)

    for i in range(alt):
        for j in range(larg):
            pixel = str(imagem[i][j])+'\n'
            arq_imagem.write(pixel)

    arq_imagem.close()

# funcao que dilata a imagem


def dilateEffect(imagem, larg, alt, elem_estru):

    # informacoes do elemento estruturante
    larg_elem = len(elem_estru[0])
    alt_elem = len(elem_estru)
    centro = int(alt_elem/2)

    img_res = imagem.copy()

    for i in range(1, alt-centro):
        for j in range(1, larg-centro):
            ver = False
            for ie in range(alt_elem):
                for je in range(larg_elem):
                    n_i = (i-1) + ie
                    n_j = (j-1) + je

                    if (elem_estru[ie][je] != 0) and (imagem[n_i][n_j] == elem_estru[ie][je]):
                        img_res[i-1 + centro][j-1 +
                                              centro] = elem_estru[centro][centro]
                        ver = True
                        break
                if ver:
                    break

    return img_res

# realiza a operacao de subtração entre duas imagens
def subtractionEffect(imagem1, imagem2):
    img_res = abs(imagem1 - imagem2)

    return img_res

# identifica as bordas dos objetos na imagem
def identifyBorder(img_name):
    tipo_img, larg, alt, imagem = getImageP1(img_name)

    imagem_copy = imagem.copy()
    elem_estru = np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]])

    imagem_dilatada = dilateEffect(imagem_copy, larg, alt, elem_estru)
    imagem_sub = subtractionEffect(imagem_dilatada, imagem_copy)

    saveImage(tipo_img, larg, alt, imagem_sub)

# identifica a quantidade de poligonos presentes na imagem
def identifyPolygon(img_name):
    tipo_img, larg, alt, imagem = getImageP1(img_name)

    coord = []
    for i in range(alt):
        for j in range(larg):
            if imagem[i][j] == 1:
                coord.append([i,j])
    coord.sort()
    retas = [[]]
    n_retas = 0
    
    for c in range(len(coord)):
        i,j = coord[c]
        if (([i,j+1] in coord) or ([i+1,j+1] in coord) or ([i+1, j-1] in coord) or ([i-1, j-1] in coord) or ([i-1, j+1] in coord)):
            retas[n_retas].append([i,j])
        else:
            retas[n_retas].append([i,j])
            retas.append([])
            n_retas += 1

    count = 0
    polygon = []
    x = []
    y = []
    for reta in retas:
        if len(reta) > 10:
            polygon.append(reta)
            y.append(reta[0])
            x.append(reta[1])
            count += 1

    print(count)
    
    




