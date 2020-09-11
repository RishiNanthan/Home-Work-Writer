import cv2
import numpy as np


def draw_line(image1, des: str, color=(0, 0, 0), thickness=3):

    def callback(event, x, y, flag, param):
        line = param[0]
        tem = param[2]
        if event == 1:
            line += [(x, y)]
        elif event == 4:
            line += [(x, y)]
        else:
            tem[0] = x
            tem[1] = y

    line_pos = []
    temp = [0, 0]

    x = 1
    if image1.shape[0] > 600 or image1.shape[1] > 600:
        x = max(image1.shape[0]//600, image1.shape[1]//600)

    while True:
        image = np.copy(image1)
        img = cv2.resize(image, (image.shape[0] // x, image.shape[1] // x))

        lines = line_pos
        if len(line_pos) % 2:
            lines = (line_pos+[tuple(temp)]).copy()

        for i in range(len(lines)//2):
            pos = (i * 2)
            pos1 = list(lines[pos])
            pos1[0] *= x
            pos1[1] *= x
            pos1 = tuple(pos1)

            pos2 = list(lines[pos+1])
            pos2[0] *= x
            pos2[1] *= x
            pos2 = tuple(pos2)

            image = cv2.line(image, pos1, pos2, color, thickness)

        img = cv2.resize(image, (image.shape[0] // x, image.shape[1] // x))
        cv2.imshow('Draw Line', img)
        cv2.setMouseCallback('Draw Line', callback, (line_pos, img, temp))
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cv2.imshow('Click S to Save', img)
    if cv2.waitKey(0) & 0xFF == ord('s'):
        cv2.imwrite(des, image)
    cv2.destroyAllWindows()


def main():
    img = cv2.imread('D:\\sample.jpg')
    draw_line(img, "D:\\sample1.jpg", (0, 0, 0), 2)


if __name__ == '__main__':
    main()
