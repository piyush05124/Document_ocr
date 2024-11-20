from pyzbar.pyzbar import decode
import cv2 #COMPUTER VISION LIBRARY
def Decode(image):
      result=[]
      img=cv2.imread(image) # IS LINE KA MATLAB BATA
      
      qdata=decode(img) # USED FOR EXTRACTION OF TEXT
      
      
##      for i in qdata:
##            result.append(i.data.decode('utf-8'))
      res=[i.data.decode('utf-8') for i in qdata] # LIST COMPREHENSION
      return ''.join(res)   #list to string joining   
