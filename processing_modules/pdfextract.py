

import PyPDF2 as pdf
from PyPDF2 import PdfReader,PdfFileReader
import cv2
import os
import pprint
import json
import re # REGULAR EXPRESSION



def pdftext(filepath,pno):
    if filepath.endswith('.pdf'):
        reader = PdfReader(filepath)
        numOfPages = len(reader.pages)
        #print('inder',(pno!= 0) , (int(pno) in list(range(1,numOfPages+1))))
        if (pno!= 0) and (pno in list(range(1,numOfPages+1))):
            page = reader.pages[pno-1]
            return page.extract_text()
        else:
            return f'{pno} no page is not avilable'