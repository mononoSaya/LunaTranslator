 
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPen,QColor ,QTextCharFormat ,QTextBlockFormat,QTextCursor,QFont,QColor,QFontMetricsF,QTextDocument,QPainter
from PyQt5.QtWidgets import  QTextBrowser ,QLabel,QPushButton,QGraphicsDropShadowEffect
import random
import functools 
from utils.config import globalconfig
from utils.wrapper import timer
from traceback import print_exc
class Qlabel_c(QLabel):
    
    def mousePressEvent(self, ev   )  :
        self.pr=True
        return super().mousePressEvent(ev)
    def mouseMoveEvent(self, ev) :
        self.pr=False
        return super().mouseMoveEvent(ev)
    def mouseReleaseEvent(self, ev )  :
        try:
            if self.pr:
                self.callback()
            self.pr=False
        except:
            print_exc()
        return super().mouseReleaseEvent(ev)

class MyTextDocument(QTextDocument):
    def __init__(self, parent ):
        super().__init__() 
        self.parent = parent 
    def drawContents(self, painter):
        
        my_cursor = self.parent.textCursor()
        my_char_format = my_cursor.charFormat() 
        my_char_format.setTextOutline(QPen(Qt.GlobalColor.red, 15))
        my_cursor.select(QTextCursor.SelectionType.Document)
        my_cursor.mergeCharFormat(my_char_format)
 
        super().drawContents(painter)
        my_char_format.setForeground(Qt.GlobalColor.white)
        my_char_format.setTextOutline(QPen(Qt.GlobalColor.white))
        my_cursor.mergeCharFormat(my_char_format)
         
        super().drawContents(painter)
        
class _QTextBrowser(QTextBrowser):
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
 
        super(_QTextBrowser, self).paintEvent(event)
 
        self.document().drawContents(painter)
