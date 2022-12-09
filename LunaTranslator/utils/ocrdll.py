from ctypes import CDLL,c_char_p ,create_string_buffer,c_uint32,POINTER

class ocrwrapper:
    def __init__(self) -> None:
        self.dll= CDLL('./files/ocr.dll')
    def _OcrInit(self,szDetModel, szRecModel, szKeyPath,szClsModel='', nThreads=4):
        
        _OcrInit=self.dll.OcrInit
        _OcrInit.restype=POINTER(c_uint32)
        self.pOcrObj=_OcrInit(c_char_p(szDetModel.encode('utf8')),c_char_p(szClsModel.encode('utf8')),c_char_p(szRecModel.encode('utf8')),c_char_p(szKeyPath.encode('utf8')),nThreads)
        
    def _OcrDetect( self,imgPath, imgName ) :
        _OcrDetect=self.dll.OcrDetect
        return _OcrDetect(  self.pOcrObj ,c_char_p(imgPath.encode('utf8')),c_char_p(imgName.encode('utf8')))
    def _OcrGet(self):
        _OcrGetLen=self.dll.OcrGetLen
        _OcrGetResult=self.dll.OcrGetResult
        length=_OcrGetLen(self.pOcrObj)
        buff = create_string_buffer(length)

        _OcrGetResult(self.pOcrObj,buff,length)
        return buff.value
    def _OcrDestroy(self):
        _OcrDestroy=self.dll.OcrDestroy
        _OcrDestroy(self.pOcrObj)
    def init(self,det,rec,key):
        self._OcrInit(det,rec,key)
    def ocr(self,path,name):
        self._OcrDetect(path,name) 
        return self._OcrGet().decode('utf8')
    def destroy(self):
        self._OcrDestroy()
# ocr=ocrwrapper()
# ocr.init('./files/ocr/ja/det.onnx','./files/ocr/ja/rec.onnx','./files/ocr/ja/dict.txt')
# print(ocr.ocr('./capture/','1668516425.0008786.jpg').decode('utf8'))