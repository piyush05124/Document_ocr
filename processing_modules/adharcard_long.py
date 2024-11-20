import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import json
import re

# pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'




pat=r'[III III I ll |l|||I|| Illl llllllllll I III! |||l|||]'
 
def adhar(image):
    try:
        imag = cv2.imread(image)  #read an image
        
        imag=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY) #convertion to grayscale
        imag = cv2.resize(imag,(1051,2280)) #resize in image(w X h)
        roi=imag[518:1500,100:900] #segment 1
        roi=cv2.resize(roi,(995,1080))
        roi=cv2.convertScaleAbs(roi, alpha=1, beta=0)
        tst=[pytesseract.image_to_string(roi, lang='eng')]

        det=[]
        details=[]
        uid=[]
        nfn=[]

        
        for i in tst:
            j=i.splitlines()
            for e in j:
                if len(e)>3:
                    det.append(e)
                             
        for o in det:
            match = re.search(r'\d{2}/\d{2}/\d{4}',o)
            if match:
                det.remove(o)

        for t in det:
            match1 = re.search(r'\d{4} \d{4} \d{4}',t)
            if match1:
                uid.append(t)
                
      
        for x in range(0,3):
            nfn.append(det[x])
            

        for e in det:
            if re.search(r'\d{10}',e) or re.search(r'\d{9}',e) or re.search(r'\d{8}',e) or re.search(r'\d{7}',e) :
                det.remove(e)

        for r in det:
            if r.isalnum():
                if not r.isalpha():
                    det.remove(r)
        
        
        del(det[:1])
        vcs=[]
        vcs=vcs+det[2:-2]

        if nfn[2]==vcs[0]:
            del(nfn[2])
        else:
            del(nfn[0])

    ##    for l in nfn:
    ##        for c in vcs:
    ##            if l==c:
    ##                nfn.remove(l)
    ##            else:
                    
             

        for z in vcs:
            if re.search(r'\d \d',z):
                vcs.remove(z)

        for m in vcs:
            if re.search("/ Your",m):
                vcs.remove(m)

        ns=[' '.join(vcs)]
            
            

        att=['Name: ','C/O: ','Address: ','UID: ','gender: ','DOB: ']

        
        

        info2=[]
        roi1=imag[1750:1900,320:800]
        text11=[pytesseract.image_to_string(roi1, lang='eng')]
        #print(text11)
        for i in text11:
            j=i.splitlines()
            for e in j:
                if len(e)>3:
                    info2.append(e)
       # print(info2)


        dob=[]
        gen=[]
        for aj in info2:
            match=re.search(r'\d{2}/\d{2}/\d{4}',aj)
            if match:
                dob.append(match.group())
        for ak in info2:
            m=re.search(r'Male',ak) or re.search(r'/ Male',ak)
            f=re.search(r'Female',ak) or re.search(r'/ Female',ak)
            if m or f:
                gen.append(ak)

        for am in gen:
            for aw in am:
                if aw=='/':
                    y2=am.split('/ ')[1]
                    gen.remove(am)
                    gen.append(y2)
           
                
        
    ##    print(dob)
    ##    print(gen)

        details=nfn+ns+uid+gen+dob
       # cv2.imwrite('{}.png'.format(uid),imag)
    ##    
        ad1=list(zip(att,details))

        return '\n'.join([''.join(i) for i in ad1])
    except IndexError:
        return "please enter valid adharcard image"

###################################################################################
##########################################################################################
################################################################################

def QRcode(image):
    try:
        
        im=image
        iread=cv2.imread(im)
        iread=cv2.cvtColor(iread,cv2.COLOR_BGR2GRAY)
        iread = cv2.resize(iread,(1051,2280))
        

        uroi=iread[1200:1500,100:1100]
        utext=pytesseract.image_to_string(uroi, lang='eng')
        zap=re.search(r'\d{4} \d{4} \d{4}',utext)
        uid=zap.group()
        print(uid)
        

        qroi=iread[500:1400, 500:1300]
        iq = cv2.resize(qroi,(2600,3950))

        
        
        v=decode(iq)
        ret=[]
        for i in v:
            ret.append(i.data.decode('utf-8'))
            
        if not ret:
            return adhar(im)
        
        else:
            return ret
    except AttributeError:
            return "please enter valid adharcard image"

        
    
    
    
    
