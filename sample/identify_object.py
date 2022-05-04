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

    arq_imagem = open('Figuras/'+nome_img, 'w')

    # escrever cabeçalho
    for conteudo in cabecalho:
        arq_imagem.write(conteudo)

    for i in range(alt):
        for j in range(larg):
            pixel = str(imagem[i][j])+'\n'
            arq_imagem.write(pixel)

    arq_imagem.close()
