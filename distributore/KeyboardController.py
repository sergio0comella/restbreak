from multiprocessing.sharedctypes import Value
import time
from Logger import Logger
from Constants import LOCK, OFFICE_NUMBER, UNLOCK
from CustomException import OutOfRangeError
from Keyboard import Keyboard
from math import nan

class KeyboardController:

    def __init__(self, robot):
        self.keyboard = Keyboard(robot)
        self.status = UNLOCK
        self.enableRun = False
        self.orderlist = []
        self.office = None
        

    def update(self):
        self.currentkey = None
        try:
            return self.updateCommands()
        except (OutOfRangeError, ValueError) as KeyboardError:
            Logger.info(KeyboardError)

    def getOffice(self):
        return self.office

    def updateCommands(self):
        self.keyboard.update()
        self.currentkey = self.keyboard.getKey()
        
        if self.isKeyPressed(self.currentkey, '\4'):
            print(chr(27) + "[2J")
            print(self.orderlist)
            
            if self.status == LOCK:
                if int(self.orderlist[-1]) == 0:
                    self.unlockStatus()
                    self.emptyOrderList()
                    print('Dispositivo sbloccato.')
                else:
                    print('Dispositivo in stato LOCKED.')
                return
            
            if(1 <= len(self.orderlist) <= 2):
                office = int(''.join(self.orderlist))
                # self.emptyOrderList()
                
                print(office)
                if office < 0 or office > 6:
                    print('Ufficio inesistente.')
                    return
                self.enableRun = True
                self.office = office
            else:
                self.emptyOrderList()
                print('In attesa di una nuova destinazione...')

        elif self.isKeyInOfficeList():
            print(chr(27) + "[2J")
            self.orderlist.append(chr(self.currentkey))
            print(str(''.join(self.orderlist)))
            time.sleep(0.5)
            
    def canRun(self):
        return self.enableRun
    
    def stopRun(self):
        self.enableRun = False

    def emptyOrderList(self):
        self.orderlist = []

    def isKeyInOfficeList(self):
        officeList = ['0','1','2','3', '4', '5', '6']
        for i in officeList:
            if self.isKeyPressed(self.currentkey, i):
                return True
        return False
    
    def reset(self):
        self.stopRun()
        self.emptyOrderList()
        
    def isKeyPressed(self, key, char):
        return key == ord(char) or key == ord(char.upper())
    
    def lockStatus(self):
        self.status = LOCK

    def unlockStatus(self):
        self.status = UNLOCK