class Textbrowser():
    def __init__(self, parent ) : 
        self.parent=parent
        #self.shadowlabel=QLabel(parent)
        #self.shadowlabel.savetext=''
        self.align=False 
        self.textbrowserback=QTextBrowser(parent)
        self.textbrowser=_QTextBrowser(parent)
        self.textbrowser.setDocument(MyTextDocument(self.textbrowser ))
        self.textbrowser.setStyleSheet("border-width: 0;\
                                           border-style: outset;\
                                           border-top: 0px solid #e8f3f9;\
                                           color: white;\
                                            \
                                           background-color: rgba(%s, %s, %s, %s)"
                                           %(0,0,0,0))
         
        self.savetaglabels=[]
        self.searchmasklabels_clicked=[]
        self.searchmasklabels=[]
        self.backcolorlabels=[]
        self.addtaged=False
        self.lastcolor=None
        self.charformat=self.textbrowser.currentCharFormat()
    def simplecharformat(self,color):
        self.textbrowser.setCurrentCharFormat(self.charformat) 
        self.textbrowser.setTextColor(QColor(color)) 
    def setText(self,text):
        self.textbrowser.setText(text) 
        
    def setVerticalScrollBarPolicy(self,x):
        self.textbrowser.setVerticalScrollBarPolicy(x) 
    def setHorizontalScrollBarPolicy(self,x): 
        self.textbrowser.setHorizontalScrollBarPolicy(x) 
    def setFont(self,x): 
        self.textbrowser.setFont(x) 
        #self.shadowlabel.setFont(x) 
    def setStyleSheet(self,x): 
        #self.textbrowser.setStyleSheet(x)
        
        #self.textbrowserback.setStyleSheet(x)
        self.parent.atback.setStyleSheet(x)
    def move(self,x,y):
        self.textbrowser.move(x,y) 
        #self.shadowlabel.move(x,y)
       
    def document(self): 
        return self.textbrowser.document()
    def setGeometry(self,_1,_2,_3,_4):
        self.textbrowser.setGeometry(_1,_2,_3,_4) 
        #self.shadowlabel.setGeometry(_1,_2,_3,_4)  
        #self.shadowlabel.resize(_3,_4)
    def setAlignment(self,x):
        self.textbrowser.setAlignment(x) 
        if Qt.AlignCenter==x:
            self.align=True
        else:
            self.align=False
        #self.shadowlabel.setAlignment(Qt.AlignTop )
    @timer
    def append(self,x ): 
        
        if self.addtaged:
            
            # self.textbrowserback.append(' ') 
            # self.textbrowser.append(' ')
            # cursor=self.textbrowser.textCursor()
            # cursor.movePosition(QTextCursor.End)
            # self.textbrowser.setTextCursor(cursor)
            # cursor=self.textbrowserback.textCursor()
            # cursor.movePosition(QTextCursor.End)
            # self.textbrowserback.setTextCursor(cursor)
         
            self.textbrowser.append('') 
             
            self.addtaged=False
            f1=QTextBlockFormat()
            f1.setLineHeight(0,QTextBlockFormat.LineDistanceHeight)
            f1.setAlignment(self.textbrowser.alignment()) 
            cursor=self.textbrowser.textCursor() 
            #cursor.movePosition(QTextCursor.StartOfBlock)
            #cursor.setBlockFormat(f1)
            cursor.mergeBlockFormat(f1)
            self.textbrowser.setTextCursor(cursor) 
            #cursor.movePosition(QTextCursor.StartOfBlock) 
            self.textbrowser.insertPlainText(x)
             
        else: 
            self.textbrowser.append(x) 
        # if self.shadowlabel.savetext!='':
        #     self.shadowlabel.savetext=(self.shadowlabel.savetext+'<br>'+ x)
        # else:
        #     self.shadowlabel.savetext=x
        # if self.align:
        #     self.shadowlabel.setText( '<html><p style="color:rgba(0,0,0)" align=\'center\'> %s</p></html>' %self.shadowlabel.savetext)
        # else:
        #     self.shadowlabel.setText( '<html><p > %s</p></html>' %self.shadowlabel.savetext)
        # if globalconfig['showShadow']:
        #     shadow = QGraphicsDropShadowEffect()
        #     shadow.setBlurRadius(10)
            
        #     shadow.setColor(QColor(globalconfig['shadowcolor']))
        #     shadow.setOffset(0)
        #     # adding shadow to the label
            
        #     self.shadowlabel.setGraphicsEffect(shadow)
    @timer
    def addsearchwordmask(self,x,callback=None,start=2):
        
        #print(x)
        pos=start
         
        labeli=0 
        cursor=self.textbrowser.textCursor()
        cursor.setPosition(start)
        self.textbrowser.setTextCursor(cursor)
        cursor.movePosition(QTextCursor.StartOfBlock)
        self.textbrowser.setTextCursor(cursor)
        
        guesswidth=[]
        for word in x:
             
            if word['orig']=='\n':
                continue
            l=len(word['orig'])
            tl1=self.textbrowser.cursorRect(self.textbrowser.textCursor()).topLeft()
            tl4=self.textbrowser.cursorRect(self.textbrowser.textCursor()).bottomRight()
            color=self.randomcolor()
             
            for i in range(1,l+1):
                    
                cursor=self.textbrowser.textCursor() 
                cursor.setPosition(pos+i )
                self.textbrowser.setTextCursor(cursor)
                 
                tl2=self.textbrowser.cursorRect(self.textbrowser.textCursor()).bottomRight() 
                tl3=self.textbrowser.cursorRect(self.textbrowser.textCursor()).topLeft() 
 
                if labeli>=len(self.searchmasklabels):
                     
                    ql=QLabel(self.parent.atback) 
                    ql.setMouseTracking(True)
                    self.searchmasklabels.append(ql)

                    ql=Qlabel_c(self.textbrowser) 
                    ql.setMouseTracking(True)
                    ql.setStyleSheet("background-color: rgba(0,0,0,0.01);")
                    self.searchmasklabels_clicked.append(ql)
                if tl1.y()!=tl3.y():
                    if globalconfig['usesearchword']:
                        self.searchmasklabels_clicked[labeli].setGeometry(tl1.x(),tl1.y() ,sum(guesswidth)//len(guesswidth),tl4.y()-tl1.y()) 
                    if globalconfig['show_fenci']:
                        self.searchmasklabels[labeli].setGeometry(tl1.x(),tl1.y() ,sum(guesswidth)//len(guesswidth),tl4.y()-tl1.y()) 
                else:
                    guesswidth.append(tl2.x()-tl1.x())
                    if globalconfig['usesearchword']:
                        self.searchmasklabels_clicked[labeli].setGeometry(tl1.x(),tl1.y() ,tl2.x()-tl1.x(),tl2.y()-tl1.y())
                    if globalconfig['show_fenci']:
                        self.searchmasklabels[labeli].setGeometry(tl1.x(),tl1.y() ,tl2.x()-tl1.x(),tl2.y()-tl1.y())
                if globalconfig['show_fenci']:
                    self.searchmasklabels[labeli].setStyleSheet(f"background-color: rgba{color};"  )
                tl1=tl3 
                tl4=tl2
                if word['orig'] not in ['\n','\r'] :
                    if globalconfig['usesearchword']:
                        self.searchmasklabels_clicked[labeli].show()
                    if globalconfig['show_fenci']:
                        self.searchmasklabels[labeli].show()
                if callback:
                    self.searchmasklabels_clicked[labeli].callback=functools.partial(callback,word['orig'])
                #self.searchmasklabels[labeli].clicked.connect(lambda x:print(111))
                #self.searchmasklabels[labeli].mousePressEvent=(lambda x:print(111))
                labeli+=1
            pos+=l
        
                
    def randomcolor(self):
        if self.lastcolor is None:
            self.lastcolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255),1)
        
        self.lastcolor= ((self.lastcolor[0]+ random.randint(64,192))%255,(self.lastcolor[1]+ random.randint(64,192))%255,(self.lastcolor[2]+ random.randint(64,192))%255,max(0.3,globalconfig['transparent']/100))
        return self.lastcolor
    @timer
    def addtag(self,x): 
        if len(self.savetaglabels)<len(x):
            self.savetaglabels+=[QLabel(self.textbrowser) for i in range(len(x)-len(self.savetaglabels))]
        #print(x)
        pos=2
        self.addtaged=True
        labeli=0 
        cursor=self.textbrowser.textCursor()
        cursor.setPosition(2)
        self.textbrowser.setTextCursor(cursor)
        cursor.movePosition(QTextCursor.StartOfBlock)
        self.textbrowser.setTextCursor(cursor)
         
        font=QFont()
        font.setFamily(globalconfig['fonttype']) 
        font.setPointSizeF(12) 
        f1=QTextBlockFormat()
        
        f1.setLineHeight(20,QTextBlockFormat.LineDistanceHeight)
        f1.setAlignment(self.textbrowser.alignment())
        need=True
        for word in x:
            if word['orig']=='\n':
                continue
            l=len(word['orig'])
            tl1=self.textbrowser.cursorRect(self.textbrowser.textCursor()).topLeft() 
            cursor=self.textbrowser.textCursor()
            if need:
                cursor.setBlockFormat(f1)
            cursor.setPosition(pos+l )
            self.textbrowser.setTextCursor(cursor)
             
            pos+=l
            need=False
            
            tl2=self.textbrowser.cursorRect(self.textbrowser.textCursor()).topLeft() 
            #print(tl1,tl2,word['hira'],self.textbrowser.textCursor().position())
            self.savetaglabels[labeli].setText(word['hira'])
            self.savetaglabels[labeli].setFont(font)
            self.savetaglabels[labeli].adjustSize()
            w=self.savetaglabels[labeli].width()
            
            if tl1.y()!=tl2.y():
                x=tl2.x()-w
                need=True
            else:
                x=tl1.x()/2+tl2.x()/2-w/2
            y=tl2.y()-20
            
            self.savetaglabels[labeli].move(x,y)  
            
             
            
            self.savetaglabels[labeli].setStyleSheet("color: %s;background-color:rgba(0,0,0,0)" %(globalconfig['rawtextcolor']))
            self.savetaglabels[labeli].show()
            labeli+=1
       
    def mergeCurrentCharFormat(self,colormiao,width):
        format2=QTextCharFormat()
        format2.setTextOutline(QPen(QColor(colormiao),width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    
        self.textbrowser.setCurrentCharFormat(format2) 
    def mergeCurrentCharFormat_out(self,colorinner,colormiao,width):
        format1 = QTextCharFormat() 
        format1.setForeground(QColor(colorinner))
        format2=QTextCharFormat()
        format2.setTextOutline(QPen(QColor(colormiao),width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        self.textbrowser.setCurrentCharFormat(format1) 
    def clear(self):
        for label in self.searchmasklabels:
            label.hide()
        for label in self.searchmasklabels_clicked:
            label.hide()
        for label in self.savetaglabels:
            label.hide()
            
        # self.textbrowser.clear()
        # self.textbrowserback.clear()

        self.textbrowser.setText('') 
        # self.shadowlabel.setText('')
        # self.shadowlabel.savetext=''