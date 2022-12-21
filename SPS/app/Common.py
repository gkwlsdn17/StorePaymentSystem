import datetime

__TIMEOUT__SEC__ = 60
__TIMEOUT__DAY__ = 30
__OFFSET__ = 30

class Token():
    def __init__(self, id, timeout):
        now = datetime.datetime.now()
        self.value = f"{id}${timeout}${now.strftime('%Y%m%d%H%M%S')}"

    def getValue(self):
        return self.value

class RESULT():
    def __init__(self):
        self.result = {
                'RESULT':'001',
                'DATA':{},
                'ERROR':{}
    }

    def setError(self, code, text):
        self.result["ERROR"] = {
            'CODE' : code,
            'TEXT' : text
        }
    
    def getError(self):
        return self.result["ERROR"]

    def setData(self, data):
        self.result['DATA'] = data

    def setRESULT(self, code):
        self.result['RESULT'] = code

    def getResult(self):
        return self.result