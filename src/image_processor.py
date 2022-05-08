# Dependências
import matplotlib.pyplot as plt
import numpy as np
import random

class ImageProcessor:
    # Função para limpar comentários
    def clearComment(matrix_img):
        cont = 0
        comments = []
        for line in matrix_img:
            if '#' in line:
                cont = 0
                comments.append(line)

            elif cont >= 4:
                break

            else:
                cont += 1

        for comment in comments:
            matrix_img.remove(comment)

        return matrix_img

    # Função para obtenção de imagens em  uma matriz
    def getImageP1(name_img):
        file_img = open(name_img, 'r')
        matrix_img = file_img.readlines()

        matrix_img = clearComment(matrix_img)

        # Tipo de arquivo
        type_img = matrix_img[0][0:2]

        # Obtenção da largura e altura da imagem
        line_size = matrix_img[1].replace('\n', '').split()
        larg, alt = int(line_size[0]), int(line_size[1])

        # Obtenção da matriz da imagem pura, sem cabeçalho e em uma lista
        ini = 2
        image = []
        for i in range(alt):
            line = []
            for j in range(ini, ini + larg):
                line.append(int(matrix_img[j]))
            image.append(line)
            ini += larg

        image_np = np.array(image)
        file_img.close()

        return (type_img, larg, alt, image_np)

    # Função que salva uma matriz como imagem
    def saveImage(type_img, larg, alt, image):
        name_img = "imagem" + str(random.randint(0, 10000)) + ".pgm"
        type_img = type_img + "\n"
        size = str(larg) + " " + str(alt) + "\n"
        header = [type_img, size]

        file_img = open('result/'+name_img, 'w')

        # Escreve o cabeçalho
        for content in header:
            file_img.write(content)

        for i in range(alt):
            for j in range(larg):
                pixel = str(image[i][j]) + '\n'
                file_img.write(pixel)

        file_img.close()

    # Função que dilata a imagem
    def dilateEffect(image, larg, alt, elem_struct):
        # Informações do elemento estruturante
        larg_elem = len(elem_struct[0])
        alt_elem = len(elem_struct)
        center = int(alt_elem / 2)

        img_res = image.copy()

        for i in range(1, alt-center):

            for j in range(1, larg-center):
                ver = False

                for ie in range(alt_elem):

                    for je in range(larg_elem):
                        n_i = (i-1) + ie
                        n_j = (j-1) + je

                        if (elem_struct[ie][je] != 0) and (image[n_i][n_j] == elem_struct[ie][je]):
                            img_res[i - 1 + center][j - 1 + center] = elem_struct[center][center]
                            ver = True
                            break

                    if ver:
                        break

        return img_res

    # Realiza a operação de subtração entre duas imagens
    def subtractionEffect(image1, image2):
        img_res = abs(image1 - image2)
        return img_res

    # Identifica as bordas dos objetos na imagem
    def identifyBorder(name_img):
        type_img, larg, alt, image = getImageP1(name_img)

        image_copy = image.copy()
        elem_struct = np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]])

        image_dilated = dilateEffect(image_copy, larg, alt, elem_struct)
        image_sub = subtractionEffect(image_dilated, image_copy)

        saveImage(type_img, larg, alt, image_sub)

    # Identifica a quantidade de polígonos presentes na imagem
    def identifyPolygon(img_name):
        tipo_img, larg, alt, image = getImageP1(img_name)

        # Percorre as coordenadas salvando os pixels pretos formando as linhas
        coord = []
        for i in range(alt):

            for j in range(larg):

                if image[i][j] == 1:
                    coord.append([i, j])

        # Ordena as coordenadas
        coord.sort()

        # Matriz de retas
        lines = [[]]
        num_lines = 0

        for c in range(len(coord)):
            i, j = coord[c]
            # Verifica uma posição afrente, diagonal inferiro direita, diagonal inferior esquerda, diagonal superior esquerda e diagonal superior direita, respctivamente
            if (([i, j + 1] in coord) or ([i + 1, j + 1] in coord) or ([i + 1, j - 1] in coord) or ([i - 1, j - 1] in coord) or ([i - 1, j + 1] in coord)):
                lines[num_lines].append([i, j])
            
            else:
                lines[num_lines].append([i, j])
                lines.append([])
                num_lines += 1

        # Contagem de polígonos
        count = 0

        # Lista de polígonos
        polygons = []

        # Coordenadas
        x = []
        y = []
        for line in lines:
            if len(line) > 10:
                polygons.append(line)
                y.append(line[0])
                x.append(line[1])
                count += 1

        print(count)