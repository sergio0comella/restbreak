from math import nan

class Keyboard:
    def __init__(self, robot):
        self.keyboard = robot.getKeyboard()
        self.keyboard.enable(64)
        self.pressedKey = nan

    def getKey(self):
        return self.pressedKey

    def update(self):
        self.pressedKey = self.keyboard.getKey()
