import dice
import uwp

class System:
    def __init__(self):
        self.coordinates = []

    def generate(self, coordinates, settlement):
        self.coordinates = coordinates
        self.settlement = settlement
        self.uwp = uwp.Uwp(coordinates = self.coordinates, settlement  = self.settlement)

    def getCoordinates(self):
        return self.coordinates

    def getString(self):
        return self.uwp.getString()

    def getStarport(self):
        return self.uwp.getStarport()



