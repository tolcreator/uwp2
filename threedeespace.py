import dice
import system

class ThreeDeeSpace:
    subspaceLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    def __init__(self, coordinates = [0, 0, 0], name = "Default", size = 4):
        self.size = [size, size, size]
        self.coordinates = coordinates
        self.density = "Standard"
        self.settlement = "Standard"
        self.name = name

    def setDensity(self, density):
        self.density = density
        for i in self.subSpaces:
            i.setDensity(density)

    def setSettlement(self, settlement):
        self.settlement = settlement
        for i in self.subSpaces:
            i.setSettlement(settlement)

    def getCoordinates(self):
        return self.coordinates

    def generate(self):
        for i in self.subSpaces:
            i.generate()

    def systemPresence(self):
        mydice = dice.Dice()
        if self.density == "Rift":
            percent = 1
        if self.density == "Scattered":
            percent = 3
        if self.density == "Sparse":
            percent = 6
        if self.density == "Standard":
            percent = 9
        if self.density == "Dense":
            percent = 12
        if mydice.roll(1, 100) <= percent:
            return True
        else:
            return False

    def show(self):
        for i in self.subSpaces:
            i.show()

    def getSubspace(self, queery):
        if queery in self.__class__.subspaceLabels:
            index = self.__class__.subspaceLabels.index(queery)
        elif queery >= 0 and queery <= 8:
            index = queery
        else:
            return None
        return self.subSpaces[index]        

    def getSubspaceCoordinates(self, subspace):
        """
        Assumes space is a cube, composed of 8 subspaces, which are also cubes
        """
        grid = [
            [0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        if(subspace < 8):
            matrix = grid[subspace]
        else:
            matrix = grid[0]
        return [matrix[0] * (self.size[0] / 2), matrix[1] * (self.size[1] / 2), matrix[2] * (self.size[2] / 2)]

class ThreeDeeSlice(ThreeDeeSpace):
    def __init__(self, coordinates = [0, 0, 0], name = "Default Slice"):
        self.size = [4, 4, 4]
        self.coordinates = coordinates
        self.systems = []
        """
        A Slice has no subspaces
        """
        self.subSpaces = []
        self.density = "Standard"
        self.settlement = "Standard"
        self.name = name

    def generate(self):
        del self.systems
        self.systems = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if self.systemPresence():
                        newSystem = system.System()
                        newSystem.generate([self.coordinates[0] + x, self.coordinates[1] + y, self.coordinates[2] + z], self.settlement)
                        self.systems.append(newSystem)

    def show(self):
        print "Slice \"%s\" %02d%02d%02d %d Systems:" % (self.name, self.coordinates[0], self.coordinates[1], self.coordinates[2], len(self.systems))
        for x in self.systems:
            print x.getString()


class ThreeDeeSubsector(ThreeDeeSpace):
    def __init__(self, coordinates = [0, 0, 0], name = "Default Subsector"):
        self.size = [8, 8, 8]
        self.coordinates = coordinates
        self.subSpaces = []
        self.name = name
        for i in range(8):
            name = "%s of %s" % (self.__class__.subspaceLabels[i], self.name)
            self.subSpaces.append(ThreeDeeSlice(coordinates = self.getSubspaceCoordinates(i), name = name))
