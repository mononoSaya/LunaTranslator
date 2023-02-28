 
import time
from traceback import print_exc 

from utils.ocrdll import ocrwrapper
from utils.config import globalconfig  
import importlib  
from difflib import SequenceMatcher 
from utils import somedef
import time  
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QImage,QPixmap
from textsource.textsourcebase import basetext  
def qimge2np(img:QImage):
    #img=img.convertToFormat(QImage.Format_Grayscale8)
    shape=img.height(),img.width(),1
    img=img.scaled(128,8*3) 
    img.shape=shape
    return img
def compareImage(img1:QImage,img2):
    cnt=0
    for i in range(128):
        for j in range(24):
            cnt+=(img1.pixel(i,j)==img2.pixel(i,j)) 
    return cnt/(128*24)
     
def getEqualRate(  str1, str2):
    
        score = SequenceMatcher(None, str1, str2).quick_ratio()
        score = score 

        return score
import win32gui ,math,win32process
class ocrtext(basetext):
    
    def imageCut(self,x1,y1,x2,y2):
     
        if self.hwnd:
            try:  
                hwnd=win32gui.FindWindow('Window_Magpie_967EB565-6F73-4E94-AE53-00CC42592A22',None) 
                if hwnd and globalconfig['ocrmagpiekeep']==False:  
                    hwnduse=QApplication.desktop().winId()
                else:
                    hwnduse=self.hwnd
                rect=win32gui.GetWindowRect(hwnduse)  
                rect2=win32gui.GetClientRect(hwnduse)
                windowOffset = math.floor(((rect[2]-rect[0])-rect2[2])/2)
                h= ((rect[3]-rect[1])-rect2[3]) - windowOffset
                # print(h)
                # print(rect)
                # print(rect2)
                # print(x1-rect[0], y1-rect[1]-h, x2-x1, y2-y1)
 
                 
                pix = self.screen.grabWindow(hwnduse, x1-rect[0], y1-rect[1]-h, x2-x1, y2-y1) 
                
            except:
                self.hwnd=None
                print_exc()
                self.object.translation_ui.isbindedwindow=False
                self.object.translation_ui.refreshtooliconsignal.emit()
                pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        else:
            pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        return pix.toImage()
    def __init__(self,textgetmethod,object)  :
        self.screen = QApplication.primaryScreen() 
        self.savelastimg=None
        self.savelastrecimg=None
        self.savelasttext=None  
        self.object=object 
        self.lastocrtime=0
        self.hwnd=None
        self.nowuseocr=None
        self.timestamp=time.time() 
        super(ocrtext,self ).__init__(textgetmethod,'0','0_ocr') 
    def gettextthread(self ):
                 
            if self.object.rect is None:
                time.sleep(1)
                return None
            
            time.sleep(0.1)
            #img=ImageGrab.grab((self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1]))
            #imgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            if self.object.rect is None:
                return None
            imgr=self.imageCut(self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1])
            
            ok=True
            
            if globalconfig['ocr_auto_method'] in [0,2]: 
                imgr1=qimge2np(imgr)
                h,w,c=imgr1.shape 
                if self.savelastimg is not None and  (imgr1.shape==self.savelastimg.shape) : 
                    
                    image_score=compareImage(imgr1 ,self.savelastimg )
                    
                else:
                    image_score=0 
                self.savelastimg=imgr1
                
                if image_score>globalconfig['ocr_stable_sim'] : 
                    if self.savelastrecimg is not None and  (imgr1.shape==self.savelastrecimg.shape   ) :
                        image_score2=compareImage(imgr1 ,self.savelastrecimg ) 
                    else:
                        image_score2=0 
                    if image_score2>globalconfig['ocr_diff_sim']:
                        ok=False
                    else: 
                        self.savelastrecimg=imgr1
                else:
                    ok=False
            if globalconfig['ocr_auto_method'] in [1,2]:
                if time.time()-self.lastocrtime>globalconfig['ocr_interval']:
                    ok=True
                else:
                    ok=False
            if ok==False:
                return None
            text=self.ocrtest(imgr)  
            self.lastocrtime=time.time()
            
            if self.savelasttext is not None:
                sim=getEqualRate(self.savelasttext,text)
                #print('text',sim)
                if sim>0.9: 
                    return  None
            self.savelasttext=text
            
            return (text)
            
    def runonce(self): 
        if self.object.rect is None:
            return
        if self.object.rect[0][0]>self.object.rect[1][0] or self.object.rect[0][1]>self.object.rect[1][1]:
            return  
        img=self.imageCut(self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1])
        
        

        text=self.ocrtest(img)
        imgr1=qimge2np(img)
        self.savelastimg=imgr1
        self.savelastrecimg=imgr1
        self.lastocrtime=time.time()
        self.savelasttext=text
        self.textgetmethod(text,False)
    def ocrtest(self,img):
        use=None
        for k in globalconfig['ocr']:
            if globalconfig['ocr'][k]['use']==True:
                use=k
                break
        if use is None:
            return ''
        fname=f'./cache/ocr/{self.timestamp}.png'
        img.save(fname)
        
        if self.nowuseocr!=use:
            try:
                self.ocrengine.end()
            except:pass
            try:
                aclass=importlib.import_module('ocrengines.'+use).OCR 
                self.ocrengine=aclass(use)   
                self.nowuseocr=use
            except:
                return ''
        
        return self.ocrengine.ocr(fname)
         