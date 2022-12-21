import requests
import json
import serial
import datetime

class Scan():
    def __init__(self, port):
        self.Scanner = serial.Serial(port=port, baudrate=9600, timeout=1)
        print(self.Scanner)
    
    def __del__(self):
        self.Scanner.close()
        print("scanner close")

    def update(self, barcode):
        print(type(barcode))
        vo = {
            'qrcode': barcode
        }

        response = requests.post("http://127.0.0.1:5000/token/make", data=vo,
                                  timeout=40)
        print(response.json())
        return response.json()

    def run(self):
        while True:
            try:
                if self.Scanner.readable():
                    barcode = self.Scanner.readline()
                    barcode = barcode.decode('utf-8').rstrip()
                    if len(barcode) > 0:
                        print('barcode:' + barcode)
                        return self.update(barcode)
                        
            except Exception as e:
                print(e)
                return None