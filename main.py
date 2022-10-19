import numpy as np

from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage.draw import line
from skimage import data
import skimage.io
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
from PIL import Image
from io import BytesIO
import os
from numpy import asarray

from detect_spines import spine_detect
from digtize_spines import get_cropped_images,detect_document
from get_book_info import get_book_info

def get_book_names(path):
    # Constructing test image
    #im = Image.open('img.jpeg')
    img_path = path

    dir = 'images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    image, points = spine_detect(img_path)

    crop_images = get_cropped_images(image, points)

    count = 1
    for crop_image in crop_images:
        pil_image = Image.fromarray(crop_image)
        pil_image.save("images/"+str(count)+"_your_file.jpeg")
        count += 1

    img_text = []
    for filename in sorted(os.listdir('images')):
        txt = detect_document('images/'+filename)
        if not txt == '':
            img_text.append(txt)


    #print(img_text)
    #img_text =["Man's Souch E M", '(Date) Your efforts and intentions will create a huge EIFS Salutes and Commends your commitment to be an Ambassador of this significant and profound Initiative. difference to our Society and ultimately to our Nation.', 'A WORLD ON HOLD A Living Record of the Global Pandemic EDITED BY DIVITA AGGARWAL - SURABHI SUNDARAM Om', 'Yuval Noah Harari Sapiens A Brief History of Humankind VINTAGE', 'INSIDE COCA-COLA Coca-Cola DU V NEVILLE ISDELL WITH DAVID BEASLEY Sa', "WARREN BUFFETT'S GROUND RULES EREM MILLE P", 'Rachel Carson Silent Spring Q MODERN CLASSICS', 'WARREN BUFFETT AND THE INTERPRETATION OF FINANCIAL STATEMENTS MARY BUFFETT & DAVID CLARK SIMON & SCHUSTER', 'LARSSON millennium I The Girl with the Dragon Tattoo int MACLEHOSE Quercus', 'Quiet Susan Cain']
    #img_text =['Alice Bliss Laura Harrington PICADOR', 'EMMA BLAIR FINDING HAPPINESS sphere.', 'HOUSE NIGHT Tempted P.C. and KRISTIN CAST Gas de * atom', "THE SUNDAY TIMES NO.1 BESTSELLING AUTHOR Damien Lewis 500 Piece ies SAS BAND OF BROTHERS THE LAST STAND OF THE SAS AND THEIR HUNT FOR THE NAZI KILLERS 11 ( l l l l l l 'Riveting. Extraordinary. A real-life thriller.' DAN SNOW", 'AK DAN NO', 'ROSIE ARCHER The Gunpowder and Glory Girls', 'Betrayed in Cornwall JANIE BOLITHO', 'Postscript CECELIA AHERN Collins', 'melting ms frost kat black', 'A PERFECT ARRANGEMENT Suzanne Berne', 'A Girl can Dream ANNE BENNETT HANPER', 'Bagshawe WHEN SHE WAS BAD', 'Lynda Bellingham the Boy I Love']
    # # txt = detect_document('images/13_your_file.jpeg')
    # # img_text.append(txt)
    #img_text =['PREDICTABLY IRRATIONAL DAN ARIELY HARPER', "C DOUGLAS ADAMS THE ULTIMATE HITCHHIKER'S GUIDE TO THE GALAXY BALLANTINE BOOKS DEL", "SO YOU'VE BEEN PUBLICLY JON RONSON SHAMED PICADOR", 'Za troso Lsino + >= ₁ √ = = = [√²) 2mw a= би била Gregory Zuckerman n O THE MAN WHO SOLVED THE MARKET HOW JIM SIMONS LAUNCHED THE QUANT REVOLUTION 1 ħ? 2m it (Fil at 4= d 1/1/at = at = F + √₂14₂ >= 18(1 1 {"(!) > € {{ (2, 4) = S < | دے BUSINESS', 'PHILIP A. FISHER COMMON STOCKS AND UNCOMMON PROFITS AND OTHER WRITINGS BY PHILIP A. FISHER W WILEY', 'INFLUENCE ROBERT B. CIALDINI, PH.D. 18 17 HARPER BUSINESS', 'HOW TO WIN FRIENDS & INFLUENCE PEOPLE CARNEGIE A', 'THE INTELLIGENT INVESTOR REVISED EDITION BENJAMIN GRAHAM HARPER BUSINESS', 'MALCOLM GLADWELL OUTLIERS']
    books = []
    for tit_text in img_text:
        book_data = {'title':'NA', 'author':'NA', 'image_url':'NA', 'publish_date': 'NA', 'description':'NA'}
        title, author, image_url, publish_date, description = get_book_info(tit_text)
        if title != 'NA' and author != 'NA':
            book_data['title'] = title
            book_data['author'] = author
            book_data['image_url'] = image_url
            book_data['publish_date'] = publish_date
            book_data['description'] = description
            books.append(book_data)
        print(title)
        print(author)
        print(image_url)
        print('##########################')
        print()
    # title, author, image_url, publish_date, description = get_book_info("LARSSON millennium I The Girl with the Dragon Tattoo int MACLEHOSE Quercus")
    # print(title)
    # print(author)
    # print('##########################')
    #print(books)
    return books 

#get_book_names('books.jpg')