"""PaperScraper, a program designed to google relevant sources on the web based on the contents of the paper
Copyright (C) 2021  Safiy Ahmad Malik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

import pytesseract
from PIL import Image
import fitz
from googlesearch import search
import nltk

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:

    config = open('config.txt', 'r')
    line = config.readline()
    line = line.replace('\n', '')
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
        textdata = textdata.replace('...', '')
        text.write(textdata)

    text.close()
    text = open(filename.replace('.pdf', '.txt'), 'r')
    textdata = text.read()
    special_separator = input('Enter any custom separator (i.e. ?,>,|) or leave blank for none:')

    if special_separator != '':

        textdata = textdata.replace(special_separator, '{!$&)}')

    for marks in range(1, 30):

        textdata = textdata.replace('[' + str(marks) + ']', '{!$&)}')
        textdata = textdata.replace('[Turn over', '{!$&)}')

    textdata = textdata.split('{!$&)}')

    # textdata = nltk.tokenize.sent_tokenize(textdata)

    links = open('links.txt', 'w')

    for block in textdata:

        block = block.replace('\n', '')
        print(block)
        links.write(block + '\n')

        for result in search(block, num=1, stop=1, pause=2.0):
            print(result)
            links.write(result + '\n')


if __name__ == '__main__':
    main()
