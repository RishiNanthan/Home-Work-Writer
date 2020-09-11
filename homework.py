import cv2
import numpy as np
import random


def main():
    capital = cv2.imread('D:\\Pictures\\capital.jpg')
    small = cv2.imread('D:\\Pictures\\small2.jpg')
    small = cv2.resize(small, (1000, 1000))
    cv2.imshow('img', small)
    arr = []
    for i in range(2*26):
        arr += [cv2.selectROI('img', small)]
    arr = np.array(arr)
    np.save('lowers2.npy', arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def check():
    arr = np.load('lowers2.npy')
    small = cv2.imread('D:\\Pictures\\small2.jpg')
    small = cv2.resize(small, (1000, 1000))
    small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(small, 150, 255, cv2.THRESH_BINARY)
    letters = []
    for letter in arr:
        img = small[letter[1]:letter[1]+letter[3], letter[0]:letter[0]+letter[2]]
        img = cv2.resize(img, (200, 200))
        _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        letters += [img]
    cv2.destroyAllWindows()
    letters = np.array(letters)
    np.save('small_letters2.npy', letters)


def check_letters():
    letters = np.load('symbols.npy', allow_pickle=True)
    print(len(letters))
    for letter in letters:
        print(letter[0])
        cv2.imshow('img', letter[1])
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_letters():
    capital = np.load('capital_letters.npy')
    small = list(np.load('small_letters.npy')) + list(np.load('small_letters2.npy'))
    number = np.load('numbers.npy')
    symbol = np.load('symbols.npy', allow_pickle=True)

    letter_dictionary = {}

    letters = capital
    for i in range(len(letters)):
        if i <= 25:
            letter_dictionary[chr(ord('A')+i)] = [letters[i]]
        else:
            i = i % 26
            letter_dictionary[chr(ord('A')+i)] += [letters[i]]

    letters = small
    for i in range(len(letters)):
        if i <= 25:
            letter_dictionary[chr(ord('a')+i)] = [letters[i]]
        else:
            i = i % 26
            letter_dictionary[chr(ord('a')+i)] += [letters[i]]

    letters = number
    for i in range(len(letters)):
        if i < 10:
            letter_dictionary[chr(ord('0')+i)] = [letters[i]]
        else:
            i = i % 10
            letter_dictionary[chr(ord('0')+i)] += [letters[i]]

    for i, j in symbol:
        letter_dictionary[i] = [j]

    return letter_dictionary


def write_home_work(src: str, des='', height=900, width=900):
    word = open(src, 'r').read()
    # word = "Hello World "
    letters = load_letters()
    x = height//10
    y = width//20
    i = 0
    pg_no = 0

    while i < len(word):
        img = np.zeros((height, width), dtype=np.uint8)
        while i < len(word):

            if x+100 >= height:
                x = height // 10
                y = width // 20
                break

            if y+50 >= width:
                y = width//20
                x += 50

            letter = word[i]
            i += 1

            caps = False
            num = False
            small = False
            sym = False

            asc = ord(letter)

            if letter == ' ':
                y += 20
                continue

            elif letter == '\n':
                x += 50
                y = width // 20
                continue

            elif letter not in letters.keys():
                print(letter)
                continue

            elif ord('a') <= asc <= ord('z'):
                small = True
            elif ord('0') <= asc <= ord('9'):
                num = True
            elif ord('A') <= asc <= ord('Z'):
                caps = True
            else:
                sym = True

            ind = random.randrange(len(letters[letter]))
            letter_img = letters[letter][ind]

            if small or num or sym:
                letter_img = cv2.resize(letter_img, (30, 30))
                if small and letter in ['p', 'q', 'g', 'f', 'j', 'y']:
                    img[x+15: x+45, y: y+30] = cv2.bitwise_or(img[x+15: x+45, y:y+30], letter_img)
                else:
                    img[x+10: x+40, y:y+30] = cv2.bitwise_or(img[x+10: x+40, y: y+30], letter_img)
                y += 20

            elif caps:
                letter_img = cv2.resize(letter_img, (40, 40))
                img[x: x+40, y: y+40] = cv2.bitwise_or(img[x: x+40, y: y+40], letter_img)
                y += 30

        _, thr = cv2.threshold(img, 126, 255, cv2.THRESH_BINARY)
        thr = np.reshape(thr, (height, width, 1))
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :, 0:1] = thr
        img[np.where((img == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
        img[np.where((img == [255, 0, 0]).all(axis=2))] = [139, 0, 0]
        cv2.imwrite(f'{des}\\{pg_no}.jpg', img)
        pg_no += 1


if __name__ == '__main__':
    write_home_work("D:\\assignments\\IP\\ipu4.txt", "D:\\assignments\\IP", 2000, 1000)
