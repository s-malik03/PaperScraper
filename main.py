import pytesseract
from PIL import Image
import fitz
from googlesearch import search
import nltk

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:

    config = open('config.txt','r')
    line = config.readline()
    line=line.replace('\n','')
    line = line.split('=')
    pytesseract.pytesseract.tesseract_cmd = line[1]
    line = config.readline()
    line = line.replace('\n', '')
    line = line.split('=')
    if line[1] == 'no':
        nltk.download('punkt')
    config.close()

except:

    print("Error Loading Config")
    exit()


def main():
    filename = input('Enter pdf file name:')
    pdf = fitz.open(filename)
    img = 0
    matrix = fitz.Matrix(3.0, 3.0)

    for page in pdf:
        image_file = "page" + str(img) + ".png"
        img += 1
        pixels = page.get_pixmap(alpha=False, matrix=matrix)
        pixels.writePNG(image_file)

    img_lim = img
    text = open(filename.replace('.pdf', '.txt'), 'w')

    start = int(input("Enter page number to start from (starting from 0):"))

    for i in range(start, img_lim):
        image_file = "page" + str(i) + ".png"
        textdata = str((pytesseract.image_to_string(Image.open(image_file))))
        textdata = textdata.replace('-\n', '')
        textdata = textdata.replace(' \n', ' ')
        text.write(textdata)

    text.close()
    text = open(filename.replace('.pdf', '.txt'), 'r')
    textdata = text.read()
    textdata = nltk.tokenize.sent_tokenize(textdata)

    for block in textdata:

        block = block.replace('\n', '')

        for result in search(block, num=1):
            print(result)


if __name__ == '__main__':
    main()
