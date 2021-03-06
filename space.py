import dice
import system
import pickle

class Space:
    def __init__(self, coordinates = [0, 0], name = "Default"):
        self.coordinates = coordinates
        self.density = "Standard"
        self.settlement = "Standard"
        self.name = name
        self.dimensions = 2

    def getDimensions(self):
        return self.dimensions

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

    def show(self):
        for i in self.subSpaces:
            i.show()

    def getSubspace(self, queery):
        if queery in self.__class__.subspaceLabels:
            index = self.__class__.subspaceLabels.index(queery)
        elif queery >= 0 and queery <= len(self.__class__.subspaceLabels):
            index = queery
        else:
            return None
        return self.subSpaces[index]

    def getFileName(self):
        return self.name + ".sec"

    def save(self, filename=None):
        FILE = open(filename, "w")
        pickle.dump(self, FILE)
        FILE.close()


class Space2D(Space):
    subspaceLabels = ['A', 'B', 'C', 'D']

    def __init__(self, coordinates = [0, 0], name = "Default"):
        self.coordinates = coordinates
        self.density = "Standard"
        self.settlement = "Standard"
        self.name = name
        self.dimensions = 2

    def systemPresence(self):
        mydice = dice.Dice()
        if self.density == "Rift":
            roll = mydice.roll(2, 6)
            if roll == 12:
                return True
            else:
                return False
        else:
            dm = 0
            roll = mydice.roll(1, 6)
            if self.density == "Scattered":
                dm = -1
            elif self.density == "Sparse":
                dm = -2
            elif self.density == "Dense":
                dm = +1
            else:
                dm = 0;

            if (roll + dm) >= 4:
                return True
            else:
                return False

    def generateDotMap(self):
        map = []
        for i in self.subSpaces:
            y = i.getCoordinates()[1]
            index = y - self.coordinates[1]
            submap = i.generateDotMap()
            for row in submap:
                if index + 1 > len(map):
                    map.append(row)
                else:
                    for x in row:
                        map[index].append(x)
                index += 1
        return map

    def drawDotMap(self):
        map = self.generateDotMap()
        for row in map:
            rowstr = " ".join(row)
            print rowstr

class Space3D(Space):
    subspaceLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    def __init__(self, coordinates = [0, 0, 0], name = "Default"):
        self.coordinates = coordinates
        self.density = "Standard"
        self.settlement = "Standard"
        self.name = name 
        self.dimensions = 3

class Subsector(Space2D):
    def __init__(self, coordinates = [0, 0], name="Default Subsector"):
        self.size = [8, 10]
        self.coordinates = coordinates
        self.systems = []
        """
        A subsector has no subSpaces
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
                if self.systemPresence():
                    newSystem = system.System()
                    newSystem.generate([self.coordinates[0] + x, self.coordinates[1] + y], self.settlement)
                    self.systems.append(newSystem)

    def generateDotMap(self):
        """
        generate blank map
        """
        map = []
        for y in range(self.size[1]):
            row = []
            for x in range(self.size[0]):
                row.append(' ')
            map.append(row)
        """
        populate
        """
        for i in self.systems:
            x = i.getCoordinates()[0] - self.coordinates[0]
            y = i.getCoordinates()[1] - self.coordinates[1]
            map[y][x] = i.getStarport()
        return map

    def show(self):
        print "%d Systems:" % len(self.systems)
        for x in self.systems:
            print x.getString() 

    def appendToFile(self, FILE):
        FILE.write("#" + self.__class__.__name__ + ":" + self.name + ":at %02d%02d" % (self.coordinates[0], self.coordinates[1]) + ":%d systems\n" % (len(self.systems)))
        for x in self.systems:
            FILE.write(x.getString() + "\n")
        

class Quadrant(Space):
    def __init__(self, coordinates = [0, 0], name="Default Quadrant"):
        self.size = [16, 20]
        self.coordinates = coordinates
        self.subSpaces = []
        self.subSpaces.append(Subsector([self.coordinates[0] + 0, self.coordinates[1] + 0]))
        self.subSpaces.append(Subsector([self.coordinates[0] + 8, self.coordinates[1] + 0]))
        self.subSpaces.append(Subsector([self.coordinates[0] + 0, self.coordinates[1] + 10]))
        self.subSpaces.append(Subsector([self.coordinates[0] + 8, self.coordinates[1] + 10]))
        self.name = name

class Sector(Space):
    def __init__(self, coordinates = [0, 0], name="Default Sector"):
        self.size = [32, 40]
        self.coordinates = coordinates
        self.subSpaces = []
        self.subSpaces.append(Quadrant([self.coordinates[0] + 0, self.coordinates[1] + 0]))
        self.subSpaces.append(Quadrant([self.coordinates[0] + 16, self.coordinates[1] + 0]))
        self.subSpaces.append(Quadrant([self.coordinates[0] + 0, self.coordinates[1] + 20]))
        self.subSpaces.append(Quadrant([self.coordinates[0] + 16, self.coordinates[1] + 20]))
        self.name = name

class Domain(Space):
    def __init__(self, coordinates = [0, 0], name="Default Domain"):
        self.size = [64, 80]
        """
        Domain coordinates are the sector coordinates of the first (Coreward Spinward)
        sector of the domain
        """
        self.coordinates = coordinates
        self.subSpaces = []
        self.subSpaces.append(Sector([self.coordinates[0] + 0, self.coordinates[1] + 0]))
        self.subSpaces.append(Sector([self.coordinates[0] + 32, self.coordinates[1] + 0]))
        self.subSpaces.append(Sector([self.coordinates[0] + 0, self.coordinates[1] + 40]))
        self.subSpaces.append(Sector([self.coordinates[0] + 32, self.coordinates[1] + 40]))
        self.name = name


def load(filename):
    FILE = open(filename, "r")
    thisSpace = pickle.load(FILE)
    FILE.close()
    return thisSpace
