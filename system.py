import dice

class System:
    def __init__(self):
        self.coordinates = []

    def generate(self, coordinates, settlement):
        self.coordinates = coordinates

    def getCoordinates(self):
        return self.coordinates
