# Dependências
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os

# Função para limpar comentários
def clearComment(img_matrix):
    count = 0
    comments = []
    for line in img_matrix:
        if '#' in line:
            count = 0
            comments.append(line)

        elif count >= 4:
            break

        else:
            count += 1

    for comment in comments:
        img_matrix.remove(comment)

    return img_matrix

# Função para obtenção de imagens em  uma matriz
def getImageP1(img_name):
    img_file = open(img_name, 'r')
    img_matrix = img_file.readlines()

    img_matrix = clearComment(img_matrix)

    # Tipo de arquivo
    type_img = img_matrix[0][0:2]

    # Obtenção da largura e altura da imagem
    line_size = img_matrix[1].replace('\n', '').split()
    width, height = int(line_size[0]), int(line_size[1])

    # Obtenção da matriz da imagem pura, sem cabeçalho e em uma lista
    ini = 2
    image = []
    for i in range(height):
        line = []

        for j in range(ini, ini + width):
            line.append(int(img_matrix[j]))

        image.append(line)
        ini += width

    image_np = np.array(image)
    img_file.close()

    return (type_img, width, height, image_np)

# Função que salva uma matriz como imagem
def saveImage(type_img, width, height, image):
    img_name = "imagem" + str(random.randint(0, 10000)) + ".pgm"
    type_img = type_img + "\n"
    size = str(width) + " " + str(height) + "\n"
    header = [type_img, size]

    file_img = open('../results/'+img_name, 'w')

    # Escreve o cabeçalho
    for content in header:
        file_img.write(content)

    for i in range(height):

        for j in range(width):
            pixel = str(image[i][j]) + '\n'
            file_img.write(pixel)

    file_img.close()

# Função que dilata a imagem
def dilateEffect(image, width, height, elem_struct):
    # Informações do elemento estruturante
    elem_width = len(elem_struct[0])
    elem_height = len(elem_struct)
    center = int(elem_height / 2)

    # Cópia da imagem
    img_res = image.copy()

    for i in range(1, height - center):

        for j in range(1, width - center):
            check = False

            for ie in range(elem_height):

                for je in range(elem_width):
                    n_i = (i-1) + ie
                    n_j = (j-1) + je

                    if (elem_struct[ie][je] != 0) and (image[n_i][n_j] == elem_struct[ie][je]):
                        img_res[i - 1 + center][j - 1 + center] = elem_struct[center][center]
                        check = True
                        break

                if check:
                    break

    return img_res

# Realiza a operação de subtração entre duas imagens
def subtractionEffect(image1, image2):
    img_res = abs(image1 - image2)
    return img_res

# Identifica as bordas inferiores dos objetos na imagem
def identifyBorder(img_name):
    type_img, width, height, image = getImageP1(img_name)

    image_copy = image.copy()
    elem_struct = np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]])

    dilated_image = dilateEffect(image_copy, width, height, elem_struct)
    subtracted_image = subtractionEffect(dilated_image, image_copy)

    saveImage(type_img, width, height, subtracted_image)

    return (type_img, width, height, subtracted_image)
      
# Identifica a quantidade de polígonos presentes na imagem
def identifyPolygon(img_type, width, height, image, img_name):
    
    # Percorre as coordenadas salvando os pixels pretos formando as linhas
    coord = []
    for i in range(height):

        for j in range(width):

            if image[i][j] == 1:
                coord.append([i, j])

    # Ordena as coordenadas
    coord.sort()
    coord_copy = coord.copy()
    
    # Matriz de retas
    lines = [[]]
    num_lines = 0

    # Identificacao de retas continuas dos poligonos   
    while len(coord_copy) != 0:
        i, j = coord_copy[0]

        checks = 10
        old_check = 10 

        while checks != 0:
               
            if ([i, j + 1] in coord_copy):
                lines[num_lines].append([i, j])
                coord_copy.remove([i, j])
                j = j + 1
                checks += 1
                    
            if ([i + 1, j + 1] in coord_copy):
                lines[num_lines].append([i, j])
                coord_copy.remove([i, j])
                i = i + 1
                j = j + 1
                checks += 1

            if ([i + 1,j] in coord_copy):
                lines[num_lines].append([i, j])
                coord_copy.remove([i, j])
                i = i + 1
                checks += 1

            if ([i - 1, j] in coord_copy):
                lines[num_lines].append([i, j])
                coord_copy.remove([i, j])
                i = i - 1
                checks += 1

            if ([i - 1, j + 1] in coord_copy):
                lines[num_lines].append([i, j])
                coord_copy.remove([i, j])
                i = i - 1
                j = j + 1
                checks += 1

            checks = checks - old_check 
            old_check = checks

        lines[num_lines].append([i, j])
        coord_copy.remove([i,j])

        lines.append([])
        num_lines += 1

    # Contagem de polígonos
    count = 0

    # Lista de polígonos e buracos
    polygons = []
    holes = []
    
    # Coordenadas
    coord_lines = []
    coord_holes = []
    
    for line in lines:
        if len(line) > 10:
            polygons.append(line)
            coord = [[], []]
            
            for pair in line:
                coord[0].append(648 - pair[0])
                coord[1].append(pair[1])

            coord_lines.append(coord)
            count += 1
               
        elif len(line) > 6:
            holes.append(line)
    
    # Lista de remoções
    removed = []

    # Referência para o polígono
    polygon_id = 1

    # Número de poligonos com buracos
    polygons_holes_num = 0
    
    for polygon in polygons:
        holes_num = 0
        
        meio = int(len(polygon)/2)
        
        for hole in holes:
            isIn = (polygon[0][1] < hole[0][1] < polygon[-1][1]) and (polygon[meio][0] > hole[0][0])
            
            if (isIn and not(hole in removed)):
                
                holes_num += 1
                removed.append(hole)

                coor = [[], []]
            
                for pair in hole:
                    coor[0].append(648 - pair[0])
                    coor[1].append(pair[1])

                    coord_holes.append(coor)

        if holes_num > 0:
            polygons_holes_num += 1
            
        print("Polígono " + str(polygon_id) + "- n° de buracos: " + str(holes_num))

        polygon_id += 1
    
    for y, x in coord_lines:
        plt.plot(x,y)

    for y,x in coord_holes:
        plt.plot(x,y)

    graph_name = img_name[10:]
    graph_name = "./../results" + graph_name[:-4] + "_grafico"+".png"
    
    plt.savefig(graph_name, dpi=300)
    plt.close()

    print("---------------------- Geral --------------------------")
    print("N° de polígonos com buracos: " + str(polygons_holes_num))
    print("N° de polígonos sem buracos: " + str(count - polygons_holes_num))
    print("Total de polígonos: " + str(count))
    print("Total de buracos: " + str(len(holes)))
    print()

# Main
start_time = time.time()
images_path = "./../tests/"
walk = list(os.walk(images_path))
_,_,files = walk[0]

for file in files:
    print("Imagem " + str(file))
    
    img_name = images_path + file
    
    img_type, width, height, image = identifyBorder(img_name)
    identifyPolygon(img_type, width, height, image, img_name)
 
final_time = time.time()
total_time = final_time - start_time
print("\nTempo total de execução: %.3f ms" %total_time)