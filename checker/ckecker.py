from PIL import Image, ImageChops
from os import listdir, rename
from os.path import isdir, isfile, join

ref_header = Image.open("header.png")
ref_0 = Image.open("0.png")
ref_1 = Image.open("1.png")
ref_2 = Image.open("2.png")
ref_3 = Image.open("3.png")
ref_4 = Image.open("4.png")
ref_5 = Image.open("5.png")
ref_6 = Image.open("6.png")
ref_7 = Image.open("7.png")
ref_8 = Image.open("8.png")
ref_flag = Image.open("flag.png")
covered = Image.open("covered.png")

success_output = "output/success/"
fail_output = "output/anomaly/"


def check_images_in_folder(folder):
    for item in listdir(folder):
        print(join(folder, item))
        if isdir(join(folder, item)):
            check_images_in_folder(join(folder, item))
        elif item.endswith(".png"):
            # check

            if 'beginner' in folder:
                sub = 'beginner_'
            elif 'advanced' in folder:
                sub = 'advanced_'
            elif 'expert' in folder:
                sub = 'expert_'
            elif 'custom' in folder:
                sub = 'custom_'
            else:
                sub = ''

            if check_image(join(folder, item)):
                rename(join(folder, item), join(success_output, sub + item))
            else:
                rename(join(folder, item), join(fail_output, sub + item))


def check_image(path):
    image = Image.open(path)
    width = image.size[0]
    height = image.size[1]

    # ищем заголовок окна
    head_crop = image.crop((2, 2, 39, 24))
    if ImageChops.difference(head_crop, ref_header).getbbox() is not None:
        print(path, "Wrong image header!")
        return False

    # обрезаем заголовок и рамки
    cropped = image.crop((8, 78, width - 8, height - 8))

    # проверяем размер обрезанной картинки
    width = cropped.size[0]
    height = cropped.size[1]
    if width % 16 > 0 or height % 16 > 0:
        print(path, "Wrong cropped size!")

    # вычисляем размеры поля
    cols = width // 16
    rows = height // 16

    # генерируем пустой список
    cells = [[0 for c in range(cols)] for r in range(rows)]

    covered_c = 0

    # распознаем картинку
    for r in range(rows):
        for c in range(cols):
            cell = cropped.crop((16 * c, 16 * r, 16 * c + 15, 16 * r + 15))
            if ImageChops.difference(cell, ref_flag).getbbox() is None:
                cells[r][c] = 'f'
            elif ImageChops.difference(cell, ref_0).getbbox() is None:
                cells[r][c] = 0
            elif ImageChops.difference(cell, ref_1).getbbox() is None:
                cells[r][c] = 1
            elif ImageChops.difference(cell, ref_2).getbbox() is None:
                cells[r][c] = 2
            elif ImageChops.difference(cell, ref_3).getbbox() is None:
                cells[r][c] = 3
            elif ImageChops.difference(cell, ref_4).getbbox() is None:
                cells[r][c] = 4
            elif ImageChops.difference(cell, ref_5).getbbox() is None:
                cells[r][c] = 5
            elif ImageChops.difference(cell, ref_6).getbbox() is None:
                cells[r][c] = 6
            elif ImageChops.difference(cell, ref_7).getbbox() is None:
                cells[r][c] = 7
            elif ImageChops.difference(cell, ref_8).getbbox() is None:
                cells[r][c] = 8
            elif ImageChops.difference(cell, covered).getbbox() is None:
                covered_c += 1
            else:
                print(path, "Wrong cell type detected!")
                return False

    print("Covered", covered_c)

    # проверяем совпадение числа флагов вокруг и указанного числа
    for r in range(rows):
        for c in range(cols):
            if cells[r][c] == 'f':
                continue

            counter = 0
            if c > 0 and r > 0 and cells[r-1][c-1] == 'f':
                counter += 1
            if r > 0 and cells[r-1][c] == 'f':
                counter += 1
            if c < (cols - 1) and r > 0 and cells[r-1][c+1] == 'f':
                counter += 1
            if c > 0 and cells[r][c-1] == 'f':
                counter += 1
            if c < (cols - 1) and cells[r][c+1] == 'f':
                counter += 1
            if c > 0 and r < (rows - 1) and cells[r+1][c-1] == 'f':
                counter += 1
            if r < (rows - 1) and cells[r+1][c] == 'f':
                counter += 1
            if c < (cols - 1) and r < (rows - 1) and cells[r+1][c+1] == 'f':
                counter += 1

            if counter != cells[r][c]:
                return False

    return True

#check_images_in_folder("input")
check_image("359_15_14.png")
